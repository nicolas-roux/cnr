import numpy as np
from problems import *


class ES():

	def __init__(self, pop_size, problem):
		self.pop = [np.zeros(problem.d) for i in range(pop_size)] # crée une liste de tableaux 1d de réels (1 réel par dimension)
		self.problem = problem

	def run(self):
		a=1