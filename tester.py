from problems import *
from solvers import *


if __name__ == "__main__":

	es1 = ES(pop_size=100, problem=SphereProblem(5))
	a = es1.problem.eval(es1.pop[0])
	print(a)