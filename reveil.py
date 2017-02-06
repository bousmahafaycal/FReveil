from config import *
from outils import *
from time import sleep
import time
import _thread 


class Reveil:

	def __init__(self):
		self.initialisation()

	def boucleInfinie(self):
		# Fonction permettant de lancer la boucle infinie du réveil.
		while (True):
			self.verificationHeure()
			self.verificationJour()
			self.verificationDate()
			print("Reveil")
			sleep (50)

	def lireConfig(self):
		# Fonction permettant d'actualiser la config du réveil.
		# Dans la config, on met l'endroit ou les modules sont stockés, le nom de tous les modules, l'endroit ou les réveils sont stockés (chaque type)
		self.conf.openConfig()

	
	def initialisation (self):
		# Créer la structure de dossiers et le fichier de configuration
		self.pathConfig = "Donnees/Config/"
		self.pathReveilHeure = "Donnees/Reveil/Heure/"
		self.pathReveilDate = "Donnees/Reveil/Date/"
		self.pathReveilJour = "Donnees/Reveil/Jour/"
		self.pathModule = "Donnees/Module/"
		self.pathLog = "Donnees/Log/"
		Outils.creeDossier(self.pathConfig)
		Outils.creeDossier(self.pathReveilHeure)
		Outils.creeDossier(self.pathReveilDate)
		Outils.creeDossier(self.pathReveilJour)
		Outils.creeDossier(self.pathModule)
		Outils.creeDossier(self.pathLog)
		self.conf = Config()
		self.temps_tab_heure = -1
		self.temps_tab_jour  = -1
		self.temps_tab_date  = -1
		

	def verificationHeure(self):
		# Verifie le fichier à l'heure actuelle existe et lance son ouverture si il existe.
		if (time.localtime() != self.temps_tab_heure  ):
			self.temps_tab_heure = time.localtime()
			chaine = str(self.temps_tab_heure[3]) + "_" +str(self.temps_tab_heure[4])+".f"
			if (Outils.testPresence(self.pathReveilHeure+chaine)):
				_thread.start_new_thread(self.ouvreReveil,(self.pathReveilHeure+chaine,))
		
		

	def verificationJour(self):
		# Verifie si le fichier à l'heure au au jour actuelle existe (jour style lundi, mardi etc) et lance son ouverture si il existe.
		if (time.localtime() != self.temps_tab_jour  ):
			self.temps_tab_jour = time.localtime()
			chaine = str(self.temps_tab_jour[6]) + "_" + str(self.temps_tab_jour[3]) + "_" +str(self.temps_tab_jour[4])+".f"
			if (Outils.testPresence(self.pathReveilJour+chaine)):
				_thread.start_new_thread(self.ouvreReveil,(self.pathReveilJour+chaine,))

	def verificationDate(self):
		# Verifie si un fichier à la date exacte d'aujourd'hui existe (format annee_mois_jour_heure_minute.f) et lance son ouverture si il existe et suprrime le fichier ensuite.
		if (time.localtime() != self.temps_tab_date ):
			self.temps_tab_date = time.localtime()
			chaine = str(self.temps_tab_date[0])+"_"+str(self.temps_tab_date[1])+"_"+str(self.temps_tab_date[2])+"_"+str(self.temps_tab_date[3]) + "_" +str(self.temps_tab_heure[4])+".f"
			if (Outils.testPresence(self.pathReveilDate+chaine)):
				_thread.start_new_thread(self.ouvreReveil,(self.pathReveilDate+chaine,))
			

	def ouvreReveil(self,path):
		# Permet d'ouvrir le fichier donné en parametres NE SE PREOCCUPE PAS DE PART1 pour le moment
		chaine = Outils.lireFichier(path)
		chainePart1 = Outils.recupereBaliseAuto(chaine,"Part 1",1)
		chainePart2 = Outils.recupereBaliseAuto(chaine,"Part 2",1)
		nb = Outils.compter(chainePart2,"<Module>")
		for i in range (0,nb):
			chaineModule = Outils.recupereBaliseAuto(chainePart2,"Module",i+1)
			chaineNom = Outils.recupereBaliseAuto(chaineModule,"Nom",1)
			arguments = []
			nbArgument = Outils.compter(chainePart2,"<Argument>")
			for i2 in range (0,nbArgument):
				arguments.append(Outils.recupereBaliseAuto(chaineModule,"Argument",i2+1))
			self.lireConfig()
			dossierModule = self.conf.getDossierModule(chaineNom)
			if dossierModule != "":
				module = __import__(dossierModule.replace(os.separator,".")+"module.py",fromlist=[None])  # I don't understant that fromlist
				try:
					module.start(arguments)
				except:
					# A METTRE DANS LE LOG
					pass









