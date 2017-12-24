from config  import *
from time import sleep
from serial import Serial

class Arduino:
	# Classe qui va communiquer en USB avec une arduino pour gerer toute la partie electronique
	def __init__(self):
		self.initialisation()

	def initialisation(self):
		# initialisation de ce qui est nécéssaire pour cette classe.
		self.conf = Config()
		self.listeAttente = []


	def serveur(self):
		# Fonction qui va etre lancer qui aura une boucle infinie et qui communiquera avec l'arduino dès qu'il y aura une modification.
		continuer = False
		#print("serveur")
		try :
			#print("before ser")
			ser = Serial(port="/dev/ttyUSB0",baudrate=9600,timeout=1)
			#print("before sleep")
			sleep(4)
			#print("After sleep")
			continuer = True
		except:
			#print("except")
			return



		self.firstLancement()
		#print("firstLancement")


		while continuer:
			#print("boucle")
			self.verifierChangement()
			if len(self.listeAttente) != 0:
				#print("different 0")
				a = str(self.getDebListeAttente())
				#print("a (str) : "+a)
				ser.write(a.encode('ascii'))
			else:
				ser.write("0".encode('ascii'))
			lu = ser.readline()
			chaine = lu.decode('ascii')
			try:
				nb = int(chaine)
				self.effectueModification(nb)
			except:
				#print("except")
				pass
				"""
			nb = int(chaine)
			self.effectueModification(nb)"""

	

	def firstLancement(self):
		# Au premier lancement les led sont forcément éteintes de l'arduino. On configure de manière à ce que tout ce parametre correctement.
		liste = self.conf.firstLancement()
		self.listeAttente.extend(liste)

	def verifierChangement(self):
		# Verifie les changements et ajoute dans la liste d'attente ces changements.
		conf = Config()
		liste = conf.verifierChangement(self.conf)
		self.listeAttente.extend(liste)
		self.conf = conf


	def getDebListeAttente(self):
		# Renvoie le premier chiffre et le supprime de la listeAttente
		a = 0
		if (len(self.listeAttente) != 0):
			a = self.listeAttente[0]
			del(self.listeAttente[0])

		#print("a : "+str(a))
		return a

	def effectueModification(self,nb):
		# Fonction qui va effectuer la modification dans config.py selon la commande reçue.
		#print("effectueModification")
		if nb == 0:
			#print("return")
			return 0
		elif nb == 1:
			self.conf.setPresence(False)
		elif nb == 2:
			self.conf.setPresence(True)
		elif nb == 3:
			self.conf.setBouton(False)
		elif nb == 4:
			self.conf.setBouton(True)