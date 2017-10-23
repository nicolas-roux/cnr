from problems import *
from fonctions import *
import numpy as np
import matplotlib.pyplot as plt


'''Les fonctions'''

#la fonction rnd_uni genere un nombre aleatoire uniformement reparti dans lintervalle[0,1]
def rnd_uni():
	return np.random.uniform()


def population(pop_size, d, pb):
	pop = []
	for i in range(pop_size):
		pop.append(np.random.uniform(low=1.,high=2.,size=d))
	return pop


def cost_pop(x, function, NP):
	cost = []
	for s in x:
		#print(s)
		cost.append(function(s))

	return cost







#***************Initialisationss************************
count = 0
trial = []
#D est la dimension du probleme .p1 est une instance de pronlem 
p1 = Problem(sphere,5,-4,4)
D= p1.d


#Le nombre maximum de generations
gen_max = 10000;

#La taille de la population (nombre de vecteurs de dimension D)
NP = 100;

#CR  constante en [0.1] proba de croisement
CR = 0.9

a = 0
b = 0
c = 0
F = 1

x1 = population(NP, p1.d, p1)


x2 = np.empty([NP,D])

fig, ax1 = plt.subplots()

cost = cost_pop(x1, p1.f, NP)
'''
Mutate/combiante
'''

while (count < gen_max):
	

	for i in range(NP):
		
		#****Mutate/combiante************
		

		while a==i:
			a = (int)(rnd_uni()*NP)

		while b==i or b==a:
			b = (int)(rnd_uni()*NP)

		while c==i or c==a or c==b:
			c = (int)(rnd_uni()*NP)

		j = (int)(rnd_uni()*D)
		trial = [None for i in range(D)]
		for k in range(1,D+1):

			if (rnd_uni() < CR or k==D):
				trial[j] = x1[c][j] + F*(x1[a][j]-x1[b][j])
			
			else:
				trial[j]= x1[i][j]
			j = (j+1) % D


		#****evaluate/select************
		#evaluer le vecteur resultat trail
		score = p1.f(trial)
		
		
		if (score <= cost[i]) :

			for j in range(D):
				x2[i][j] = trial[j]
				
			cost[i] = score
		

		else:

			for j in range(D):
				x2[i][j] = x1[i][j]
		#print(cost)
	#**********************end of pupulation loop swap arrays

	for i in range(NP):
		for j in range(D):
			x1[i][j] = x2[i][j]
	

	cost = cost_pop(x1, p1.f, NP)
	#la valeur min a chaque generation
	minn = min(cost)	
	print(minn, end = "\r") 
	
	#ax1.scatter(count, minn)
	#plt.pause(0.05)
	count += 1

			
			

