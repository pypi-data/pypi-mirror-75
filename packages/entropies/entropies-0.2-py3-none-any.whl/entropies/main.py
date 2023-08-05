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
        return np.array([entropy(d, **kwargs) for d in sld_data])


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

    # ----------------------------------------------------------------------
    @classmethod
    def marginal2joint(cls, marginals):
        """"""
        logging.debug(f'Performing marginal -> joint algorithm')
        x = np.array([np.random.choice(range(p.shape[0]), 2**10, p=p)
                      for p in marginals])

        p, _ = np.histogramdd(x.T, bins=100, density=True)
        p /= np.sum(p)

        return p, 1


########################################################################
class Dist:
    """"""

    # ----------------------------------------------------------------------
    @classmethod
    def vq_dist(cls, x, r=None, tau=3):

        if r is None:
            r = 0.2 * x.std()

        m = x.shape[0] % tau
        if m:
            x = x[:-m]
        x = x.reshape(-1, tau)

        D = [x[0]]
        [D.append(sim) for sim in x if not np.sum(
            dis.cdist(np.asarray(D), [sim]) < r)]
        D = np.array(D)

        d = dis.cdist(D, x)
        sig = np.median(d)
        simil = np.exp(-((d)**2) / (2 * sig**2))

        Pd = simil.mean(axis=1)
        m = np.mean(np.asarray([x[:, i].reshape(
            x[:, i].shape[0], 1) * simil.T for i in range(x.shape[1])]), axis=1).T

        d2 = dis.cdist(x, m)
        var = np.mean(((dis.cdist(x, m).T)**2) * simil, axis=1)
        simil2 = np.exp(-((d2)**2) / (2 * var))

        psd = simil2.mean(axis=0)
        psd = psd * Pd
        psd /= np.sum(psd)

        return psd

    # ----------------------------------------------------------------------
    @classmethod
    def vq(cls, x, r=None, tau=3, **kwargs):
        """"""
        psd = cls.vq_dist(x, r, tau)
        return np.sum(-psd * np.log(psd) / np.log(kwargs.get('base', 2))) / x.shape[0]

    # ----------------------------------------------------------------------
    @classmethod
    def shannon_dist(cls, x, bins=16):
        """"""
        jointProbs, edges = np.histogramdd(x.T, bins=bins, normed=True)
        jointProbs /= jointProbs.sum()
        non_zeros = jointProbs[jointProbs != 0]

        return non_zeros

    # ----------------------------------------------------------------------
    @classmethod
    def shannon(cls, x, bins=16, base=2, **kwargs):
        """"""
        non_zeros = cls.shannon_dist(x, bins)
        return np.sum(- non_zeros * np.log(non_zeros) / np.log(base))

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


