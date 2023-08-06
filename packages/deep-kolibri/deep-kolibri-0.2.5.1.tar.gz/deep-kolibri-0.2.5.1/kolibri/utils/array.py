import functools
import operator

import numpy as np


def get_shape(l):
    d = 0
    while isinstance(l, list):
        d += 1
        l = l[0]
    return d


def flatten(l):
    while get_shape(l) >= 2:
        l = functools.reduce(operator.iconcat, l, [])
    return l


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def get_dimensions(X):
    """ Return the dimensions from a numpy.array, numpy.ndarray or list.

    Parameters
    ----------
    X: numpy.array, numpy.ndarray, list, list of lists.

    Returns
    -------
    tuple
        A tuple representing the X structure's dimensions.
    """
    r, c = 1, 1
    if isinstance(X, type(np.array([0]))):
        if X.ndim > 1:
            r, c = X.shape
        else:
            r, c = 1, X.size

    elif isinstance(X, type([])):
        if isinstance(X[0], type([])):
            r, c = len(X), len(X[0])
        else:
            c = len(X)

    return r, c
