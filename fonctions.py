import numpy as np

"""
Ces fonctions doivent renvoyer une valeur normalisée dans l'intervalle [0,1].

"""
class Problem():
	def __init__(self, f, d, low, high):
		self.f = f
		#dimensions du vecteur 		
		self.d = d
		#la plus petite valeur de lintevalle des valeurs du vecteur
		self.low = low
		#la plus grande valeur de lintevalle des valeurs du vecteur
		self.high = high

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
