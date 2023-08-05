import numpy as np
from .PSDtoFlux import PSDtoFlux
from .FluxtoCounts import FluxtoCounts


def PSDtoCounts(v,f,m,Eff=1.0,dOmega=1.0,nSpec=1.0,Tau=1.0,g=1.0):
	'''
	Convert PSD to counts
	
	Inputs
	======
	v : float
		Speed, m/s
	f : float
		PSD
	m : float
		Particl mass, kg
		
	
	
	'''
	dJdE = PSDtoFlux(v,f,m)
	C = FluxtoCounts(v,dJdE,m,Eff,dOmega,nSpec,Tau,g)
	return C
