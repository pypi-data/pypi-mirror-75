import numpy as np
from math import sqrt
from sklearn.preprocessing import scale


def ssy(y, mean_y=None):
    if mean_y == None:
        mean_y = np.mean(y)
    ssy = sum((y-mean_y*np.ones(np.shape(y)))**2)
    return ssy


def calcPress(yreal, ypred):
    press = sum((yreal-ypred)**2)
    return press


def calcR2(yreal, ypred, mean_y=None):
    ssy1 = ssy(yreal, mean_y)
    R2 = 1-(calcPress(yreal, ypred)/ssy1)
    return R2


def calcMAE(yreal, ypred):
    MAE = 1/len(yreal)*np.sum(abs(yreal-ypred))
    return MAE


def calcRMSE(yreal, ypred):
    RMSE = sqrt(calcPress(yreal, ypred)/len(yreal))
    return RMSE


def calcR(yreal, ypred):
    r = np.dot(scale(yreal), scale(ypred))/(len(yreal))
    return r
