""".. include:: ../_notebooks/01-shannon.rst"""

from typing import Optional
import numpy as np


########################################################################
class Shannon:
    """Shannon entropy"""

    # ----------------------------------------------------------------------
    def __new__(self, data: np.ndarray, bins: Optional[int] = 16, base: Optional[int] = 2, conditional: Optional[int] = None) -> float:
        """Calculate the shannon entropy for `n` variables.

        If `n` is higher than 1, then the joint entropy is calculated.
        """
        # Data must be nxm
        if len(data.shape) == 1:
            data = data.reshape(1, -1)

        dist = self.dist(data, bins)

        if not conditional is None:
            return np.sum(- dist * np.log(dist) / np.log(base)) - (self.__new__(self, data[conditional], bins, base))
        else:
            return np.sum(- dist * np.log(dist) / np.log(base))

    # ----------------------------------------------------------------------
    @classmethod
    def dist(cls, x: np.ndarray, bins: int) -> np.ndarray:
        """Calculate the joint probability of `x`."""

        jointProbs, edges = np.histogramdd(x.T, bins=bins, normed=True)
        jointProbs /= jointProbs.sum()
        dist = jointProbs[jointProbs != 0]

        return dist
