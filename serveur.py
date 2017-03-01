# -*- coding: utf8 -*-

import socket
import select
from outils import *
from rappel import *

class serveurAClients:




    def messageRecu(message):
        # Recupere la chaine et renvoie la réponsee
        chaine = ""
        if Outils.recupereBaliseAuto(message,"c",1) == "connexion":
            chaine = "Vous êtes bien connecté"
        if Outils.recupereBaliseAuto(message,"c",1) == "ajoutRappel":
            r = Rappel()
            r.openChaine(message)
            r.save()
            chaine = "Rappel ajouté"
        
        chaine = chaine.replace("\n","[n]")+"\n"
        return chaine

        

    def boucleInfinie(self):
        # Fonction lançant le serveur
        hote = ''
        port = 12800

        connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connexion_principale.bind((hote, port))
        connexion_principale.listen(5)
        print("Le serveur ecoute a present sur le port {}".format(port))

        serveur_lance = True
        clients_connectes = []
        while serveur_lance:
            # On va verifier que de nouveaux clients ne demandent pas à  se connecter
            # Pour cela, on écoute la connexion_principale en lecture
            # On attend maximum 50ms
            connexions_demandees, wlist, xlist = select.select([connexion_principale],[], [], 0.05)

            for connexion in connexions_demandees:
                connexion_avec_client, infos_connexion = connexion.accept()
                # On ajoute le socket connecté à  la liste des clients
                clients_connectes.append(connexion_avec_client)

            # Maintenant, on écoute la liste des clients connectés
            # Les clients renvoyés par select sont ceux devant etre lus (recv)
            # On attend là  encore 50ms maximum
            # On enferme l'appel à  select.select dans un bloc try
            # En effet, si la liste de clients connectés est vide, une exception
            # Peut etre levée
            clients_a_lire = []
            try:
                clients_a_lire, wlist, xlist = select.select(clients_connectes,[], [], 0.05)
            except select.error:
                pass
            else:
                # On parcourt la liste des clients à  lire
                for client in clients_a_lire:
                    # Client est de type socket
                    msg_recu = client.recv(1024)
                    if msg_recu.decode() != "":
                        print("Recu {}".format(msg_recu.decode()))
                        try :
                            chaine = bytes(messageRecu(msg_recu.decode()).encode('UTF-8'))
                            client.send(chaine)
                        except :
                            pass
                    if msg_recu == "fin":
                        serveur_lance = False

        print("Fermeture des connexions")
        for client in clients_connectes:
            client.close()

        connexion_principale.close()
