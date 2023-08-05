import tensorflow as tf
from tensorflow.keras import Model, Input
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import regularizers

from graphgallery.nn.layers import SGConvolution
from graphgallery.nn.models import SupervisedModel
from graphgallery.sequence import FullBatchNodeSequence
from graphgallery.utils.shape_utils import repeat
from graphgallery import astensor, asintarr, normalize_x, normalize_adj, Bunch


class SGC(SupervisedModel):
    """
        Implementation of Simplifying Graph Convolutional Networks (RobustGCN). 
        `Simplifying Graph Convolutional Networks <https://arxiv.org/abs/1902.07153>`
        Pytorch implementation: <https://github.com/Tiiiger/SGC>

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
            order (Positive integer, optional): 
                The power (order) of adjacency matrix. (default :obj: `2`, i.e., math:: A^{2})
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

    def __init__(self, adj, x, labels, order=2,
                 norm_adj_rate=-0.5, norm_x_type='l1',
                 device='CPU:0', seed=None, name=None, **kwargs):

        super().__init__(adj, x, labels, device=device, seed=seed, name=name, **kwargs)

        self.order = order
        self.norm_adj_rate = norm_adj_rate
        self.norm_x_type = norm_x_type
        self.preprocess(adj, x)

    def preprocess(self, adj, x):
        super().preprocess(adj, x)
        # check the input adj and x, and convert them into proper data types
        adj, x = self._check_inputs(adj, x)

        if self.norm_adj_rate:
            adj = normalize_adj(adj, self.norm_adj_rate)

        if self.norm_x_type:
            x = normalize_x(x, norm=self.norm_x_type)

        with tf.device(self.device):
            x, adj = astensor([x, adj])
            x = SGConvolution(order=self.order)([x, adj])
            self.x_norm, self.adj_norm = x, adj

    def build(self, lr=0.2, l2_norms=5e-5):
        l2_norms = repeat(l2_norms, 1)
        local_paras = locals()
        local_paras.pop('self')
        paras = Bunch(**local_paras)
        # update all parameters
        self.paras.update(paras)
        self.model_paras.update(paras)

        with tf.device(self.device):

            x = Input(batch_shape=[None, self.n_features], dtype=self.floatx, name='features')

            output = Dense(self.n_classes, activation='softmax', kernel_regularizer=regularizers.l2(l2_norms[0]))(x)

            model = Model(inputs=x, outputs=output)
            model.compile(loss='sparse_categorical_crossentropy', optimizer=Adam(lr=lr), metrics=['accuracy'])

            self.set_model(model)

    def train_sequence(self, index):
        index = asintarr(index)
        labels = self.labels[index]
        with tf.device(self.device):
            x = tf.gather(self.x_norm, index)
            sequence = FullBatchNodeSequence(x, labels)
        return sequence

    def predict(self, index):
        super().predict(index)
        index = asintarr(index)
        with tf.device(self.device):
            x = tf.gather(self.x_norm, index)
            logit = self.model.predict_on_batch(x)

        if tf.is_tensor(logit):
            logit = logit.numpy()
        return logit
