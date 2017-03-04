# -*- coding: utf8 -*-

import socket
import select
from outils import *
from rappel import *
from config import *
from liste_rappel import *

class Serveur:

    def messageRecu(self,message):
        # Recupere la chaine et renvoie la réponsee
        #print("messageRecu")
        chaine = ""
        if Outils.recupereBaliseAuto(message,"c",1) == "connexion":
            chaine = "0"
        elif Outils.recupereBaliseAuto(message,"c",1) == "ajoutRappel":
            r = Rappel()
            #print("rappel")
            r.openChaine(Outils.recupereBaliseAuto(message,"a",1))
            #print("rappel2")
            reussi = r.save()
            if (reussi)
                chaine = "1" # Ajout de rappel réussi
            else 
                chaine = "2" # Ajout de rappel pas réussi
        
        elif Outils.recupereBaliseAuto(message,"c",1) == "getCommande":
            c= Config()
            chaine = listToString(c.listeModule)

        elif Outils.recupereBaliseAuto(message,"c",1) == "getRappelUnique":

        #print("messageRecu2")
        chaine = chaine.replace("\n","[n]")
        chaine +="\n"
        return chaine


    def listToString(liste):
        # Fonction qui renvoie une chaine a partir d'une liste ou chaque item est dans la balise <i>
        chaine = ""
        for i in range(len(liste)):
            chaine += Outils.constitueBalise("i",chaine)
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
                            chaine = self.messageRecu(msg_recu.decode())
                            print("chaine:"+chaine)
                            chaine = bytes(chaine.encode('UTF-8'))
                            client.send(chaine)
                        except :
                            pass
                    if msg_recu == "fin":
                        serveur_lance = False

        print("Fermeture des connexions")
        for client in clients_connectes:
            client.close()

        connexion_principale.close()
