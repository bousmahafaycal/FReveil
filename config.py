from outils import *
import os
from time import sleep

class Config:
	# Classe permettant de gérer la configuration  du réveil.
	# Gestion de :
	# - Localisation des modules
	# - Liste des modules, leur localisation dans le dossier et le nom associé à ces modules
	# - Liste des fichiers à lancer dès le début (nom du module, fichier classe qui sera à importer et à lancer (fonction start pour lancer))
	# - Le fichier presence.f


	def __init__(self):
		self.endroitFichier = "Donnees"+os.sep+"Config"+os.sep+"config.f" # Voici l'endroit ou on enregristre la configuration
		self.endroitModule = "Donnees"+os.sep+"Module"+os.sep
		self.lockAudio = False
		self.listeAttenteLockAudio = []
		self.lastId = 0
		self.openConfig()


	def getDossierModule(self,nom):
		# A partir du nom du module, renvoyer la localisation du module concerné est une chaine vide sinon
		for i in range(0, len(self.listeModule)):
			if self.listeModule[i][0] == nom:
				return self.endroitModule+self.listeModule[i][1]+os.sep
		return ""

	def addModule (self,nom,pathModule):
		# Nom du module, un dossier sera crée en remplaçant les espaces par des _
		# pathModule c'est le dossier ou a été crée le module afin qu'on puisse
		self.verificationModule(nom)
		liste = []
		Dossier =  nom .replace(" ","_")
		liste.append(nom)
		liste.append(Dossier)
		self.listeModule.append(liste)
		Outils.copieDossier(pathModule, self.endroitModule+Dossier)
		self.save()


	def verificationModule (self,nom):
		# Vérifie que le le module n'existe pas déja
		for i in range (len(self.listeModule)):
			if (self.listeModule[i][0] == nom):
				return False;
		return True;

	def getNumModule(self,nom):
		# Retourne le numéro du module à partir de son nom
		for i in range (len(self.listeModule)):
			if (self.listeModule[i][0] == nom):
				return i;
		return -1;

	def delModule (self,nb):
		# Supprime un module à partir de son numéro
		Outils.supprimeDossier(self.endroitModule+self.listeModule[nb][1]) 
		del(self.listeModule[nb])
		self.save()
		# LOG A FAIRE

	def initialisation (self):
		self.listeModule = []
		self.listeLancement = [] # 
		self.presence = True
		self.bouton = False
		self.pathConfig = "Donnees"+os.sep+"Config"+os.sep+""
		self.pathReveilHeure = "Donnees"+os.sep+"Reveil"+os.sep+"Heure"+os.sep
		self.pathReveilDate = "Donnees"+os.sep+"Reveil"+os.sep+"Date"+os.sep+""
		self.pathReveilJour = "Donnees"+os.sep+"Reveil"+os.sep+"Jour"+os.sep+""
		self.pathModule = "Donnees"+os.sep+"Module"+os.sep+""
		self.pathLog = "Donnees"+os.sep+"Log"+os.sep+""
		self.lockAudio = False
		self.listeAttenteLockAudio = []
		self.lastId = 0
		Outils.creeDossier(self.pathConfig)
		Outils.creeDossier(self.pathReveilHeure)
		Outils.creeDossier(self.pathReveilDate)
		Outils.creeDossier(self.pathReveilJour)
		Outils.creeDossier(self.pathModule)
		Outils.creeDossier(self.pathLog)
		# LOG A FAIRE

	def openConfig(self):
		# Ouvre le fichier config.f et importe les données
		self.initialisation()
		if (Outils.testPresence(self.endroitFichier)):
			# LOG A FAIRE
			chaine = Outils.lireFichier(self.endroitFichier)
			for i in range (Outils.compter(chaine,"<Module>")):
				chaine2 = Outils.recupereBaliseAuto(chaine, "Module", i+1, "Module")
				liste = [Outils.recupereBaliseAuto(chaine2, "Nom", 1, "Nom"), Outils.recupereBaliseAuto(chaine2, "Dossier", 1, "Dossier")]
				self.listeModule.append(liste)
			
			for i in range (Outils.compter(chaine,"<Lancement>")):
				chaine3 = Outils.recupereBaliseAuto(chaine, "Lancement", i+1, "Lancement")
				liste2 = [Outils.recupereBaliseAuto(chaine3, "Nom", 1, "Nom"), Outils.recupereBaliseAuto(chaine3, "Classe", 1, "Classe")]
				self.listeLancement.append(liste2)

			for i in range(Outils.compter(chaine,"<ListeAttenteRessourceAudio")):
				chaine2 = Outils.recupereBaliseAuto(chaine, "ListeAttenteRessourceAudio", i+1)
				self.listeAttenteLockAudio.append(int(chaine2))
			#print("openConfig : "+str(self.listeAttenteLockAudio))
			self.presence = Outils.recupereBaliseAuto(chaine, "Presence", 1, "Presence") == "True"
			self.bouton = Outils.recupereBaliseAuto(chaine, "Bouton", 1) == "True"
			self.lockAudio = Outils.recupereBaliseAuto(chaine, "RessourceAudio", 1) == "True"
			self.lastId = int(Outils.recupereBaliseAuto(chaine, "LastId", 1))
			
		else:
			# Le fichier n'existe pas LOG A FAIRE
			pass





	def setPresence(self, presence):
		# Modifie si l'utilisateur est présent ou pas.
		self.openConfig()
		self.presence = presence
		self.save()
		# LOG A FAIRE

	def setBouton(self, bouton):
		# Modifie si l'utilisateur est présent ou pas.
		self.openConfig()
		self.bouton = bouton
		self.save()
		# LOG A FAIRE

	def getId(self):
		# Va donner un id au module
		self.openConfig()
		self.lastId += 1
		self.save()
		##print("lastId : "+str(self.lastId))
		return self.lastId - 1

	def setLockAudio(self,valeur,id):
		# Quand cette ressouce est à true, cela signifie qu'un module utilise la musique
		# Returns: 1 signifie qu'on a le lock audio, 2 qu'on lache le lock audio, 3 quand on est dans la file d'attente
		fileAttente = False
		self.openConfig()
		#print("commencement"+str(self.listeAttenteLockAudio))
		if self.lockAudio == False:
			if len(self.listeAttenteLockAudio) == 0:
				self.listeAttenteLockAudio.append(id)
				self.lockAudio = valeur
				self.save()
				#print("setLockAudio: "+str(self.listeAttenteLockAudio))
				sleep(0.2)
				return 1
			elif id == self.listeAttenteLockAudio[0]:
				self.lockAudio = valeur
				self.save()
				#print("Facilité")
				sleep(0.2)
				return 1
			elif id not in self.listeAttenteLockAudio and valeur:
				#print("file1")
				fileAttente = True
		else:
			if len(self.listeAttenteLockAudio) == 0:
				#print("file2")
				fileAttente = True

			elif (valeur) and id == self.listeAttenteLockAudio[0]: # Si on demande à avoir le lock alors qu'on l'a déja. Cas qui ne devrait pas se présenter mais on sait jamais
				sleep(0.2)
				return 1
			

			elif (not valeur) and id == self.listeAttenteLockAudio[0]:
				del(self.listeAttenteLockAudio[0])
				self.lockAudio = valeur
				self.save()
				#print("On lache le setLockAudio: "+str(self.listeAttenteLockAudio))
				sleep(0.2)
				return 2
			elif id not  in self.listeAttenteLockAudio:
				#print("file3")
				fileAttente = True

		# Si fileAttente vaut True, ca veut dire qu'on doit l'inserer dans la file d'attente
		if fileAttente == True :
			#print("fileAttente")
			self.listeAttenteLockAudio.append(id)
			self.save()
		sleep(0.2)
		return 3 # soit on vient de l'inserer dans la file d'attente, soit il y est déja

	def save(self):
		# Fonction qui va sauvegarder la config dans le fichier config.f
		chaine = Outils.constitueBalise("Presence",str(self.presence)) + "\n"
		chaine += Outils.constitueBalise("Bouton",str(self.bouton)) + "\n"
		chaine += Outils.constitueBalise("RessourceAudio",str(self.lockAudio)) + "\n"
		chaine += Outils.constitueBalise("LastId",str(self.lastId)) + "\n"
		
		for i in range (len(self.listeModule)):
			chaine += Outils.constitueBalise("Module", Outils.constitueBalise("Nom",self.listeModule[i][0])+Outils.constitueBalise("Dossier",self.listeModule[i][1]))+"\n"
		chaine += "\n"
		for i in range(len(self.listeLancement)):
			chaine += Outils.constitueBalise("Lancement",Outils.constitueBalise("Nom", self.listeLancement[i][0])+Outils.constitueBalise("Classe",self.listeLancement[i][1]))+"\n"
		chaine += "\n"
		for i in range(len(self.listeAttenteLockAudio)):
			chaine += Outils.constitueBalise("ListeAttenteRessourceAudio", str(self.listeAttenteLockAudio[i]))+"\n"
		Outils.ecrireFichier(self.endroitFichier,chaine)


	def cleanUpAudio(self):
		# Fonction permettant de remettre la gestion de ressource audio à 0
		self.openConfig()
		self.lockAudio = False
		self.listeAttenteLockAudio = []
		self.lastId = 0
		self.save()


	def verifierChangement(self,conf):
		# Fonctioon verifiant l'objet actuel (le plus récent) à l'objet conf (plus ancien) et qui renvoie une liste de tous les changements
		liste = []
		if self.presence != conf.presence:
			if not self.presence:
				liste.append(1) # Signifie que la présence est passée true à false
			else:
				liste.append(2) # Signifie que la présence est passée de false à true
		if self.bouton != conf.bouton:
			if not self.bouton:
				liste.append(3) # Signifie que le bouton est passé de true à false
			else :
				liste.append(4) # Signifie que le bouton est passé de false à true

		if self.lockAudio != conf.lockAudio:
			if not self.lockAudio:
				liste.append(5)  # Signifie que le lock audio est passé de true à false
			else:
				liste.append(6) # Signifie que le lock audio est passé de false à true

		return liste


	def firstLancement(self):
		# Crée une liste de l'état de la config actuelle
		liste = []
		if not self.presence:
			liste.append(1) # Signifie que la présence est  à false
		else:
			liste.append(2) # Signifie que la présence est  à true

		if not self.bouton:
			liste.append(3) # Signifie que le bouton est à false
		else :
			liste.append(4) # Signifie que le bouton est à true

		if not self.lockAudio:
			liste.append(5)  # Signifie que le lock audio est à false
		else:
			liste.append(6) # Signifie que le lock audio est à true

		return liste