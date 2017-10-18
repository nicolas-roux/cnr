import numpy as np

class Problem():
	def __init__(self, f, d, low, high):
		self.f = f
		//dimensions du vecteur 		
		self.d = d
		//la plus petite valeur de lintevalle des valeurs du vecteur
		self.low = low
		//la plus grande valeur de lintevalle des valeurs du vecteur
		self.high = high

	
