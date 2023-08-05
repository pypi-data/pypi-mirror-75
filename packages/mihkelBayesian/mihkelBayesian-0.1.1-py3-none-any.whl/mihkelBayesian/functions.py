import numpy as np
from numpy import random


def rosenbrock(XY, a=1.0, b=100.0):

    '''
    Evaluates the Rosenbrock function.

    Parameters
    ----------
    XY : numpy array
        (starting_points x 2)numpy array .
    a : float
        constant a in the Rosenbrock funtion.
    b : float
        constant b in the Rosenbrock funtion.

    Returns
    -------
    Z: numpy array (1 x 1)
       Returns array with the function value evaluated at each XY point 
    '''

    x=XY[:,0]
    y=XY[:,1]
    Z=(a-x)**2+b*(y-x**2)**2
    return Z.reshape(-1,1)


def anyFunction(XY):

    '''
    Evaluates the any given function.

    Parameters
    ----------
    XY : numpy array
        (starting_points x 2)numpy array .

    Returns
    -------
    Z: numpy array
       Returns array with the function value evaluated at each XY point \.
    '''

    x=XY[:,0]
    y=XY[:,1]

    """
    Z= INSERT 2D FUNCTION HERE and delete placeholder.
    """
    Z=x+y

    return Z.reshape(-1,1)
