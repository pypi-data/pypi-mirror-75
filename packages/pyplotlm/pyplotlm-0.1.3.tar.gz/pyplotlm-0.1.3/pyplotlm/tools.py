import numpy as np
import matplotlib.pyplot as plt

class Error(Exception):
    """ base class
    """
    pass

class DimensionError(Error):
    """ raise when dimension mismatch
    """
    pass

def abline(intercept, slope, x_min=0, x_max=10, marker=':', color='black'):
    """ plot a line from slope and intercept
    Parameters: intercept (float) - intercept
                slope (float) - slope
                x_min (float) - x minimum value, optional, default is 0
                x_max (float) - x maximum value, optional, default is 10
                marker (str) - matplotlib marker
                color (str) - line color
    """
    x_vals = np.linspace(x_min, x_max)
    y_vals = x_vals*slope + intercept
    plt.plot(x_vals, y_vals, marker, color=color)
