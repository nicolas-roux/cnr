from fonctions import *
from pprint import pprint
import json

import numpy as np

def moyenne(f):
    nom_fichier = "moyenne"+str(f)[:-4]+"txt"
    fichier_json = open(f, 'r', encoding="utf-8")

    compteur = 0
    valeur = 0

    with fichier_json as fichier:
        data = json.load(fichier)
        #print("le fichier json")
        #print(fichier_json)
        

        for cle in data.keys():
            print(cle)
            valeur += float(cle)
            compteur += 1

    with open(nom_fichier, 'w') as file:
        
        file.write("la somme : "+str(valeur))
        file.write("\n")
        file.write("La moyenne : "+str(valeur/compteur))