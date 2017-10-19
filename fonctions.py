import numpy as np

"""
Ces fonctions doivent renvoyer une valeur normalisée dans l'intervalle [0,1].

"""

def sphere(solution):
	return np.tanh(np.sum(np.square(solution)))

