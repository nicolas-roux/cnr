from fonctions import *
from average_results_json import *
import numpy as np
import matplotlib.pyplot as plt
import string 
import json
import copy


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

def mse(sols):
	if len(sols) < 2:
		return 1
	# returns the mean (across all dimensions) of the squared difference to the average (for each dimension)
	vals = sols
	means = np.mean(vals, axis=0) # mean along the 0 axis, ie not per individual but per dimension
	return np.sum(np.sqrt(np.mean(np.square(np.subtract(vals, means)), axis=0))) # subtracting the mean to each vector, squaring and then meaning the result, and returning the sum







#***************Initialisationss************************

#Recuperer les valeurs depuis un fichiers json
Fichier = open('init.json')
data = json.load(Fichier)
Fichier.close()





#D est la dimension du probleme .p1 est une instance de pronlem 
d = { "sphere": sphere, "rastrigin": rastrigin }
fn = data['fonction']

p1 = Problem(d[fn] , data['dim'],-4,4)
D= p1.d



#Le nombre maximum de generations
gen_max = data['gen_max'];

#La taille de la population (nombre de vecteurs de dimension D)
NP = data['NP']


#CR  constante en [0.1] proba de croisement
CR = data['CR']

a = 0
b = 0
c = 0
F = data['F']



'''
Mutate/combiante
'''
#une matrice qui contient le vecteur du meilleur cout pour chaque generation
best_element = {}
fig, ax1 = plt.subplots()

for it in range(data["nb_iterations"]):

	#x1 est la population de depart qui contient des vecteurs D-dimentionnels
	x1 = population(NP, p1.d, p1)


	x2 = np.empty([NP,D])


	print ("iteration: {}".format(it))
	#best_gen une liste qui contient le meilleur vecteur de chaque generation
	best_gen = []
	mse_val = 1
	trial = []
	list_best =[]
	max_count = 0
	#cost contien l evaluation de la population x1
	cost = cost_pop(x1, p1.f, NP)

	count = 0
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
		best_gen.append(copy.deepcopy(x1[index_min]))

		print("Best score for generation{} is {}".format(count, minn), end="\r")	
		#print(minn, end = "\r") 
		
		
		count += 1
		mse_val = mse(x1)
		#print(mse_val)
	max_count = max(count, max_count)
	best_element[cost[-1]] = best_gen[-1].tolist()
	print(best_gen)
	nom_fichier = str(data['fonction'])+"_"+"dim"+"_"+str(data['dim'])+"_"+"F"+"_"+str(data['F'])+"_"+"CR"+"_"+str(data['CR'])+"_"+"gen"+"_"+str(data['gen_max'])+"_"+"iteration"+"_"+str(data['nb_iterations'])+".json"

	with open(nom_fichier, 'w') as file:
		#json.dump(data, file)
		#file.write("\n ")	
		json.dump(best_element, file, indent=4)
		file.write("\n")	
		
		file.close()
	list_best.append(best_gen)
	flist = [[] for i in range(max_count)]

for bglist in list_best:
	for j,bg in enumerate(bglist):
		flist[j].append(p1.f(bg))
flist2 = []
for f in flist:
	flist2.append(np.mean(f))
ax1.scatter([i for i in range(max_count)], flist2)
plt.pause(0.05)
plt.show()
moyenne(nom_fichier)