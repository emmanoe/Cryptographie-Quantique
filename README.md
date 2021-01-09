# Cryptographie-Quantique

## Mise en œuvre d’une simulation de l’algorithme BB84 et de son utilisation.

Dans ce dossier vous trouverez un fichier main.py qui permet de lancer un serveur de transmission de QBit en local et également d'y connecter plusieurs clients.

### Lancement

1 - Lancer un terminal depuis le dossier Cryptographie-Quantique puis en ligne de commande, demarrer le serveur:
>$ ./main.py

2 - Dans deux autres terminaux on va connecter les clients au serveur créé. Pour cela, faites la même chose qu'à l'étape 1 sauf que cette fois ci on va ajouter l'adresse du serveur en paramêtre de notre excutable:
>$ ./main.py :: #pour se connecter au serveur local

3 - Il vous sera demandé si vous voulez jouer en réseau, répondre O (oui) ou N (non) à l'aide des touches de votre clavier.

### Fonctionnalités
- Création de QBit
- Transmission de QBits entre deux machines du réseau local
- Mesure de l'état reçu (base: |0>, |1>)
