import numpy as np



def FluxtoCounts(v,dJdE,m,Eff=1.0,dOmega=1.0,nSpec=1.0,Tau=1.0,g=1.0):
	'''
	Convert Counts to flux
	
	Inputs
	======
	v : float
		Velocity, m/s
	dJdE : float
		particle flux
	m : float
		particle mass, kg
	
	
	'''
	
	E = 0.5*m*v**2
	return (E*Tau*g*Eff*dOmega*nSpec)*dJdE
