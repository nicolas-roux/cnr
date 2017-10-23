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
p1 = Problem(sphere,20,-4,4)
D= p1.d


#Le nombre maximum de generations
gen_max = 100;

#La taille de la population (nombre de vecteurs de dimension D)
NP = 500;

#CR  constante en [0.1] proba de croisement
CR = 0.8

a = 0
b = 0
c = 0
F = 2

#x1 est la population de depart qui contient des vecteurs D-dimentionnels
x1 = population(NP, p1.d, p1)


x2 = np.empty([NP,D])

fig, ax1 = plt.subplots()

#cost contien l evaluation de la population x1
cost = cost_pop(x1, p1.f, NP)
'''
Mutate/combiante
'''
#une matrice qui contient le vecteur du meilleur cout pour chaque generation
best_gen = []

while (count < gen_max):
	

	for i in range(NP):
		
		#****Mutate/combiante************
		#generer a b et c tous differents de i

		while a==i:
			a = (int)(rnd_uni()*NP)

		while b==i or b==a:
			b = (int)(rnd_uni()*NP)

		while c==i or c==a or c==b:
			c = (int)(rnd_uni()*NP)

		
		#on choisit aleatoirement un point de depart de notre boucle parce qu'on fait automatiquement une mutation sur le dernier element du vecteur, ainsi il est different a chaque fois  
		j = (int)(rnd_uni()*D)
		#
		trial = [None for i in range(D)]
		

		for k in range(1,D+1):
			#rnd_uni() < CR est une condition aleatoire 
			#k == D 
			if (rnd_uni() < CR or k==D):
				trial[j] = x1[c][j] + F*(x1[a][j]-x1[b][j])
			
			else:
				trial[j]= x1[i][j]
			#
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
	#lindex de la valeur du minn dans cost
	index_min = cost.index(minn)
	#vecteur correspondant au mmin
	#print(x1[index_min])
	#np.concatenate((best_gen ,x1[index_min]))
	best_gen.append(x1[index_min])

	print("Best score for generation{} is {}".format(count, minn))	
	#print(minn, end = "\r") 
	
	ax1.scatter(count, minn)
	plt.pause(0.05)
	count += 1

print (best_gen)		
			

