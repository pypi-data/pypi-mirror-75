""".. include:: ../_notebooks/01-vq.rst"""

import numpy as np
from typing import Optional
import scipy.spatial.distance as dis


########################################################################
class VQEntropy:
    """"""

    # ----------------------------------------------------------------------
    def __new__(self, data: np.ndarray, r: Optional[float] = None, tau: Optional[int] = 3, base: Optional[int] = np.e, conditional: Optional[int] = None) -> float:
        """Constructor"""

        # Data must be nxm
        if len(data.shape) == 1:
            data = data.reshape(1, -1)

        if x.shape[0] > 1:
            pds, norm = self.joint(data, r, tau)
        else:
            pds, norm = self.marginal(data, r, tau)

        ent = np.sum(-psd * (np.log(psd) / np.log(base)))
        return ent / norm

    # ----------------------------------------------------------------------
    @classmethod
    def joint(cls, data, r=None, tau=3):
        """"""
        if r is None:
            r = 0.2 * data.std()

        X = [data[i, :].reshape(1, data.shape[1])
             for i in range(data.shape[0])]
        Xm = [cls.symbol_set(i, tau) for i in X]
        XX = []
        for i in Xm:
            XX += i
        D = cls.quantize_set(XX, r)

        xx = np.asarray(XX)

        d = dis.cdist(np.asarray(D), np.asarray(XX))
        sig = np.median(d)
        simil = np.exp(-((d)**2) / (2 * sig**2))

        # print(sum(simil.ravel()))
        Pd = np.mean(simil, axis=1)
        m = np.mean(np.asarray([xx[:, i].reshape(
            xx[:, i].shape[0], 1) * simil.T for i in range(xx.shape[1])]), axis=1).T
        var = np.mean(((dis.cdist(xx, m).T)**2) * simil, axis=1)
        d2 = dis.cdist(xx, m)
        simil2 = np.exp(-((d2)**2) / (2 * var))

        Psd = np.mean(simil2, axis=0)
        Pds = Psd * Pd

        return Pds, len(XX) / len(X)

    # ----------------------------------------------------------------------
    @classmethod
    def marginal(cls, X, r=None, tau=3):
        """"""
        if r is None:
            r = 0.2 * X.std()

        pos = 0
        Xm = []
        while pos + tau + 1 < X.shape[1]:
            Xm.append(X[:, pos:pos + tau])
            pos = pos + tau
        D = []
        for sim in Xm:
            if len(D) == 0:
                D.append(sim.ravel())
            elif np.sum(dis.cdist(np.asarray(D), sim) < r) == False:
                D.append(sim.ravel())
        Xm = [i.ravel() for i in Xm]
        xx = np.asarray(Xm)
        d = dis.cdist(np.asarray(D), np.asarray(Xm))
        sig = np.median(d)
        simil = np.exp(-((d)**2) / (2 * sig**2))
        # print(sum(simil.ravel()))
        Pd = np.mean(simil, axis=1)
        m = np.mean(np.asarray([xx[:, i].reshape(
            xx[:, i].shape[0], 1) * simil.T for i in range(xx.shape[1])]), axis=1).T
        var = np.mean(((dis.cdist(xx, m).T)**2) * simil, axis=1)
        d2 = dis.cdist(xx, m)
        simil2 = np.exp(-((d2)**2) / (2 * var))
        Psd = np.mean(simil2, axis=0)
        Pds = Psd * Pd
        # print(len(D),len(Xm))
        # E = -np.sum(Pds * np.log(Pds)) / len(Xm)
        return Pds, len(Xm)

    # ----------------------------------------------------------------------
    @classmethod
    def symbol_set(cls, x, tau):
        """"""
        pos = 0
        Xm = []
        while pos + tau + 1 < x.shape[1]:
            Xm.append(x[:, pos:pos + tau])
            pos = pos + tau
        Xm = [i.ravel() for i in Xm]
        return Xm

    # ----------------------------------------------------------------------
    @classmethod
    def quantize_set(cls, Xm, r):
        """"""
        D = []
        for sim in Xm:
            if len(D) == 0:
                D.append(sim)
            elif np.sum(dis.cdist(np.asarray(D), sim.reshape(1, sim.shape[0])) < r) == False:
                D.append(sim)
        return D
