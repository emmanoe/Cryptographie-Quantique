#!/usr/bin/python3

from qubit import *
import  random
import time
import socket
import select
import sys

U0 = 0 #Client 0
U1 = 1 #Client 1

#Fonction de reception d'un QBit 
def receiveQBit(client):
    boats = []
    x = int(client.recv(1)) + 1
    print("coucou QBit x")

def main_client(x):
    choix = (input ("Voulez vous vous connecter au tunnel de transmission de QBit <N>on <O>ui ?"))
    if (choix.upper()[0] != 'O'):
    	return
    #Création de la socket TCP/IP
    client = socket.socket(family = socket.AF_INET6, type = socket.SOCK_STREAM, proto = 0, fileno = None)

    #On connecte la nouvelle socket client au port où le server "écoute"
    server = (x,7777)
    print("Connection au tunnel distant sur le port 7777")
    client.connect(server)
    print("Vous êtes connecté au tunnel de transmission")
    print("Attente de client ...")

    User_Number = client.recv(1)

    if (int(User_Number) >= 2):
        print("Dernier connecté vous observerez la transmission de QBit")
        return

    print("Client trouvé")
    
    print("======================")

    
    print("Votre id client est %d" % int(User_Number))
    
    #Ouverture du dialog de création d'un QBit 
    if (int(User_Number) == 0):
        print("Voulez vous: ")
        print("<1> - Transmettre un QBit ? ")
        choixApp = (input ("<2> - Transmettre une série de QBits (random) ? "))
        
        if (choixApp == "1"):
            alpha,beta = createQBit()
            payload = str(alpha).encode()+b' '
            client.send(payload)
            print("QBit transmitted to user 1")

        if (choixApp == "2"):
            state = ''
            size = int((input("Taille de la série :")))
            print("- Base |0>, |1> -")
            for _ in range(size):
                state += str(random.randint(0,1))
            payload = state.encode()
            client.send(payload)
            print("Bits envoyés: "+state)
            pass

    else :
        print("Bit entrant: ")
        byte_list = b''
        while True:
            c = client.recv(1)
            print(c)
            if c == b'':
                break
            byte_list+=c
        alpha = int(byte_list)
        
        print("QBit transmit par user 0: ")

        #Convertissage des bytes en int
        try:
            print("Mesure de l'état reçu dans la base |0>, |1>:")
            beta = 100 - alpha
            qbit = sqrt(alpha/100.) * zero_qubit + sqrt(beta/100.) * one_qubit
            print(measure_in_01_basis(qbit)) 
        except ValueError:

            print(measure_in_01_basis(create_quantum_state(str(alpha))))
        

            
def main():

    if len(sys.argv) >1:
        main_client(sys.argv[1])
        return
    
    #création de socket TCP
    server = socket.socket(family = socket.AF_INET6, type = socket.SOCK_STREAM, proto = 0, fileno = None)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #Bind la socket au port 7777
    print("Lancement du tunnel de transmission de QBit sur le port 7777")
    server.bind(('::',7777))
    # "Ecoute" pour les demandes de connections entrantes
    server.listen(5)

 
    #Attente de connexion
    clients_connectes = []
    
    print("Attente de connexion..")
    while True:
        # Attente d'une connexion
        #On récupère les sockets disponibles en lecture
        
        
        connexions_demandees, wlist, xlist = select.select([server],[], [])
        print("1 client s'est connecté")
        for connexion in connexions_demandees:
            connexion_avec_client, infos_connexion = connexion.accept()
            # On ajoute la socket connecté à la liste des clients
            clients_connectes.append(connexion_avec_client)

        #Les 2 premiers clients connectés sont les interlocuteurs on leur renvoit les infos et leur id client
        if (len(clients_connectes) == 2):
            print("2 clients connectés" )

            print("Chargement ...")    
            print("Attente d'éventuel observateurs")
            timeout = 1
            connexions_demandees, wlist, xlist = select.select([server],[], [],timeout)
            for connexion in connexions_demandees:
                connexion_avec_client, infos_connexion = connexion.accept()
                # On ajoute la socket connecté à la liste des clients
                clients_connectes.append(connexion_avec_client)

            print("time out:")    
            print("%d observateur(s) connecté(s)" % (len(clients_connectes) - 2))
            print("Chargement terminé")

            id = 0
            for i in range (len(clients_connectes)):
                clients_connectes[i].sendall(str(id).encode('utf-8'))
                id += 1                        
            
            #Pour commencer on defini le client du serveur à 0 
            currentUser = 0
            
            if (currentUser == U0):
                x = b''
                for i in range(8):
                    x = x + clients_connectes[0].recv(1)
                clients_connectes[1].sendall(x)
            
            print("QBit sent from user 0 to user 1 !")
            break
    #Fin de la transmission et fermeture des connexions
    for client in clients_connectes:
        client.close()
    server.close()

            
    
main()
