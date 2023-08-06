import numpy as np


def FluxtoPSD(v,dJdE,m):
	'''
	Convert Flux to PSD
	
	Inputs
	======
	v : float
		Speed, m/s
	dJdE : float
		Flux
	m : float
		Particl mass, kg
	
	'''
	e = 1.6022e-19
	
	return (m/v**2) * (10.0/e) * dJdE
