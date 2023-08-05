import numpy as np
from numpy import random
import matplotlib.pyplot as plt
from mihkelBayesian import bayesianFunctions as bf, functions as fu
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import ConstantKernel as C, Matern



def runRosenbrock(a,b, boundaries=np.array([[-100.0, 100.0],[-100.0,100.0]])):

    '''
    Runs the Bayesian optimiser

    Parameters
    ----------
    a : float
        Rosenbrock constant a
    b : float
        Rosenbrock constant b
    boundaries: numpy array (2 x 2)
        Boundaries of the searchspace in the form of [[xmin,xmax],[ymin,ymax]]

    Returns
    -------
    min_val: float
        Smallest evaluation.
    min_point: numpy array (1 x 2)
        Point correspoinding to the smallest evaluation
    '''

    """
    -------------
    Hyperparameters of the optimiser
    ------------
    """

    #Bounds within which the optimiser is searching for the answer
    bounds = boundaries
    #Number of iterations
    n_iterations=20
    #Exploitation-exploration trade-off parameter
    exploration=0.1
    #Number of random points considered for expected improvement
    samplePoints=10000
    #Number of random measurements done before applying Bayesian optimisation
    no_startingPoints=10
    #Number of evaluation before applying restricted boundries
    tavalist=10
    suurem=10000

    #Generating startingpoints

    X=np.random.uniform(bounds[0,0], bounds[0,1], [no_startingPoints,1])
    Y=np.random.uniform(bounds[1,0], bounds[1,1], [no_startingPoints,1])
    XY=np.column_stack((X,Y))
    Z=fu.rosenbrock(XY,a,b)


    #Which Gaussian model
    customKernel=C(1.0) * Matern()
    model = GaussianProcessRegressor(kernel=customKernel)


    for i in range(n_iterations):
        #print iteration
        print("Iteration " + str(i) + "/"+str(n_iterations))

        # Update Gaussian process with existing samples
        model.fit(XY, Z)

        # Obtain next sampling point from the acquisition function (expected_improvement)
        XY_next = bf.propose_location(bf.expected_improvement, XY, Z, model, bounds, samplePoints, tavalist,suurem, no_startingPoints,exploration)
        
        # Obtain next sample from the objective function
        Z_next = fu.rosenbrock(XY_next,a,b)
        
        #Changes kernel for very small values

        if Z_next>10:
            model = GaussianProcessRegressor(kernel=customKernel)
        else:
            model= GaussianProcessRegressor()
        
        # Add sample to previous samples
        XY = np.vstack((XY, XY_next))
        Z = np.vstack((Z, Z_next))


    minindex=np.argmin(Z)  
    min_val=Z[minindex]
    min_point=XY[minindex]  

    return min_val, min_point

