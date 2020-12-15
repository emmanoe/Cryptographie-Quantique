#!/usr/bin/python3

from qubit import createDialog
import  random
import time
import socket
import select
import sys

U0 = 0 #Client 0
U1 = 1 #Client 1

def main_client(x):
    choix = (input ("Voulez vous vous connecter au serveur de transmission de QBit <N>on <O>ui ?"))
    if (choix == 'N'):
    	return
    #Création de la socket TCP/IP
    client = socket.socket(family = socket.AF_INET6, type = socket.SOCK_STREAM, proto = 0, fileno = None)

    #On connecte la nouvelle socket client au port où le server "écoute"
    server_address = (x,7777)
    print("Connection au server distant sur le port 7777")
    client.connect(server_address)
    print("Vous êtes connecté au serveur de transmission")
    print("Attente de client ...")

    User_Number = client.recv(1)

    if (int(User_Number) >= 2):
        print("Dernier connecté vous observerez la transmission de QBit")
        return

    print("Client trouvé")
    
    print("======================")

    
    print("Votre id client est %d" % int(User_Number))

    #Ouverture du dialog de création d'un QBit 
    if int(User_Number) == U0:
        x_char = input ("quelle colonne ? ")
        x_char.capitalize()
        x = ord(x_char)-ord("A")  + 1
        y = int(input ("quelle ligne ? "))  
        client.send(str(x-1).encode('utf-8'))
        client.send(str(y-1).encode('utf-8'))


    #Ouverture du dialog de récéption d'un QBit 
    if int(User_Number) == U1:
        print("Atente de reception ...")
        x = client.recv(1) 
        y = client.recv(1) 
            
def main():

    if len(sys.argv) >1:
        main_client(sys.argv[1])
        return
    
    #création de socket TCP
    server = socket.socket(family = socket.AF_INET6, type = socket.SOCK_STREAM, proto = 0, fileno = None)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #Bind la socket au port 7777
    print("Lancement du serveur de transmission de QBit sur le port 7777")
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
            timeout = 8
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
            

    #Fin de la transmission et fermeture des connexions
    for client in clients_connectes:
        client.close()
    server.close()

            
    
main()