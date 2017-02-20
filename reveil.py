from config import *
from outils import *
from time import sleep
import time
import _thread 
from rappel import *
import sys


class Reveil:

	def __init__(self):
		self.initialisation()

	def boucleInfinie(self):
		# Fonction permettant de lancer la boucle infinie du réveil.
		while (True):
			self.verificationHeure()
			self.verificationJour()
			self.verificationDate()
			print("Reveil "+str(time.localtime()[3])+"h"+str(time.localtime()[4]))
			sleep (50)

	def lireConfig(self):
		# Fonction permettant d'actualiser la config du réveil.
		# Dans la config, on met l'endroit ou les modules sont stockés, le nom de tous les modules, l'endroit ou les réveils sont stockés (chaque type)
		self.conf.openConfig()

	
	def initialisation (self):
		# Créer la structure de dossiers et le fichier de configuration
		self.conf = Config()
		self.pathConfig = self.conf.pathConfig
		self.pathReveilHeure = self.conf.pathReveilHeure
		self.pathReveilDate = self.conf.pathReveilDate
		self.pathReveilJour = self.conf.pathReveilJour
		self.pathModule = self.conf.pathLog
		self.pathLog = self.conf.pathLog
		self.temps_tab_heure = [-1,-1,-1,-1,-1,-1,-1,-1,-1]
		self.temps_tab_jour  = [-1,-1,-1,-1,-1,-1,-1,-1,-1]
		self.temps_tab_date  = [-1,-1,-1,-1,-1,-1,-1,-1,-1]
		
		
		

	def verificationHeure(self):
		# Verifie le fichier à l'heure actuelle existe et lance son ouverture si il existe.
		type = 0
		if (time.localtime()[4] != self.temps_tab_heure[4] ):
			self.temps_tab_heure = time.localtime()
			chaine = str(self.temps_tab_heure[3]) + "_" +str(self.temps_tab_heure[4])+".f"
			listeDateHeure = [self.temps_tab_heure[3],self.temps_tab_heure[4]]
			if (Outils.testPresence(self.pathReveilHeure+chaine)):
				_thread.start_new_thread(self.ouvreReveil,(type,listeDateHeure,))
		
		

	def verificationJour(self):
		# Verifie si le fichier à l'heure au au jour actuelle existe (jour style lundi, mardi etc) et lance son ouverture si il existe.
		type = 1
		if (time.localtime()[4] != self.temps_tab_jour[4]  ):
			self.temps_tab_jour = time.localtime()
			chaine = str(self.temps_tab_jour[6]) + "_" + str(self.temps_tab_jour[3]) + "_" +str(self.temps_tab_jour[4])+".f"
			listeDateHeure = [self.temps_tab_jour[6],self.temps_tab_jour[3],self.temps_tab_jour[4]]
			if (Outils.testPresence(self.pathReveilJour+chaine)):
				_thread.start_new_thread(self.ouvreReveil,(type,listeDateHeure,))

	def verificationDate(self):
		# Verifie si un fichier à la date exacte d'aujourd'hui existe (format annee_mois_jour_heure_minute.f) et lance son ouverture si il existe et suprrime le fichier ensuite.
		type = 2
		if (time.localtime()[4] != self.temps_tab_date[4] ):
			self.temps_tab_date = time.localtime()
			listeDateHeure = [self.temps_tab_date[0],self.temps_tab_date[1],self.temps_tab_date[2],self.temps_tab_date[3],self.temps_tab_date[4]]
			type = 2
			chaine = str(self.temps_tab_date[0])+"_"+str(self.temps_tab_date[1])+"_"+str(self.temps_tab_date[2])+"_"+str(self.temps_tab_date[3]) + "_" +str(self.temps_tab_heure[4])+".f"
			if (Outils.testPresence(self.pathReveilDate+chaine)):
				_thread.start_new_thread(self.ouvreReveil,(type,listeDateHeure,))
			

	

	def  createArgument(self,liste,type):
		# Elle crée la première liste d'arguments au début
		self.argumentsListe = []
		self.append(type)
		self.argumentsListe.extends(liste)
		# A FINIR



	def ouvreReveil(self,type,listeDateHeure):
		#  Permet d'oubrir le reveil donné en parametres et d'y lancer les fonctions
		r = Rappel()
		r.openRappel(type,listeDateHeure)
		#print("OuvreReveil")
		# GESTION DE LA PARTIE 1 A FAIRE
		continuer = True
		while continuer:
			#print("boucle")
			for i in range(0,len(r.listeCommandePart1)):
				#input("i : "+str(i))
				self.lireConfig()
				#print("i : "+str(i))
				#print("conf.lastId reveil : "+str(self.conf.lastId))
				if self.conf.bouton == False:
					dossierModule = self.conf.getDossierModule(r.listeCommandePart1[i])
					#print("Dossier : "+dossierModule)
					if dossierModule != "":
						sys.path.append(dossierModule)
						#module = __import__(dossierModule.replace(os.sep,"."),fromlist=[None])  # I don't understant that fromlist # Ajouter module à dossierModule
						module = __import__("module",fromlist=[None])  # I don't understant that fromlist
						sys.path.remove(dossierModule)


						#try:
							#print("arguments : "+str(r.listeArgumentPart1[i]))
							#print("conf.lastId avant module : "+str(self.conf.lastId))
						module.start(r.listeArgumentPart1[i])
						
							#print("conf.lastId apres module : "+str(self.conf.lastId))
						self.suppressionModule()
						#except:
							# A METTRE DANS LE LOG
							#print("conf.lastId except : "+str(self.conf.lastId))
							#pass
				if self.conf.bouton:
					#input("bouton")
					self.conf.setBouton(False)
					continuer = False
					#print("conf.listeLancement : "+str(self.conf.listeAttenteLockAudio))
					#print("break")
					#input("bouton")
					break
			if len(r.listeArgumentPart1) == 0:
				continuer = False
		self.lireConfig()
		#print("conf.listeLancement : "+str(self.conf.listeAttenteLockAudio))
		#print("Rappel ouvert : "+str(len(r.listeCommandePart2)))
		#print("PART 2")
		#input("appuyez pour part2")
		for i in range(0,len(r.listeCommandePart2)):
			dossierModule = self.conf.getDossierModule(r.listeCommandePart2[i])
			#print("Dossier : "+dossierModule)
			if dossierModule != "":
				#print("arguments : "+str(r.listeArgumentPart2[i]))
				#module = __import__(dossierModule.replace(os.sep,"."),fromlist=[None])  # I don't understant that fromlist
				sys.path.append(dossierModule)
				self.lireConfig()
				#print("conf.listeLancement : "+str(self.conf.listeAttenteLockAudio))
				module = __import__("module",fromlist=[None])  # I don't understant that fromlist
				sys.path.remove(dossierModule)

				#try:
				#print("MODULE LANC")
				module.start(r.listeArgumentPart2[i])
				self.suppressionModule()
				#except:
				#	print("EXCEPTION")
				#	print ("Unexpected error:", sys.exc_info()[0])
					# A METTRE DANS LE LOG
				#	pass


	def suppressionModule(self):
		# Supprime le module des listes de modules importés
		#<print("fonction")
		for item in sorted(sys.modules.keys()):
			if "module" in item :
				#print("suppression")
				del(sys.modules[item])




#a = Reveil()
#a.ouvreReveil(2,[2017,2,12,23,5])



