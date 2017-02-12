import os
from config import *
from rappel import *
from outils import *

class ListeRappel:
	# Classe permeettant de lister les rappels existants pour chaque type
	def __init__(self,type):
		self.type = type
		self.conf = Config()

	def getListe(self):
		# Permet de recuperer la liste des  rappels, doit utiliser une fonction python permettant de récuperer la liste des fichiers
		liste = os.listdir()
		pass

	def delRappel(self,id):
		# Permet de supprimer un rappel, en supprimant physiquement le fichier correspondant
		rappel = self.getRappelFromList(listeDateHeure)
		endroit = rappel.createPath(rappel.getEndroit())
		Outils.supprimerFichier()


	def getRappel(self, id):
		# return un rappel avec l'id du fichier demander
		liste = self.getListe()
		nom = liste[id]
		nom = nom.replace(".f","")
		listeDateHeure =  nom.split("_")
		return self.getRappelFromList(listeDateHeure)

	def getRappelFromList(self,listeDateHeure):
		# A partir d'une liste on recuperere le rappel
		rappel = Rappel()
		rappel.definirDateHeure(self.type,listeDateHeure)
		return rapppel


