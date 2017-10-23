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

def intermediate_recomb(sols):
	return Solution(vals=np.mean(np.array([s.vals for s in sols]), axis=0), pb=sols[0].pb)

def weighted_recomb(sols):
	# dur dur! https://ac.els-cdn.com/S0304397506003008/1-s2.0-S0304397506003008-main.pdf?_tid=b9c3a934-b7cc-11e7-9dcf-00000aacb360&acdnat=1508747737_0beb20243cdef85bfa55cb3aeebbb129
	# solution bâtarde: w_k = 1/(2**k), acceptable quand k devient grand (>> 10)
	a = np.array([s.vals for s in sols])

def fitness_select(sols, nbparents):
	sols.sort(key=lambda x:x.fitness)
	return sols[:nbparents]

if __name__ == "__main__":
	# n, ro, mu, lambda as in Evolution Strategies by Hansen & al., template 1
	nbdims = 20
	nbparents = 1
	popsize = 1
	nbenfants = 1

	nbparams = nbdims # either 1 or n


	# initializing P with the sphere function as f(x)
	pb = Problem(f=ellipsoid, d=nbdims, low=-5.12, high=5.12)
	# set of solutions
	pop = [Solution(vals=np.random.uniform(low=pb.low, high=pb.high, size=nbdims), pb=pb) for i in range(popsize)]
	pop.sort(key=lambda x:x.fitness)
	
	""" FOR TEST PURPOSES
	ts1 = Solution(vals=np.array([0.,1.,3]),pb=pb)
	ts2 = Solution(vals=np.array([2,3,1]),pb=pb)
	ts3 = Solution(vals=np.array([1,2,2]),pb=pb)
	ts4= intermediate_recomb([ts1,ts2,ts3])
	print(ts4.vals)
	sys.exit(1)
	"""

	# Endogenous parameters.
	"""
	neg = np.random.uniform(low=-1, high=-np.power(10.,-5), size=nbparams)
	pos = np.random.uniform(low=np.power(10.,-5), high=1, size=nbparams)
	params = np.array([neg[i] if np.random.uniform() < 0.5 else pos[i] for i in range(nbparams)])
	"""
	params = np.array([2. for i in range(nbparams)])
	#params = np.array([2.])
	fig, ax1 = plt.subplots()
	
	it = 0
	stopsigma = np.power(10.,-10)
	degrade = np.power(1.5, -1/4)
	max_it = 100000 * nbdims
	best = 10000000
	git, restarts = 0, 0
	while True:
		if it > max_it or np.mean(params) < stopsigma:
			pop = [Solution(vals=np.random.uniform(low=pb.low, high=pb.high, size=nbdims), pb=pb) for i in range(popsize)]
			pop.sort(key=lambda x:x.fitness)
			params = np.array([2. for i in range(nbdims)])
			git += it
			it = 0
			restarts += 1
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
		if pop[0].fitness < best:
			best = pop[0].fitness
			ax1.scatter(git+it, pop[0].fitness, label="fitness", color="blue")
			plt.pause(0.05)	
		if it % 100 == 0:
			print("restarts: " +str(restarts) + ", it=" + str(git + it) + ", best=" + str(best) + ", sigma=" + str(params[0]), end = "    \r")
			
		it += 1
	print()