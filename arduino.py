from config  import *

class Arduino:
	# Classe qui va communiquer en USB avec une arduino pour gerer toute la partie electronique
	def __init__(self):
		initialisation()

	def initialisation(self):
		# initialisation de ce qui est nécéssaire pour cette classe.
		self.conf = Config()
		self.listeAttente = []


	def serveur(self):
		# Fonction qui va etre lancer qui aura une boucle infinie et qui communiquera avec l'arduino dès qu'il y aura une modification.
		while True:
			if len(self.listeAttente) != 0:
				ser.write(str(self.getDebListeAttente()).encode('ascii'))
			lu = ser.readline()
			chaine = lu.decode('ascii')
			try:
				nb = int(chaine)
				self.effectueModification(nb)
			except:
				pass

	

	def verifChangement(self):
		# Verifie les changements et ajoute dans la liste d'attente ces changements.
		conf = Config()
		liste = conf.verifChangement()
		self.listeAttente.extend(liste)
		self.conf = conf


	def getDebListeAttente(self):
		# Renvoie le premier chiffre et le supprime de la listeAttente
		a = 0
		if (len(self.listeAttente) != 0):
			a = self.listeAttente[0]
			del(self.listeAttente[0])
		return a

	def effectueModification(self,nb):
		# Fonction qui va effectuer la modification dans config.py selon la commande reçue.
		if nb == 0:
			return
		elif nb == 1:
			self.conf.setPresence(False)
		elif nb == 2:
			self.conf.setPresence(True)
		elif nb == 3:
			self.conf.setBouton(False)
		elif nb == 4:
			self.conf.setBouton(True)