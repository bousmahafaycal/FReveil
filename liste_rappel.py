import os
from config import *
from rappel import *
from outils import *

class ListeRappel:
	# Classe permeettant de lister les rappels existants pour chaque type et d'y apporter des modifications (supprimer des fichiers, les trier etc..)
	def __init__(self,type):
		self.type = type
		self.conf = Config() # 0 c'est les rappels journaliers, 1 c'est les rappels hebdomadaire et 2 c'est les rappels uniques.

	def getListe(self):
		# Permet de recuperer la liste des  rappels, doit utiliser une fonction python permettant de récuperer la liste des fichiers
		liste = []
		if self.type == 0:
			liste = Outils.getDossier(self.conf.pathReveilHeure)
		elif self.type == 1:
			liste = Outils.getDossier(self.conf.pathReveilJour)
		else :
			liste  = Outils.getDossier(self.conf.pathReveilDate)
		return liste

	def afficherRappel(self,id):
		# Permet d'afficher quand est-ce que le rappel va être appelé de manière formatée
		return self.getRappel(id).afficherRappel()


	def delRappel(self,id):
		# Permet de supprimer un rappel, en supprimant physiquement le fichier correspondant
		rappel = self.getRappel(id)
		endroit = rappel.createPath(rappel.getEndroit())
		Outils.supprimerFichier(endroit)
		#print("Ce fichier est supprimé : "+endroit)


	def getListeRappel(self):
		# Renvoie une liste de rappel qui sont tous les rappels enregistrés pour le type demandé
		liste = self.getListe()
		listeRappel = []
		for i in range (0, len(liste)):
			listeRappel.append(self.getRappel(i))
		return listeRappel

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
		rappel.openRappel(self.type,listeDateHeure)
		return rappel


	def getIdRappel(self,rappel):
		# Renvoie l'id d'un rappel à partir du rappel
		liste = self.getListeRappel()
		for i in range(len(liste)):
			if liste[i] == rappel:
				return i
		return -1

	def getIdRappelFichier(self,chaine):
		# Renvoie un id de rappel à partir du nom de fichier
		liste = self.getListe()
		for i in range(len(liste)):
			if liste[i] == chaine:
				return i;

		return -1
