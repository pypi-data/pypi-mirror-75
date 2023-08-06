import mihkelBayesian.functions as fu
import pytest
import numpy as np 


def test_rosenbrock():

	startingPoint=np.array([[3,9]])

	answer1=fu.rosenbrock(startingPoint, [3,100])
	assert answer1==0.0

	answer2=fu.rosenbrock(startingPoint, [2, 10])
	assert answer2==1.0

	startingpoint=np.array([[4,12]])
	answer3=fu.rosenbrock(startingPoint, [3, 100])
	assert answer3== pytest.approx(1601, 1)