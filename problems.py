import numpy as np

class SphereProblem():
	def __init__(self, d):
		super().__init__()
		self.d = d

	def eval(self, solution):
		return np.sum(np.square(solution))
