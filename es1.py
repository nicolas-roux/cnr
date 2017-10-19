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

def discrete_recomb(sols): # aka uniform crossover
	return Solution(vals=np.array([sols[np.random.randint(low=0, high=len(sols))].vals[i] for i in range(len(sols[0].vals))]), pb=sols[0].pb)

def fitness_select(sols, nbparents):
	sols.sort(key=lambda x:x.fitness)
	return sols[:nbparents]

if __name__ == "__main__":
	# n, ro, mu, lambda as in Evolution Strategies by Hansen & al., template 1
	nbdims = 5
	nbparents = 2
	popsize = 100
	nbenfants = 2

	# initializing P with the sphere function as f(x)
	pb = Problem(f=sphere, d=nbdims, low=-5, high=5)
	# set of solutions
	pop = [Solution(vals=np.random.uniform(low=pb.low, high=pb.high, size=nbdims), pb=pb) for i in range(popsize)]
	pop.sort(key=lambda x:x.fitness)
		
	# Endogenous parameters. In this implementation, a single step size is chosen.
	params = np.random.uniform(low=-1, high=1, size=1)

	
	fig, ax1 = plt.subplots()
		
	it = 0
	snapshot = 1

	while it < 1000000000:
		if it % snapshot == 0:
			ax1.scatter(it, pop[0].fitness, label="fitness", color="blue")
			plt.pause(0.05)	
		offspring = None

		for i in range(nbenfants):
			# parent selection
			parents = fitness_select(pop,nbparents)
			# recombination
			offspring = discrete_recomb(parents)
			# Mutation: to each value is added step_size * (normal_distribution(mu=0,sigma=1))
			np.add(offspring.vals, np.multiply(params,np.random.normal()), out=offspring.vals)
			offspring.fitness = pb.f(offspring.vals)
			# adjusting endogenous parameters
			if offspring.fitness < np.mean([p.fitness for p in parents]):
				np.multiply(params, 1.5, out=params)
			else:
				np.multiply(params, 0.9, out=params)

			# inserting offspring into pop
			pop.append(offspring)



		pop.sort(key=lambda x:x.fitness)
		# downsizing population to [popsize]
		pop = pop[:popsize]
		print(str(it) + " " + str(pop[0].fitness), end = "\r")
		it += 1
