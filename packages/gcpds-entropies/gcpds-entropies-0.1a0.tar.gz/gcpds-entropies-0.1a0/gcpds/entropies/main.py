import numpy as np
from scipy.signal import periodogram, welch
import scipy.spatial.distance as dis
from functools import lru_cache
import logging


# ----------------------------------------------------------------------
def joint_entropy(data, method='shannon', dist=False, **kwargs):  # P(X,Y)
    """"""
    if dist:
        data = Tools.dist2data(data)

    if data.shape[0] > 1:
        logging.debug(f'Performing Joint {method} Entropy')

    ent = getattr(Dist, method)(data, **kwargs)
    return ent


# ----------------------------------------------------------------------
def conditional_entropy(data, conditional_index=0, method='shannon', dist=False, base=2, **kwargs):  # P(X|Y)
    """"""
    logging.debug(f'Performing Conditional {method} Entropy')
    if dist:
        data = Tools.dist2data(data)

    return joint_entropy(data, method=method, base=base, **kwargs) - joint_entropy(data[conditional_index], method=method, base=base, **kwargs)


# ----------------------------------------------------------------------
def entropy(x, method='shannon', dist=False, base=2, **kwargs):
    """"""
    logging.debug(f'Performing {method} Entropy')

    if len(x.shape) == 1:
        x = x.reshape(1, -1)

    return joint_entropy(x, method=method, base=base, **kwargs)


# ----------------------------------------------------------------------
def sliding_entropy(x, window, overlap=0.9, conditional=False, **kwargs):
    """"""
    if isinstance(x, (list, tuple)):
        x = np.asarray(x)

    if len(x.shape) > 1 and x.shape[0] > 1:
        sld_data = zip(*[Tools.sliding_window(xi, window, overlap)
                         for xi in x])
    else:
        if x.shape[0] == 1:
            x = x[0]
        sld_data = Tools.sliding_window(x, window, overlap)

    if conditional:
        return np.array([conditional_entropy(d, **kwargs) for d in sld_data])
    else:
        return np.array([entropy(np.array(d), **kwargs) for d in sld_data])


########################################################################
class Tools:
    """"""

    # ----------------------------------------------------------------------
    @classmethod
    @lru_cache(maxsize=32)
    def dist2data(cls, dist, N=1000):
        """"""
        P = [p[p != 0] for p in dist if p[p != 0].shape[0]]
        data = np.array([[np.random.choice(p.shape[0], p=p / np.sum(p))
                          for i in range(N)] for p in P])
        return data

    # ----------------------------------------------------------------------
    @classmethod
    def sliding_window(cls, data, window, overlap):
        """"""
        return np.array([data[start:start + window] for start in range(0, len(data) - (window - int(np.ceil(window * (1 - overlap)))), int(np.ceil(window * (1 - overlap))))], dtype=object)

    # ----------------------------------------------------------------------
    @classmethod
    def marginal(cls, joint, index=-1):
        """"""
        if index == -1:
            return np.array([marginal(joint, index=i) for i in range(len(joint.shape))])

        y = joint.copy()
        for i in range(len(joint.shape)):
            if i != index:
                y = np.sum(y, axis=i, keepdims=True)
        return y.flatten()

    # # # ----------------------------------------------------------------------
    # # @classmethod
    # # def marginal2joint(cls, marginals):
        # # """"""
        # # logging.debug(f'Performing marginal -> joint algorithm')
        # # x = np.array([np.random.choice(range(p.shape[0]), 2**10, p=p)
                      # # for p in marginals])

        # # p, _ = np.histogramdd(x.T, bins=100, density=True)
        # # p /= np.sum(p)

        # # return p, 1


