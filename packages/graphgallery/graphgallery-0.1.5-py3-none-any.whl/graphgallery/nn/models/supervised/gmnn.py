import numpy as np
import tensorflow as tf
from tensorflow.keras import Model, Input
from tensorflow.keras.layers import Dropout, Softmax
from tensorflow.keras.optimizers import RMSprop, Adam
from tensorflow.keras import regularizers

from graphgallery.nn.layers import GraphConvolution
from graphgallery.sequence import FullBatchNodeSequence
from graphgallery.nn.models import SupervisedModel
from graphgallery.utils.shape_utils import set_equal_in_length
from graphgallery import astensor, asintarr, normalize_x, normalize_adj, Bunch


class GMNN(SupervisedModel):
    """
        Implementation of Graph Markov Neural Networks (GMNN). 
        `Graph Markov Neural Networks <https://arxiv.org/abs/1905.06214>`
        Pytorch implementation: <https://github.com/DeepGraphLearning/GMNN>

        Arguments:
        ----------
            adj: shape (N, N), Scipy sparse matrix if  `is_adj_sparse=True`, 
                Numpy array-like (or matrix) if `is_adj_sparse=False`.
                The input `symmetric` adjacency matrix, where `N` is the number 
                of nodes in graph.
            x: shape (N, F), Scipy sparse matrix if `is_x_sparse=True`, 
                Numpy array-like (or matrix) if `is_x_sparse=False`.
                The input node feature matrix, where `F` is the dimension of features.
            labels: Numpy array-like with shape (N,)
                The ground-truth labels for all nodes in graph.
            norm_adj_rate (Float scalar, optional): 
                The normalize rate for adjacency matrix `adj`. (default: :obj:`-0.5`, 
                i.e., math:: \hat{A} = D^{-\frac{1}{2}} A D^{-\frac{1}{2}}) 
            norm_x_type (String, optional): 
                How to normalize the node feature matrix. See `graphgallery.normalize_x`
                (default :str: `l1`)
            device (String, optional): 
                The device where the model is running on. You can specified `CPU` or `GPU` 
                for the model. (default: :str: `CPU:0`, i.e., running on the 0-th `CPU`)
            seed (Positive integer, optional): 
                Used in combination with `tf.random.set_seed` & `np.random.seed` & `random.seed`  
                to create a reproducible sequence of tensors across multiple calls. 
                (default :obj: `None`, i.e., using random seed)
            name (String, optional): 
                Specified name for the model. (default: :str: `class.__name__`)

    """

    def __init__(self, adj, x, labels, norm_adj_rate=-0.5, norm_x_type='l1',
                 device='CPU:0', seed=None, name=None, **kwargs):

        super().__init__(adj, x, labels, device=device, seed=seed, name=name, **kwargs)

        self.norm_adj_rate = norm_adj_rate
        self.norm_x_type = norm_x_type
        self.preprocess(adj, x)
        self.labels_onehot = np.eye(self.n_classes)[labels]
        self.custom_objects = {'GraphConvolution': GraphConvolution}

    def preprocess(self, adj, x):
        super().preprocess(adj, x)
        # check the input adj and x, and convert them into proper data types
        adj, x = self._check_inputs(adj, x)

        if self.norm_adj_rate:
            adj = normalize_adj(adj, self.norm_adj_rate)

        if self.norm_x_type:
            x = normalize_x(x, norm=self.norm_x_type)

        with tf.device(self.device):
            self.x_norm, self.adj_norm = astensor([x, adj])

    def build(self, hiddens=[16], activations=['relu'], dropouts=[0.6], l2_norms=[5e-4],
              lr=0.05, use_bias=False, ensure_shape=True):

        local_paras = locals()
        local_paras.pop('self')
        paras = Bunch(**local_paras)
        hiddens, activations, dropouts, l2_norms = set_equal_in_length(hiddens, activations, dropouts, l2_norms)
        paras.update(Bunch(hiddens=hiddens, activations=activations, dropouts=dropouts, l2_norms=l2_norms))
        # update all parameters
        self.paras.update(paras)
        self.model_paras.update(paras)

        with tf.device(self.device):
            tf.random.set_seed(self.seed)
            x_p = Input(batch_shape=[None, self.n_classes], dtype=self.floatx, name='input_p')
            x_q = Input(batch_shape=[None, self.n_features], dtype=self.floatx, name='input_q')
            adj = Input(batch_shape=[None, None], dtype=self.floatx, sparse=True, name='adj_matrix')
            index = Input(batch_shape=[None],  dtype=self.intx, name='index')

            def build_GCN(x):
                h = x
                for hid, activation, dropout, l2_norm in zip(hiddens, activations, dropouts, l2_norms):
                    h = GraphConvolution(hid, use_bias=use_bias,
                                         activation=activation,
                                         kernel_regularizer=regularizers.l2(l2_norm))([h, adj])
                    h = Dropout(rate=dropout)(h)

                h = GraphConvolution(self.n_classes, use_bias=use_bias)([h, adj])
                # To aviod the UserWarning of `tf.gather`, but it causes the shape
                # of the input data to remain the same
                if ensure_shape:
                    h = tf.ensure_shape(h, [self.n_nodes, self.n_classes])
                h = tf.gather(h, index)
                output = Softmax()(h)

                model = Model(inputs=[x, adj, index], outputs=output)
                model.compile(loss='categorical_crossentropy', optimizer=RMSprop(lr=lr), metrics=['accuracy'])
                return model

            # model_p
            model_p = build_GCN(x_p)

            # model_q
            model_q = build_GCN(x_q)

            self.model_p, self.model_q = model_p, model_q
            self.set_model(self.model_q)

    def train(self, index_train, index_val=None, pre_train_epochs=100,
              epochs=100, early_stopping=None, verbose=None, save_best=True,
              weight_path=None, as_model=False,
              monitor='val_acc', early_stop_metric='val_loss'):

        histories = []
        index_all = tf.range(self.n_nodes, dtype=self.intx)

        # pre train model_q
        self.set_model(self.model_q)
        history = super().train(index_train, index_val, epochs=pre_train_epochs,
                                early_stopping=early_stopping,
                                verbose=verbose, save_best=save_best, weight_path=weight_path, as_model=True,
                                monitor=monitor, early_stop_metric=early_stop_metric)
        histories.append(history)

        label_predict = self.predict(index_all).argmax(1)
        label_predict[index_train] = self.labels[index_train]
        label_predict = tf.one_hot(label_predict, depth=self.n_classes)
        # train model_p fitst
        with tf.device(self.device):
            train_sequence = FullBatchNodeSequence([label_predict, self.adj_norm, index_all], label_predict)
            if index_val is not None:
                val_sequence = FullBatchNodeSequence([label_predict, self.adj_norm, index_val], self.labels_onehot[index_val])
            else:
                val_sequence = None

        self.set_model(self.model_p)
        history = super().train(train_sequence, val_sequence, epochs=epochs,
                                early_stopping=early_stopping,
                                verbose=verbose, save_best=save_best, weight_path=weight_path, as_model=as_model,
                                monitor=monitor, early_stop_metric=early_stop_metric)
        histories.append(history)

        # then train model_q again
        label_predict = self.model.predict_on_batch(astensor([label_predict, self.adj_norm, index_all]))
        if tf.is_tensor(label_predict):
            label_predict = label_predict.numpy()

        label_predict[index_train] = self.labels_onehot[index_train]

        self.set_model(self.model_q)
        with tf.device(self.device):
            train_sequence = FullBatchNodeSequence([self.x_norm, self.adj_norm, index_all], label_predict)
        history = super().train(train_sequence, index_val, epochs=epochs,
                                early_stopping=early_stopping,
                                verbose=verbose, save_best=save_best,
                                weight_path=weight_path, as_model=as_model,
                                monitor=monitor, early_stop_metric=early_stop_metric)

        histories.append(history)
        # update training paras and all paras
        self.train_paras.update(Bunch(pre_train_epochs=pre_train_epochs))
        self.paras.update(Bunch(pre_train_epochs=pre_train_epochs))

        return histories

    def train_sequence(self, index):
        index = asintarr(index)
        labels = self.labels_onehot[index]
        with tf.device(self.device):
            sequence = FullBatchNodeSequence([self.x_norm, self.adj_norm, index], labels)
        return sequence

    def predict(self, index):
        super().predict(index)
        index = asintarr(index)
        with tf.device(self.device):
            index = astensor(index)
            logit = self.model.predict_on_batch([self.x_norm, self.adj_norm, index])

        if tf.is_tensor(logit):
            logit = logit.numpy()
        return logit
