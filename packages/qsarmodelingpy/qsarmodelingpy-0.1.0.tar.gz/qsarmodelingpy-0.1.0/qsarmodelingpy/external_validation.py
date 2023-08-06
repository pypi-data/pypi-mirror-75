import sys
import numpy as np
import pandas as pd
from qsarmodelingpy.validacao_externa import ExternalValidation
from qsarmodelingpy.cross_validation_class import CrossValidation


if __name__ == '__main__':
    dfConf = pd.read_csv("confExtVal.csv", header=None)
    directory = dfConf[1][0]
    Xfile = dfConf[1][1]
    yfile = dfConf[1][2]
    test_set = dfConf[1][3]
    nLV = None if dfConf.isnull()[1][4] else int(dfConf[1][4])
    out_directory = dfConf[1][5]
    ext_val_file = dfConf[1][6]
    cv_file = dfConf[1][7]
    Xtrain_file = dfConf[1][8]
    ytrain_file = dfConf[1][9]
    Xtest_file = dfConf[1][10]
    ytest_file = dfConf[1][11]
    autoscale = dfConf[1][12].upper() == "YES"
    dfX = pd.read_csv(directory+"/"+Xfile, sep=';', index_col=0)
    y = pd.read_csv(directory+"/"+yfile, sep=';', header=None).values
    X = dfX.values
    ext = ExternalValidation(X, y, nLV)
    test = [int(i)-1 for i in test_set.split(',')]
    train = [j for j in range(len(y)) if j not in test]
    ext.extVal(train, test)
    ext.saveExtVal(train, test, out_directory+"/"+ext_val_file)
    cv = CrossValidation(X[train, :], y[train], nLVMax=nLV, scale=True)
    cv.saveParameters(out_directory+"/"+cv_file)
    # dfXtrain = pd.DataFrame(X[train,:],columns=dfX.columns)
    dfXtrain = dfX.loc[dfX.index[train], dfX.columns]
    dfXtrain.to_csv(out_directory+"/"+Xtrain_file, sep=';')
    dfytrain = pd.DataFrame(y[train])
    dfytrain.to_csv(out_directory+"/"+ytrain_file, sep=',', header=False)
    # dfXtest = pd.DataFrame(X[test,:],columns=dfX.columns)
    dfXtest = dfX.loc[dfX.index[test], dfX.columns]
    dfXtest.to_csv(out_directory+"/"+Xtest_file, sep=';')
    dfytest = pd.DataFrame(y[test])
    dfytest.to_csv(out_directory+"/"+ytest_file, sep=',', header=False)
