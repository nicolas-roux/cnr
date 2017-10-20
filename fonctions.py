import numpy as np

"""
Ces fonctions doivent renvoyer une valeur normalisée dans l'intervalle [0,1].

"""

def sphere(vals):
	return np.sum(np.square(vals))

def ellipsoid(vals):
	f = 0.0
	denom = len(vals) - 1
	for i, x in enumerate(vals):
		f += np.multiply(np.power(10, np.divide(i-1,denom)), np.square(x))
	return f

def rastrigin(vals):
	return np.add(np.multiply(10,len(vals)), np.sum(np.subtract(np.square(vals), np.multiply(10, np.cos(np.multiply(np.multiply(2, np.pi), vals))))))
	