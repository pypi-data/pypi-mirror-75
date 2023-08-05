import numpy as np
from .PSDtoCounts import PSDtoCounts

k_B = 1.38064852e-23
e = 1.6022e-19


def MaxwellBoltzmannDist(n,v,T,m):
	
	vth = np.sqrt(k_B*T/m)
	f = n* (1.0/(vth*(np.sqrt(2.0*np.pi)))**3.0) * np.exp(-v**2.0/(2.0*vth**2.0))
	return f


def MaxwellBoltzmannDistCts(n,v,T,m,Eff=1.0,dOmega=1.0,nSpec=1.0,Tau=1.0,g=1.0):
	# vth = np.sqrt(k_B*T/m)
	
	# v4 = v**4
	# A = (Tau*g*dOmega*n*ProtonEff*nSpec)/(20*(vth*np.sqrt(2.0*np.pi))**3)
	# C = A*v4*np.exp(-(v**2)/(2.0*vth**2))
	# return C/1000.0
	
	f = MaxwellBoltzmannDist(n,v,T,m)
	return PSDtoCounts(v,f,m,Eff,dOmega,nSpec,Tau,g)
