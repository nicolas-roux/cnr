from problems import *
from fonctions import *
import sys
import matplotlib.pyplot as plt


class Solution():
	def __init__(self, vals, pb):
		self.age = 0
		self.vals = vals
		self.fitness = pb.f(self.vals)
		self.pb = pb

	def eval(self):
		self.fitness = pb.f(self.vals)

def discrete_recomb(sols): # aka uniform crossover
	return Solution(vals=np.array([sols[np.random.randint(low=0, high=len(sols))].vals[i] for i in range(len(sols[0].vals))]), pb=sols[0].pb)

def fitness_select(sols, nbparents):
	sols.sort(key=lambda x:x.fitness)
	return sols[:nbparents]

if __name__ == "__main__":
	# n, ro, mu, lambda as in Evolution Strategies by Hansen & al., template 1
	nbdims = 5
	nbparents = 1
	popsize = 1
	nbenfants = 1


	# initializing P with the sphere function as f(x)
	pb = Problem(f=sphere, d=nbdims, low=-5.12, high=5.12)
	# set of solutions
	pop = [Solution(vals=np.random.uniform(low=pb.low, high=pb.high, size=nbdims), pb=pb) for i in range(popsize)]
	pop.sort(key=lambda x:x.fitness)
	# Endogenous parameters.
	nbparams = 1
	"""
	neg = np.random.uniform(low=-1, high=-np.power(10.,-5), size=nbparams)
	pos = np.random.uniform(low=np.power(10.,-5), high=1, size=nbparams)
	params = np.array([neg[i] if np.random.uniform() < 0.5 else pos[i] for i in range(nbparams)])
	"""
	params = np.array([2. for i in range(nbdims)])

	fig, ax1 = plt.subplots()
	
	it = 0
	snapshot = 1
	stopsigma = np.power(10.,-12)
	degrade = np.power(1.5, -1/4)
	while it < 10000000 and np.mean(params) > stopsigma:
		if it % snapshot == 0:
			ax1.scatter(it, pop[0].fitness, label="fitness", color="blue")
			plt.pause(0.05)	
			a=1
		offspring = None

		for i in range(nbenfants):
			# parent selection
			parents = fitness_select(pop,nbparents)
			# recombination
			offspring = discrete_recomb(parents)
			# Mutation: to each value is added step_size * (normal_distribution(mu=0,sigma=1))
			offspring.vals = np.add(offspring.vals, np.multiply(params,np.random.normal(size=nbdims)))
			offspring.eval()
			# adjusting endogenous parameters
			if offspring.fitness <= np.mean([p.fitness for p in parents]):
				np.multiply(params, 1.5, out=params)
			else:
				np.multiply(params, degrade, out=params)
			# inserting offspring into pop
			pop.append(offspring)

		pop.sort(key=lambda x:x.fitness)
		# downsizing population to [popsize]
		pop = pop[:popsize]
		print("it " + str(it) + ", best=" + str(pop[0].fitness) + ", sigma=" + str(params[0]), end = "\r")
		it += 1
	print()