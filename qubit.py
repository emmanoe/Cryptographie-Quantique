import numpy as np
from math import sqrt, log
from random import random 
import itertools

#Functions fortement inspiré de "Mastering Quantum Computing with IBM QX: Explore the world of quantum"

#Ici on choisi |0> et |1> comme base 
zero_qubit=np.matrix('1;0')
one_qubit=np.matrix('0;1')

#a et b amplitude (pourcentage) des etats de base
# a*zero_qubit + b*one_qubit

# Superposition des deux QBits de base |0> et |1>
def createQubit(percentage_zero, percentage_one):
    if not percentage_zero+percentage_one == 100 or percentage_zero < 0 or percentage_one < 0:
        raise Exception("La somme des pourcentages en entree doit valoir 100 et chaque pourcentage doit etre positif")
    return sqrt(percentage_zero/100.)*zero_qubit+sqrt(percentage_one/100.)*one_qubit

def createQBit():
    print ("Veuillez entrer les amplitudes en pourcent (ex alpha: 50, beta: 50 ) : ")
    alpha = int(input ("Pourcentage du bit 0: "))
    beta = int(input ("Pourcentage du bit 1: "))
    res = createQubit(alpha,beta)
    print("Creation du QBit [[racine-carree(alpha)|0>][racine-carree(beta)|1>]] : ")
    print(res)
    return alpha, beta

def measure_in_01_basis(state):
    n_qubits=int(log(state.shape[0],2))
    probabilities = [(coeff*coeff.conjugate()).real for coeff in state.flat]
    rand=random()
    """ print("Going with rand : ",rand)
    print("Going with probabilities : ",probabilities) """
    for idx,state_desc in enumerate([''.join(map(str,state_desc))
        for state_desc in itertools.product([0,1], repeat=n_qubits)]): 
            if rand < sum(probabilities[0:(idx+1)]):
                return '|"%s">' % state_desc 
   
