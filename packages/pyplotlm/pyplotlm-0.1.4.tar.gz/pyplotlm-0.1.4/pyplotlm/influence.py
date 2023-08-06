import numpy as np
from numpy.linalg import *

def leverage(X):
    """ compute leverage of a design matrix

    Parameters: X (nd-array) - the design matrix (with intercept)

    Returns: (array) - the leverage
    """
    # the orthogonal projection onto the column space of X
    H = np.dot(np.dot(X, np.linalg.inv(np.dot(X.T, X))), X.T)
    # diagonal of hat matrix, aka, leverage
    H_diag = H.diagonal()

    return H_diag

def internally_studentized(residuals, h, p, n):
    """ compute the Internally Studentized Residuals

    Parameters: residual (array-like) - the raw residuals
                h (array-like) - leverae of the design matrix
                p (int) - coefficients dimensions
                n (int) - total numbers of observations

    Returns: (array) - the studentized residual
    """
    sigma = np.sqrt((1/(n-p))*np.dot(residuals.T, residuals))
    standardized_residuals = residuals / (sigma*np.sqrt(1-h))
    return standardized_residuals

def cooks_distance(standard_residuals, h, p):
    """ compute cook's distance

    Parameters: standard_residuals (array) - studentized residauls
                h (array) - leverage
                p (int) - coefficients dimensions

    Returns: (array) - an array of Cook's distance
    """
    cooks = (h / (1-h)) * (standard_residuals**2 / p)
    return cooks

################### for t test ###################
def coef_standard_error(residuals, X):
    """ find standard errors of regression coefficients

    Parameters: residuals (array) - raw residuals
                X (nd-array) - design matrix, including intercept

    Returns: (nd-array) - the standard errors of regression coefficients
    """
    sse = np.dot(residuals.T, residuals) / (X.shape[0] - X.shape[1])
    se = np.sqrt(np.diagonal(sse * np.linalg.inv(np.dot(X.T, X))))
    return se

################### r2 & adj r2 ###################
def r_squared(y, residuals, p):
    """ compute r-squared and adjusted r-squared

    Parameters: y (array) - raw response
                residuals (array) - raw residuals
                p (int) - coefficients dimensions, including intercept

    Returns: r2, adj_r2 (float), (float)
    """
    n = len(y)
    sse = np.sum(residuals**2)
    sst = np.sum((y - np.mean(y))**2)
    r2 = 1 - (sse / sst)
    adj_r2 = 1 - ((sse / (n-p)) / (sst/(n-1)))
    return r2, adj_r2

################### for f test ###################
def f_stat(residuals, fitted_values, y, p):
    """ compute f statistics for testing regression model slope

    Parameters: residuals (array) - raw residuals
                fitted_values (array) - the model fitted values
                y (array) - raw response
                p (int) - coefficients dimesnion, including intercept

    Returns: (float) - the f statistics for the model
    """
    n = len(y)
    sse = np.sum(residuals**2)
    ssr = np.sum((fitted_values - np.mean(y))**2)
    f_stat = (ssr / (p-1)) / (sse / (n-p))
    return f_stat
