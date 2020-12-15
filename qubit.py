import numpy as np
from math import sqrt

#Ici on choisi 0 et 1 comme base des superpositions 
zero_qubit=np.matrix('1;0')
one_qubit=np.matrix('0;1')

#a et b amplitude (pourcentage) des etats de base
# a*zero_qubit + b*one_qubit

def createQubit(percentage_zero, percentage_one):
    if not percentage_zero+percentage_one == 100 or percentage_zero < 0 or percentage_one < 0:
        raise Exception("La somme des pourcentages en entree doit valoir 100 et chaque pourcentage doit etre positif")
    return sqrt(percentage_zero/100.)*zero_qubit+sqrt(percentage_one/100.)*one_qubit

def createDialog():
    choix = (input ("Veuillez entrer les amplitudes (ex: 50,50 ) : "))
    res = createQubit(int(choix[0]+choix[1]),int(choix[3]+choix[4]))
    print("Creation du QBit a deux etats d'amplitude : ")
    print(res)
    return res
    

    