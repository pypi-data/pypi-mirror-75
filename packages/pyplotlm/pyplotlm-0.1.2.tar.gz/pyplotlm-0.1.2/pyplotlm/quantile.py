import numpy as np
from scipy import stats

def theorectical_quantiles(residuals):
    """ compute the theorectical quantiles of residuals

    Parameters: residuals (array-like) - the raw residuals

    Returns: (array-like) - the theorectical quantiles
    """
    sorted_ = np.sort(residuals)
    below_xi = (np.arange(1, len(sorted_)+1) - 0.5) / len(sorted_)

    theo_quantiles = stats.norm.ppf(below_xi)
    return theo_quantiles
