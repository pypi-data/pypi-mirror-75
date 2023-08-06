from qsarmodelingpy.leaveNout import LeaveNout
import numpy as np
from sklearn.cross_decomposition import PLSRegression
import qsarmodelingpy.calculate_parameters as cp


class LNO(object):
    """docstring for LNO"""

    def __init__(self, X, y, nLV, n=None, nrepet=5):
        self.X = X
        self.y = y
        if nLV != None:
            self. nLV = nLV
        else:
            self. nLV = len(y)/5
        if n == None:
            self.n = int(len(y)/4)
        else:
            self.n = n
        self.nrepet = nrepet
        ycv = np.zeros((len(y), 1))
        self.Q2 = np.zeros((self.n, nrepet))
        i = 0
        pls = PLSRegression(n_components=nLV)
        n_samples = np.shape(X)[0]
        for i in range(self.n):
            lno = LeaveNout(i+1, n_repeats=self.nrepet)
            nsplits = int(n_samples/(i+1))
            if n_samples % (i+1) != 0:
                nsplits += 1
            j = 0
            k = 0
            for train, test in lno.split(X):
                pls.fit(X[train, :], y[train])
                ycv[test, :] = pls.predict(X[test, :])
                j = (j+1) % nsplits
                if j == 0:
                    self.Q2[i, k] = cp.calcR2(self.y, ycv)
                    k = k + 1
        # self.Q2[i,:] = [cp.calcR2(self.y[:,0],self.ycv[:,i]) for i in range(self.nrepet)]
