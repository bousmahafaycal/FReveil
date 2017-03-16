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
        print("messageRecu")
        chaine = "-1"
        if Outils.recupereBaliseAuto(message,"c",1) == "connexion":
            chaine = "0"

        elif Outils.recupereBaliseAuto(message,"c",1) == "ajoutRappel":
            r = Rappel()
            #print("rappel")
            if Outils.recupereBaliseAuto(argument,"Ajout",1) == "":
                r.openChaine(Outils.recupereBaliseAuto(message,"a",False))
            else:
                r.openChaine(Outils.recupereBaliseAuto(argument,"Ajout",False))
            #print("rappel2")
            reussi = r.save()
            if (reussi):
                chaine = "1" # Ajout de rappel réussi
            else :
                chaine = "2" # Ajout de rappel pas réussi


        elif Outils.recupereBaliseAuto(message,"c",1) == "modifieRappel":
            argument = Outils.recupereBaliseAuto(message,"a",1)
            r = Rappel()
            r.openChaine(Outils.recupereBaliseAuto(argument,"Ajout",1),False)
            endroit = r.getEndroit()
            #print("Pas de bras pas de choco : +"+endroit+": type ;"+str(r.typeRappel))
            if (endroit == ""):
                return self.createChaine("6") # Modification de rappel pas réussi
            nomAjout = endroit
            endroit = r.createPath(endroit)


           

            supression = Outils.recupereBaliseAuto(argument,"Suppression",1)
            l = ListeRappel(int(Outils.recupereBaliseAuto(supression,"Type",1)))

            nom = Outils.recupereBaliseAuto(supression,"ListeDateHeureAncien",1)
            for i in range(1,Outils.compter(supression,"<ListeDateHeureAncien>")):
                nom += "_"+Outils.recupereBaliseAuto(supression,"ListeDateHeureAncien",i+1)
            nom += ".f"

            if (nom != nomAjout):
                if Outils.testPresence(endroit):
                    chaine = "6"# Modification de rappel pas réussi
                if (l.delRappelFichier(nom)):
                    r.save()
                    chaine =  "5"# Modification de rappel réussie
                else:
                    chaine = "6"# Modification de rappel pas réussi
            else:
                if (l.delRappelFichier(nom)):
                    r.save()
                    chaine = "5"# Modification de rappel réussie
                else:
                    chaine = "6"# Modification de rappel pas réussi



        elif Outils.recupereBaliseAuto(message,"c",1) == "supprimeRappel":
            argument = Outils.recupereBaliseAuto(message,"a",1)
            l = ListeRappel(int(Outils.recupereBaliseAuto(argument,"Type",1)))
            reussi = l.delRappelFichier(Outils.recupereBaliseAuto(argument,"Nom",1))
            if reussi:
                chaine = "3" # Suppression de rappel réussie
            else :
                chaine = "4" # Suppression de rappel pas réussie
            
        
        elif Outils.recupereBaliseAuto(message,"c",1) == "getCommande":
            c= Config()
            liste = []
            for i in range (len(c.listeModule)):
                liste.append(c.listeModule[0])
            chaine = self.listToString(c.liste)

        elif Outils.recupereBaliseAuto(message,"c",1) == "getRappelJournalier":
            l = ListeRappel(0)
            chaine = self.listToString(l.getListe())

        elif Outils.recupereBaliseAuto(message,"c",1) == "getRappelHebdomadaire":
            l = ListeRappel(1)
            chaine = self.listToString(l.getListe())

        elif Outils.recupereBaliseAuto(message,"c",1) == "getRappelUnique":
            l = ListeRappel(2)
            chaine = self.listToString(l.getListe())

        elif Outils.recupereBaliseAuto(message,"c",1) == "getRappel":
            argument = Outils.recupereBaliseAuto(message,"a",1)
            l = ListeRappel(int(Outils.recupereBaliseAuto(argument,"Type",1)))
            r  = l.getRappelFichier(Outils.recupereBaliseAuto(argument,"Nom",1))
            chaine = r.toString()

        elif Outils.recupereBaliseAuto(message,"c",1) == "getBouton":
            c = Config()
            if c.bouton:
                chaine = "7" # Bouton appuyé
            else :
                chaine = "8" # Bouton pas appuyé

        elif Outils.recupereBaliseAuto(message,"c",1) == "getPresence":
            c = Config()
            if c.presence:
                chaine = "9" # Present
            else :
                chaine = "10" # Pas présent

        elif Outils.recupereBaliseAuto(message,"c",1) == "setBouton":
            c = Config()
            if Outils.recupereBaliseAuto(message,"a",1) == "1":
                c.setBouton(True)
            else :
                c.setBouton(False)
            chaine = "11" # setBouton terminé avec succès

        elif Outils.recupereBaliseAuto(message,"c",1) == "setPresence":
            c = Config()
            if Outils.recupereBaliseAuto(message,"a",1) == "1":
                c.setPresence(True)
            else :
                c.setPresence(False)
            chaine = "12" # setPresence terminée avec succès





        print("messageRecu2")
        
        return self.createChaine(chaine)

    def createChaine(self,chaine):
        chaine = chaine.replace("\n","[n]")
        chaine +="\n"
        return chaine

    def listToString(self,liste):
        # Fonction qui renvoie une chaine a partir d'une liste ou chaque item est dans la balise <i>
        chaine = ""
        print("createString")
        for i in range(len(liste)):
            chaine += Outils.constitueBalise("i",liste[i])
            print("liste[i]:"+liste[i])
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