########################################################################
class Dist:
    """"""

    # # ----------------------------------------------------------------------
    # @classmethod
    # def vq_dist(cls, X, r=None, tau=3):

        # if r is None:
            # r = 0.2 * X.std()

        # # x = x.flatten()

        # # m = x.shape[0] % tau
        # # if m:
            # # x = x[:-m]
        # # x = x.reshape(-1, tau)

        # # D = [x[0]]
        # # [D.append(sim) for sim in x if not np.sum(
            # # dis.cdist(np.asarray(D), [sim]) < r)]
        # # D = np.array(D)

        # # d = dis.cdist(D, x)
        # # sig = np.median(d)
        # # simil = np.exp(-((d)**2) / (2 * sig**2))

        # # Pd = simil.mean(axis=1)
        # # m = np.mean(np.asarray([x[:, i].reshape(
            # # x[:, i].shape[0], 1) * simil.T for i in range(x.shape[1])]), axis=1).T

        # # d2 = dis.cdist(x, m)
        # # var = np.mean(((dis.cdist(x, m).T)**2) * simil, axis=1)
        # # simil2 = np.exp(-((d2)**2) / (2 * var))

        # # psd = simil2.mean(axis=0)
        # # psd = psd * Pd
        # # psd /= np.sum(psd)

        # # return psd, x.shape[0]

        # pos = 0
        # Xm = []
        # while pos + tau + 1 < X.shape[1]:
            # Xm.append(X[:, pos:pos + tau])
            # pos = pos + tau
        # D = []
        # for sim in Xm:
            # if len(D) == 0:
                # D.append(sim.ravel())
            # elif np.sum(dis.cdist(np.asarray(D), sim) < r) == False:
                # D.append(sim.ravel())
        # Xm = [i.ravel() for i in Xm]
        # xx = np.asarray(Xm)
        # d = dis.cdist(np.asarray(D), np.asarray(Xm))
        # sig = np.median(d)
        # simil = np.exp(-((d)**2) / (2 * sig**2))
        # # print(sum(simil.ravel()))
        # Pd = np.mean(simil, axis=1)
        # m = np.mean(np.asarray([xx[:, i].reshape(
            # xx[:, i].shape[0], 1) * simil.T for i in range(xx.shape[1])]), axis=1).T
        # var = np.mean(((dis.cdist(xx, m).T)**2) * simil, axis=1)
        # d2 = dis.cdist(xx, m)
        # simil2 = np.exp(-((d2)**2) / (2 * var))
        # Psd = np.mean(simil2, axis=0)
        # Pds = Psd * Pd
        # # print(len(D),len(Xm))
        # # E = -np.sum(Pds * np.log(Pds)) / len(Xm)
        # return Pds, len(Xm)

    # # ----------------------------------------------------------------------
    # @classmethod
    # def vq(cls, x, r=None, tau=3, **kwargs):
        # """"""
        # if x.shape[0] > 1:
            # psd, norm = cls.VQ_multi(x, r, tau)
        # else:
            # psd, norm = cls.vq_dist(x, r, tau)

        # E = np.sum(-psd * (np.log(psd) / np.log(kwargs.get('base', 2))))
        # return E / norm

    # # ----------------------------------------------------------------------
    # @classmethod
    # def shannon_dist(cls, x, bins=16):
        # """"""
        # jointProbs, edges = np.histogramdd(x.T, bins=bins, normed=True)
        # jointProbs /= jointProbs.sum()
        # non_zeros = jointProbs[jointProbs != 0]

        # return non_zeros

    # # ----------------------------------------------------------------------
    # @classmethod
    # def shannon(cls, x, bins=16, base=2, **kwargs):
        # """"""
        # non_zeros = cls.shannon_dist(x, bins)
        # return np.sum(- non_zeros * np.log(non_zeros) / np.log(base))

    # ----------------------------------------------------------------------
    @classmethod
    def spectral_dist(cls, x, sf=1, method='fft', nperseg=None, **kwargs):
        """"""
        if x.shape[0] > 1:
            return Tools.marginal2joint([cls.spectral(xi.reshape(1, -1), sf, method, nperseg) for xi in x])
        x = x.flatten()

        if method == 'fft':
            _, psd = periodogram(x, sf)
        elif method == 'welch':
            _, psd = welch(x, sf, nperseg=nperseg)
        psd_norm = np.divide(psd, psd.sum())

        psd_norm = np.abs(psd_norm)
        psd_norm = psd_norm[psd_norm > 0]

        return psd_norm

    # ----------------------------------------------------------------------
    @classmethod
    def spectral(cls, x, sf=1, method='fft', nperseg=None, base=2, **kwargs):
        """"""
        non_zeros = cls.spectral_dist(x, sf, method, nperseg)
        return np.sum(- non_zeros * np.log(non_zeros) / np.log(base))

    # ----------------------------------------------------------------------
    @classmethod
    def renyi(cls, x, a=0, bins=16, **kwarg):
        """"""
        dist = cls.shannon_dist(x, bins)
        return (1 / (1 - a)) * np.log2(np.sum(dist**a))

    # @classmethod
    # def symbol_set(cls, X, tau):
        # pos = 0
        # Xm = []
        # while pos + tau + 1 < X.shape[1]:
            # Xm.append(X[:, pos:pos + tau])
            # pos = pos + tau
        # Xm = [i.ravel() for i in Xm]
        # return Xm

    # @classmethod
    # def quantize_set(cls, Xm, r):
        # D = []
        # for sim in Xm:
            # if len(D) == 0:
                # D.append(sim)
            # elif np.sum(dis.cdist(np.asarray(D), sim.reshape(1, sim.shape[0])) < r) == False:
                # D.append(sim)
        # return D

    # @classmethod
    # def VQ_multi(cls, x, r=None, tau=3):

        # if r is None:
            # r = 0.2 * x.std()

        # X = [x[i, :].reshape(1, x.shape[1]) for i in range(x.shape[0])]
        # Xm = [cls.symbol_set(i, tau) for i in X]
        # XX = []
        # for i in Xm:
            # XX += i
        # D = cls.quantize_set(XX, r)

        # xx = np.asarray(XX)

        # d = dis.cdist(np.asarray(D), np.asarray(XX))
        # sig = np.median(d)
        # simil = np.exp(-((d)**2) / (2 * sig**2))

        # # print(sum(simil.ravel()))
        # Pd = np.mean(simil, axis=1)
        # m = np.mean(np.asarray([xx[:, i].reshape(
            # xx[:, i].shape[0], 1) * simil.T for i in range(xx.shape[1])]), axis=1).T
        # var = np.mean(((dis.cdist(xx, m).T)**2) * simil, axis=1)
        # d2 = dis.cdist(xx, m)
        # simil2 = np.exp(-((d2)**2) / (2 * var))

        # Psd = np.mean(simil2, axis=0)
        # Pds = Psd * Pd
        # # print(Psd)
        # # E = -np.sum(Pds * np.log(Pds)) / (len(XX) / len(X))
        # # E = -np.sum(Pds * np.log(Pds)) / len(XX)
        # return Pds, len(XX) / len(X)

    @classmethod
    def fuzzy(cls, X, m=3, r=None, **kwarg):

        if r is None:
            r = 0.2 * X.std()

        N = X.shape[1]
        phi = np.zeros((1, 2))
        X_n = X
        patterns = np.zeros((m + 1, N - m))

        for i in range(m + 1):
            patterns[i, :] = X_n[0, i:N - m + i]
        #patterns = patterns - np.mean(patterns,axis=0)
        for kk in range(m, m + 2):
            #dist = dis.pdist(patterns[0:kk,0:N-m+1].T,metric='chebyshev')
            dist = dis.pdist((patterns[0:kk, 0:N - m + 1] - np.mean(
                patterns[0:kk, 0:N - m + 1], axis=0)).T, metric='chebyshev')
            # print(patterns[0:kk,0:N-m+1],np.mean(patterns[0:kk,0:N-m+1]))
            #Dg = np.exp(-np.log(2)*(dist**2/r**2))
            Dg = np.exp(-(dist**2 / r))
            phi[0, kk - m] = np.sum(Dg) / (N - m) / (N - m)

        FEn = np.log(phi[0, 0]) - np.log(phi[0, 1])
        return FEn

    @classmethod
    def samp(cls, x, m=3, r=None, **kwarg):

        if r is None:
            r = 0.2 * x.std()

        N = x.shape[1]
        m_aux = m
        i = np.arange(0, N - m_aux + 1)
        x_m = np.zeros((i.shape[0], m_aux))

        for ii in i:
            x_m[ii, :] = x[0, ii:ii + m_aux]

        Dist = dis.pdist(x_m, metric='chebyshev')
        Bm1 = 2 * np.sum(Dist <= r) / (N - m_aux - 1) / (N - m_aux)

        m_aux = m + 1
        i = np.arange(0, N - m_aux + 1)
        x_m = np.zeros((i.shape[0], m_aux))

        for ii in i:
            x_m[ii, :] = x[0, ii:ii + m_aux]

        Dist = dis.pdist(x_m, metric='chebyshev')
        Bm2 = 2 * np.sum(Dist <= r) / (N - m_aux - 1) / (N - m_aux)

        SE = -np.log(Bm2 / Bm1)

        if np.isinf(SE) or np.isnan(SE):
            SE = -np.log(2 / ((N - m_aux - 1) * (N - m_aux)))
        return SE
