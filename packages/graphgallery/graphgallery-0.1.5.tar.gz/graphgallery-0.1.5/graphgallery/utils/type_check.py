
import tensorflow as tf
import numpy as np
import collections.abc as collections_abc


def is_list_like(x):
    """Check if x is list like: `List` or `Tuple`
    """
    return isinstance(x, collections_abc.Sequence)


def is_sparse(x):
    """Check whether `x` is sparse.

    Check whether an object is a `tf.sparse.SparseTensor` or
    `tf.compat.v1.SparseTensorValue`.

    Arguments:
        x: A python object to check.

    Returns:
        `True` iff `x` is a `tf.sparse.SparseTensor` or
        `tf.compat.v1.SparseTensorValue`.
    """
    return isinstance(x, (tf.sparse.SparseTensor, tf.sparse.SparseTensorValue))


def is_tensor_or_variable(x):
    """Check whether `x` is tf.Tensor or tf.Variable.

    Arguments:
        x: A python object to check.

    Returns:
        `True` iff `x` is a `tf.Tensor` or `tf.Variable`.
    """
    return tf.is_tensor(x) or isinstance(x, tf.Variable)


def is_interger_scalar(x):
    return isinstance(x, (int, np.int8,
                           np.int16,
                           np.int32,
                           np.int64,
                           np.uint8,
                           np.uint16,
                           np.uint32,
                           np.uint64,
                           ))
