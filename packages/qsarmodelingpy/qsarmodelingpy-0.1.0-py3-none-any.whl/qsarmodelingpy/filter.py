import numpy as np
import pandas as pd
from sklearn.preprocessing import scale as autoscale
import logging

import qsarmodelingpy.lj_cut as lj


def variance_cut(X, cut):
    v = np.var(X, 0, ddof=1)
    indCut = [i for i in range(len(v)) if v[i] >= cut]
    return indCut


def autoscale1(X):
    m, n = np.shape(X)
    means = np.mean(X, 0)
    stds = np.std(X, 0, ddof=1)
    Xm = X-np.ones((m, 1))*means
    Xa = np.divide(Xm, np.ones((m, 1)))
    return Xa


def correlation_cut(X, y, cut):
    corr = abs(np.dot(np.transpose(autoscale(X)), autoscale(y))/(len(y)-1))
    indCut = [i for i in range(len(corr)) if corr[i] >= cut]
    return indCut


def autocorrelation_cut(X, y, cut):
    Xcorr = np.corrcoef(X.T)
    m, n = X.shape
    var_filtered = []
    for i in range(n):
        for j in range(i+1, n):
            corr = Xcorr[i, j]
            if corr > cut:
                corr_i = abs(
                    np.dot(np.transpose(autoscale(X[:, i])), autoscale(y))/(m-1))
                corr_j = abs(
                    np.dot(np.transpose(autoscale(X[:, j])), autoscale(y))/(m-1))
                if corr_i < corr_j:
                    if i not in var_filtered:
                        var_filtered.append(i)
                else:
                    if j not in var_filtered:
                        var_filtered.append(j)
    var = [i for i in range(n) if i not in var_filtered]
    return var


def filter_matrix(
    X: pd.DataFrame,
    y: pd.DataFrame,
    lj_transform: bool,
    var_cut: float,
    corr_cut: float,
    auto_corrcut: float,
) -> pd.DataFrame:

    # Pre processing
    if lj_transform:
        X = lj.transform(X)

    logging.info("Dimensions of the original matrix")
    logging.info(X.shape)

    # Variance Cut
    indVar = variance_cut(X.values, var_cut)
    X = X.loc[:, X.columns[indVar]]

    logging.info("Dimensions of the matrix after variance cut")
    logging.info(X.shape)

    # Correlation Cut
    indCorr = correlation_cut(X.values, y, corr_cut)
    X = X.loc[:, X.columns[indCorr]]

    logging.info("Dimensions of the matrix after correlation cut")
    logging.info(X.shape)

    # Autocorrelation cut
    indAuto = autocorrelation_cut(X.values, y, auto_corrcut)
    X = X.loc[:, X.columns[indAuto]]

    logging.info("Dimensions of the matrix after auto correlation cut")
    logging.info(X.shape)

    return X
