class Config:
	# Classe permettant de gérer la configuration  du réveil.
	# Gestion de :
	# - Localisation des modules
	# - Liste des modules, leur localisation dans le dossier et le nom associé à ces modules
	# - Les ressources ajoutées
	# - Le fichier presence.f


	def __init__(self):
		self.endroitFichier = "config.f" # Voici l'endroit ou on enregristre la configuration
		self.open()


	def addModule (self,nom,pathModule):
		# Nom du module, un dossier sera crée en remplaçant les espaces par des _
		# pathModule c'est le dossier ou a été crée le module afin qu'on puisse
		self.verificationModule(nom)
		liste = []
		nomDossier =  nom .replace(" ","_")
		liste.append(nom)
		liste.append(nomDossier)
		self.listeModule.append(liste)

		# A FAIRE : transferer le dossier pathModule dans le bon dossier.

		


	def verificationModule (nom):
		# Vérifie que le le module n'existe pas déja
		for i in range (len(self.listeModule)):
			if (self.listeModule[i][0] == nom):
				return False;
		return True;
		
	def delModule (self):
		pass

	def initialisation (self):
		self.listeModule = []
		pass

	def open(self):
		self.initialisation()


	def save(self):

		pass

	def changePathStop1(self):
		pass

	def changePathStop1(self):
		pass

	def get
