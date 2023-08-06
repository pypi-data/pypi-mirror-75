import numpy as np


def CountstoFlux(v,C,m,Eff=1.0,dOmega=1.0,nSpec=1.0,Tau=1.0,g=1.0):
	'''
	Convert Counts to flux
	
	Inputs
	======
	v : float
		Velocity, m/s
	C : float
		particle counts
	m : float
		particle mass, kg
	
	
	'''
	
	E = 0.5*m*v**2
	return C/(E*Tau*g*Eff*dOmega*nSpec)
