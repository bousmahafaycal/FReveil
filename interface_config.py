from outils import *
from config import *
import os
from time import *

class InterfaceConfig:
	# interface console permettant de gérer la configuration du FReveil
	def __init__(self):
		self.conf = Config()
		self.annonce()
		self.menuPrincipal()


	def lireConfig(self):
		# Fonction permettant d'actualiser la config du réveil.
		# Dans la config, on met l'endroit ou les modules sont stockés, le nom de tous les modules, l'endroit ou les réveils sont stockés (chaque type)
		self.conf.openConfig()


	def annonce(self):
		# Annonce et crédit du programme
		print("Bienvenue dans l'interface de configuration du FReveil.")
		print("Ce programme a été crée par Fayçal Bousmaha.")
		print()
		print()

	def menuPrincipal(self):
		# Menu principal de cette interface
		print()
		liste = ["Quitter","Gestion des modules","Gestion de la présence","Gestion de l'appui sur le bouton"]
		a = Outils.menu("MENU PRINCIPAL",liste)
		print()
		if a == 1:
			self.menuModule()
		elif a == 2:
			self.gestionPresence()
		elif a == 3:
			self.gestionBouton()


	def menuModule(self):
		# Menu pour la gestion des modules
		print()
		liste = ["Revenir au menu principal","Voir tous les modules","Ajouter un module","Supprimer un module"]
		a = Outils.menu("GESTION DES MODULES",liste)
		print()
		if a == 0:
			self.menuPrincipal()
		elif a == 1:
			self.seeModule()
		elif a == 2:
			self.addModule()
		elif a == 3 :
			self.delModule()


	def seeModule(self):
		# Voir une liste des modules
		self.lireConfig()
		print("Voici la liste des modules actuellement disponible : ")
		for i in range(0,len(self.conf.listeModule)):
			print(str(i+1)+" - "+self.conf.listeModule[i][0])
		print()
		input("Appuyez sur entrée pour retourner à la gestion des modules.")
		print()
		self.menuModule()
	
	def addModule(self):
		# Ajouter un module
		print()
		print("Ajouter un module")
		print("-----------------")
		continuer = True
		menu = False
		endroit = ""
		while continuer:
			endroit = input("Merci de donner le chemin (relatif ou absolu) du dossier du module que vous souhaitez ajouter (tapez MENU pour revenir au menu precedent) : ")
			if (Outils.testPresenceRep(endroit)):
				continuer = False
			elif endroit == "MENU":
				menu = True
				continuer = False
			else:
				print()
				print("Chemin incorrect, merci de donner un chemin correct vers le dossier du module.")

		if menu :
			print()
			self.menuModule()

		else :
			
			if self.verificationModule(endroit): 
				self.conf.addModule(self.getNomModule(endroit),endroit) # ATTENTION : il faut gerer le cas ou le nom du module existe déja
				print("Le module a été ajouté avec succès")
				sleep(3)

			else:
				print()
				print("Ce module n'a pas été crée par l'outil dédié. Merci de bien vouloir utiliser l'outils de création de module dédié au FReveil.")
			print()
			self.menuModule()

	def verificationModule(self,endroit):
		# A partir du dossier, verifie que le module est reellement fonctionnel
		if endroit[len(endroit)-1] != os.sep:
			endroit += os.sep
		endroit += "configModule.f"
		if not Outils.testPresence(endroit):
			return False

		chaine = Outils.lireFichier(endroit)
		if (Outils.compter(chaine,"<Nom>") < 1):
			return False

		# VERIFICATION QUE LA FOCNTION START EXISTE A FAIRE	ULTERIEUREMENT

		return True

	def getNomModule(self,endroit):
		# Recupere le nom du module a partir du chemin du dossier
		if endroit[len(endroit)-1] != os.sep:
			endroit += os.sep
		endroit += "configModule.f"
		chaine = Outils.lireFichier(endroit)
		nom = Outils.recupereBaliseAuto(chaine,"Nom",1)
		return nom


	def delModule(self):
		# Supprimer un module
		print()
		liste = []
		liste.append("Revenir à la gestion des modules")
		for i in range(0,len(self.conf.listeModule)):
			liste.append(self.conf.listeModule[i][0])
		a = Outils.menu("Choisissez le module à supprimer : ",liste)
		if a == 0:
			self.menuModule()
		else:
			self.conf.delModule(a-1)
			print("Le module a été supprimé avec succès")
			sleep(3)
			print()
			self.menuModule()

		
 
	def gestionPresence(self):
		# Va donner la précédente valeur de présence et offrir le choix à l'utilisateur de le changer
		self.lireConfig()
		print()
		print("--------------------------------------------------------")
		if (self.conf.presence ):
			print("Etat de votre présence : PRESENT")
		else:
			print("Etat de votre présence : ABSENT")
		print()
		liste = ["Revenir au menu principal","Passer en mode présent","Passer en mode absent"]
		a = Outils.menu("GESTION DE LA PRESENCE",liste, False)
		print("--------------------------------------------------------")
		if a == 0:
			self.menuPrincipal()
		elif a == 1:
			self.conf.setPresence(True)
			print()
			print()
			self.gestionPresence()
		elif a == 2:
			self.conf.setPresence(False)
			print()
			print()
			self.gestionPresence()

	def gestionBouton(self):
		# Va donner la precedente valeur de bouton  et offrir le choix à l'utilisateur de simuler l'appui sur le bouton
		self.lireConfig()
		print()
		print("--------------------------------------------------------")
		if (self.conf.bouton ):
			print("Etat bouton : Appuyé")
		else:
			print("Etat bouton : Non appuyé")
		print()
		liste = ["Revenir au menu principal","Appuyer sur le bouton","Passer en mode non appuyé"]
		a = Outils.menu("GESTION DU BOUTON",liste, False)
		print("--------------------------------------------------------")
		if a == 0:
			self.menuPrincipal()
		elif a == 1:
			self.conf.openConfig()
			print("conf.lastId avant boutton : "+str(self.conf.lastId))
			self.conf.setBouton(True)
			print("conf.lastId avant boutton : "+str(self.conf.lastId))
			print()
			print()
			self.gestionBouton()
		elif a == 2:
			self.conf.setBouton(False)
			print()
			print()
			self.gestionBouton()


a = InterfaceConfig()


