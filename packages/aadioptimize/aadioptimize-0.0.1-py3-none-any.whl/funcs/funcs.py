import numpy as np


def rosenbrock(X):
	x = X[0]
	y = X[1]
	f = ((1-x)**2 + 100*(y-x**2)**2)
	return f




def kenny(X):
	x=X[0]
	y=X[1]
	F = np.sin(x+y) +(x-y)**2-(1.5*x)+(2.5*y)+1
	return F