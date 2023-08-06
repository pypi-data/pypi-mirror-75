import os
import numpy as np
import scipy.io as sio
import pandas as pd
from scipy import stats
from sklearn.metrics.pairwise import euclidean_distances as EuDist2


def precision(y_true, y_pred):
    assert (len(y_pred) == len(y_true))
    N = len(y_pred)
    y_df = pd.DataFrame(data=y_pred, columns=["label"])
    ind_L = y_df.groupby("label").indices
    ni_L = [stats.mode(y_true[ind]).count[0] for yi, ind in ind_L.items()]
    return np.sum(ni_L) / N


def recall(y_true, y_pred):
    re = precision(y_true=y_pred, y_pred=y_true)
    return re


def load_Agg():
    this_directory = os.path.dirname(__file__)
    data_path = os.path.join(this_directory, "data/")
    name_full = os.path.join(data_path + "Agg.mat")
    X, y_true, N, dim, c_true = load_mat(name_full)
    return X, y_true, N, dim, c_true


def load_mat(path):
    data = sio.loadmat(path)
    X = data["X"]
    y_true = data["Y"].astype(np.int32).reshape(-1)
    N, dim, c_true = X.shape[0], X.shape[1], len(np.unique(y_true))
    return X, y_true, N, dim, c_true


def save_mat(name_full, xy):
    sio.savemat(name_full, xy)


def matrix_index_take(X, ind_M):
    assert np.all(ind_M >= 0)

    n, k = ind_M.shape
    row = np.repeat(np.array(range(n), dtype=np.int32), k)
    col = ind_M.reshape(-1)
    ret = X[row, col].reshape((n, k))
    return ret


def matrix_index_assign(X, ind_M, Val):
    n, k = ind_M.shape
    row = np.repeat(np.array(range(n), dtype=np.int32), k)
    col = ind_M.reshape(-1)
    if isinstance(Val, (float, int)):
        X[row, col] = Val
    else:
        X[row, col] = Val.reshape(-1)


