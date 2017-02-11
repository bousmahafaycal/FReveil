from outils import *
import os

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
		self.openConfig()


	def getDossierModule(self,nom):
		# A partir du nom du module, renvoyer la localisation du module concerné est une chaine vide sinon
		for i in range(0, len(self.listeModule)):
			if self.listeModule[i][0] == nom:
				return self.endroitModule+self.listeModule[i][1]
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
		self.pathConfig = "Donnees"+os.sep+"Config"+os.sep+""
		self.pathReveilHeure = "Donnees"+os.sep+"Reveil"+os.sep+"Heure"+os.sep
		self.pathReveilDate = "Donnees"+os.sep+"Reveil"+os.sep+"Date"+os.sep+""
		self.pathReveilJour = "Donnees"+os.sep+"Reveil"+os.sep+"Jour"+os.sep+""
		self.pathModule = "Donnees"+os.sep+"Module"+os.sep+""
		self.pathLog = "Donnees"+os.sep+"Log"+os.sep+""
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
			
			for i2 in range (Outils.compter(chaine,"<Lancement>")):
				chaine3 = Outils.recupereBaliseAuto(chaine, "Lancement", i+1, "Lancement")
				liste2 = [Outils.recupereBaliseAuto(chaine3, "Nom", 1, "Nom"), Outils.recupereBaliseAuto(chaine3, "Classe", 1, "Classe")]
				self.listeLancement.append(liste2)

			self.presence = Outils.recupereBaliseAuto(chaine, "Presence", 1, "Presence") == "True"
		else:
			# Le fichier n'existe pas LOG A FAIRE
			pass





	def setPresence(self, presence):
		# Modifie si l'utilisateur est présent ou pas.
		self.presence = presence
		self.save()
		# LOG A FAIRE

	def save(self):
		# Fonction qui va sauvegarder la config dans le fichier config.f
		chaine = Outils.constitueBalise("Presence",str(self.presence)) + "\n"
		
		for i in range (len(self.listeModule)):
			chaine += Outils.constitueBalise("Module", Outils.constitueBalise("Nom",self.listeModule[i][0])+Outils.constitueBalise("Dossier",self.listeModule[i][1]))+"\n"
		for i in range(len(self.listeLancement)):
			chaine += Outils.constitueBalise("Lancement",Outils.constitueBalise("Nom", self.listeLancement[i][0])+Outils.constitueBalise("Classe",self.listeLancement[i][1]))
		
		Outils.ecrireFichier(self.endroitFichier,chaine)


