import numpy as np


def PSDtoFlux(v,f,m):
	'''
	Convert Flux to PSD
	
	Inputs
	======
	v : float
		Speed, m/s
	f : float
		PSD
	m : float
		Particl mass, kg
	
	'''
	e = 1.6022e-19
	
	return ((v**2)/m) * (e/10.0) * f
