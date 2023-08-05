import numpy as np
from scipy.stats import norm
import sklearn



#Expected improvementi arvutamine
def expected_improvement(sample, XY, Z, model, exploration):
    
    '''
    Computes the EI at points X based on existing samples XY
    and Z using a Gaussian process surrogate model.
    
    Args:
        sample: Points at which EI shall be computed (m x d).
        XY: Sample locations (n x d).
        Z: Sample values (n x 1).
        model: A GaussianProcessRegressor fitted to samples.
        exlporation: Exploitation-exploration trade-off parameter.
    
    Returns:
        Expected improvements at points "sample".
    '''
    mu, sigma = model.predict(sample, return_std=True)
   
    #reshapin sigma ja liidan vaikese arvu, et edasistes arvutustes ei oleks 0-ga jagamist
    sigma = sigma.reshape(-1, 1) + 10**(-8)
    #print(np.column_stack((mu,sigma)))
    mu_sample_opt = np.min(model.predict(XY))

    with np.errstate(divide='warn'):
        imp = mu - mu_sample_opt - exploration
        Z = imp / sigma
        
        Z=sklearn.preprocessing.scale(Z)
        
        ei = imp * norm.cdf(Z) + sigma * norm.pdf(Z)
        #ei[sigma < 10**-7] = 0.0
            

        return ei 


def calculate_boundaries(XY, Z, model, bounds, samplePoints, tavalist, suurem, no_startingPoints, dimensions):

    if len(Z) > tavalist+no_startingPoints:

        index=np.argmin(Z)
        xzero=xplus=xmin=XY[index,0]
        yzero=yplus=ymin=XY[index,1]

        while abs(model.predict(np.array([xplus,yzero]).reshape(1,2))) < (np.min(Z)*suurem) and xplus<bounds[0,1]:
            xplus=xplus+abs(bounds[0,1])/len(Z)
            
            
        while abs(model.predict(np.array([xmin,yzero]).reshape(1,2))) < (np.min(Z)*suurem)  and xmin>bounds[0,0]:
            xmin=xmin-abs(bounds[0,0])/len(Z)
            
        while abs(model.predict(np.array([xzero,yplus]).reshape(1,2))) < (np.min(Z)*suurem)  and yplus<bounds[1,1]:
            yplus=yplus+abs(bounds[1,1])/len(Z)
            
        while abs(model.predict(np.array([xzero,ymin]).reshape(1,2))) < (np.min(Z)*suurem)  and ymin>bounds[1,0]:
            ymin=ymin-abs(bounds[1,0])/len(Z)
        

        # Find the best optimum by starting from samplePoints different random points
        xrandomPoints=np.random.uniform(xmin, xplus, [samplePoints,1])
        yrandomPoints=np.random.uniform(ymin, yplus, [samplePoints,1])
        randomPoints=np.column_stack((xrandomPoints,yrandomPoints))

    else:
    
        xrandomPoints=np.random.uniform(bounds[0,0], bounds[0,1], [samplePoints,1])
        yrandomPoints=np.random.uniform(bounds[1,0], bounds[1,1], [samplePoints,1])
        randomPoints=np.column_stack((xrandomPoints,yrandomPoints))

    return randomPoints


def propose_location(acquisition, XY, Z, model, bounds, samplePoints, tavalist, suurem, no_startingPoints,exploration):
    
    '''
    Proposes the next sampling point by optimizing the acquisition function.
    
    Args:
        acquisition: Acquisition function.
        XY: Sample locations (n x d).
        Z: Sample values (n x 1).
        model: A GaussianProcessRegressor fitted to samples.

    Returns:
        Location of the acquisition function maximum.
    '''
    dimensions = XY.shape[1]
    min_val = 1000000000000000000000000
    min_x=None

    randomPoints=calculate_boundaries(XY, Z, model, bounds, samplePoints, tavalist, suurem, no_startingPoints, dimensions)
    
    EI=acquisition(randomPoints.reshape(len(randomPoints), dimensions), XY, Z, model ,exploration)
    

    min_index=np.argmin(EI)
    min_val=EI[min_index,0]
    min_x=np.array([randomPoints[min_index]])
            

    return min_x