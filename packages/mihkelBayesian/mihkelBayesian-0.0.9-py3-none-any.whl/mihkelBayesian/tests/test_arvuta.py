from mihkelBayesian import arvutamine
import pytest


def test_liitmine():

	vastus1=arvutamine.liida(2,3)
	assert vastus1==5

	vastus2 = arvutamine.lahuta(4,2)
	assert vastus2==2



