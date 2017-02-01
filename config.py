from Outils import *

class Config:
	# Classe permettant de gérer la configuration  du réveil.
	# Gestion de :
	# - Localisation des modules
	# - Liste des modules, leur localisation dans le dossier et le nom associé à ces modules
	# - Les ressources ajoutées
	# - Le fichier presence.f


	def __init__(self):
		self.endroitFichier = "Donnees/Config/config.f" # Voici l'endroit ou on enregristre la configuration
		self.endroitModule = "Donnees/Modules/"
		self.open()


	def addModule (self,nom,pathModule):
		# Nom du module, un dossier sera crée en remplaçant les espaces par des _
		# pathModule c'est le dossier ou a été crée le module afin qu'on puisse
		self.verificationModule(nom)
		liste = []
		Dossier =  nom .replace(" ","_")
		liste.append(nom)
		liste.append(Dossier)
		self.listeModule.append(liste)
		Outils.copieDossier(pathModule, self.endroitModule+Dossier) # FONCTION A FAIRE : transferer le dossier pathModule dans le bon dossier.
		self.save()


	def verificationModule (nom):
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
		Outils.supprimeDossier(self.endroitModule+self.listeModule[nb][1]) # FONCTION A FAIRE
		del(self.listeModule[nb])
		self.save()
		# LOG A FAIRE

	def initialisation (self):
		self.listeModule = []
		self.presence = True
		# LOG A FAIRE

	def open(self):
		# Ouvre le fichier config.f et importe les données
		self.initialisation()
		if (Outils.testPresence(endroitFichier)):
			# LOG A FAIRE
			chaine = Outils.lireFichier(endroitFichier)
			for i in range (Outils.compter(chaine,"<Module>")):
				chaine2 = Outils.recupereBaliseAuto(chaine, "Module", i+1, "Module")
				liste = [Outils.recupereBaliseAuto(chaine, "Nom", 1, "Nom"), Outils.recupereBaliseAuto(chaine, "Dossier", 1, "Dossier")]
				self.listeModule.append(liste)
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
		for i in range (len(self.listeModule))
			chaine += Outils.constitueBalise("Module", Outils.constitueBalise("Nom",self.listeModule[i][0])+Outils.constitueBalise("Dossier",self.listeModule[i][1]))
		Outils.ecrireFichier(self.endroitFichier,chaine)


