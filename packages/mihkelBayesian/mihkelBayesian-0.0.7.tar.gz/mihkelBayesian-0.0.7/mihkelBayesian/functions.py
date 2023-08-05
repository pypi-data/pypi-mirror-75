import numpy as np
from numpy import random

#takes a 2D array and outputs 1D answer
def rosenbrock(XY, a=1,b=100):
    x=XY[:,0]
    y=XY[:,1]
    Z=(a-x)**2+b*(y-x**2)**2
    return Z.reshape(-1,1)

def sphere(XY, a=1,b=100):
    x=XY[:,0]
    y=XY[:,1]
    Z=a*x**2+b*y**2
    return Z.reshape(-1,1)


def XDfunction(XD):
	D = XD.shape[1]
	Z=1
	for i in range(D):
		xi=XD[:,i]
		Z=Z+xi**2
	return Z

