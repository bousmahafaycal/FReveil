from time import sleep
from rappel import *
from reveil import *
import datetime

class InterfaceReveil:
	def __init__ (self):
		self.initialisation()
		self.annonce()
		self.menuPrincipal()


	def annonce(self):
		# Annonce et crédit du programme
		print("Bienvenue dans l'interface de configuration du FReveil.")
		print("Ce programme a été crée par Fayçal Bousmaha.")
		print()
	
	def menuPrincipal(self):
		# Menu principal de cette interface
		print()
		self.initialisation()
		liste = ["Quitter","Ajouter un rappel","Modifier un rappel","Supprimer un rappel", "Voir tous les rappels"]
		a = Outils.menu("MENU PRINCIPAL",liste)
		print()
		if a == 1:
			self.initialisation()
			self.menuAjout()
		elif a == 2:
			modifierRapp()
		elif a == 3:
			self.gestionSuppr()
		elif a == 4:
			self.voirRapp()

	def voirRapp(self):
		# Menu permettant de choisir le type de rappel souhaitant être vu
		pass

	def modifierRapp(self):
		# Menu permettant de choisir le type de rappel souhaitant être modifié
		pass

	def gestionSuppr(self):
		# Permet de supprimer un rappel
		pass

	def initialisation(self):
		# initialise les variables notammant pour ajouter un rappel
		self.rappel = Rappel()
		self.conf = Config()
		self.reveil = Reveil()





	def menuAjout(self):
		# Menu permettant l'ajout d'un réveil
		print()
		liste = ["Menu principal","Definir la date et/ou l'heure","Afficher les commandes de ce rappel","Ajouter des commandes","Supprimer des commandes","Modifier l'ordre des commandes"]
		a = Outils.menu("MENU AJOUT",liste)
		print()
		if a == 0:
			# Faire la sauvegarde
			#print(str(self.rappel.typeRappel)+" \n"+str(self.rappel.listeCommandePart1)+"\n"+str(self.rappel.listeCommandePart2))
			if self.rappel.typeRappel !=  -1  and (len(self.rappel.listeCommandePart1) != 0 or len(self.rappel.listeCommandePart2) != 0):
				self.menuSauvegarder()
			self.menuPrincipal()
		if a == 1 :
			self.definirDateHeure()
		if a == 2:
			self.afficheCommande()
		if a == 3:
			self.ajouterCommande()
		if a == 4:
			self.supprimerCommande()
		if a == 5:
			self.modifierCommande()


	def menuSauvegarder(self):
		# Demande à l'utilisateur si il souhaite sauvegarder le rappel
		print()
		liste = ["Oui","Non"]
		a = Outils.menu("Souhaitez vous sauvegarder le rappel ?",liste,False)
		print()
		if a == 0:
			self.rappel.save()
			print("Ce rappel a été sauvegardé")
		else:
			print("Ce rappel n'a pas été sauvegardé")



	def afficheCommande(self):
		# Afficher les commandes actuellement disponibles
		print()
		print("-------------------")
		print("PART 1 :")
		for i in range(0,len(self.rappel.listeCommandePart1)):
			print(str(i+1)+" - "+self.rappel.listeCommandePart1[i])
		print()
		print("-------------------")
		print("PART 2 :")
		for i in range(0,len(self.rappel.listeCommandePart2)):
			print(str(i+1)+" - "+self.rappel.listeCommandePart2[i])
		print("-------------------")
		print()
		input("Appuyez sur entree pour revenir au menu ")
		print()
		self.menuAjout()

	def seeModule(self):
		# Voir une liste des modules
		self.conf  = Config()
		print("Voici la liste des modules actuellement disponible : ")
		for i in range(0,len(self.conf.listeModule)):
			print(str(i+1)+" - "+self.conf.listeModule[i][0])
		print()

	def ajouterCommande(self):
		# permet d'ajouter des commandes
		self.conf = Config()
		print()
		part1 = self.menuChoixPart()
		print()
		continuer = True
		a = 0
		self.seeModule()
		print()
		menu = False
		argument = []
		while continuer:
			a = Outils.intInput("Merci de bien vouloir entrer le numéro de la commande souhaité (ou 0 pour revenir au menu) : ")

			if (a >= 1 and a <= len(self.conf.listeModule)):
				continuer = False
				a -= 1
			elif a == 0:
				continuer = False
				menu = True
			else :
				print("Merci de bien vouloir entrer un numéro entre 1 et "+len(self.conf.listeModule)+" inclus.")

		
		if not menu:
			print()
			b = Outils.intInput("Combien d'arguments à ce module souhaitez-vous donnez : ")
			print()
			for i in range(0,b):
				argument.append(input("Entrez l'argument n°"+str(1+i)+" : "))
				print()
			self.rappel.addCommande(self.conf.listeModule[a][0],argument ,part1)
			print()
			print("Commande ajoutée !")
		else :
			print()
			print("Commande annulée !")

		sleep(1)
		print()
		self.menuAjout()


	def menuChoixPart(self):
		# Choisir dans quelle partie du rappel la commande sera séléctionnée
		print()
		liste = ["Commandes qui seront lancées en boucle avant l'appui sur le bouton","Commandes lancés après l'appui sur le bouton (si la partie 1 n'est pas vide)"]
		a = Outils.menu("Choix d'une partie",liste)
		print()
		if a == 0:
			return True
		else : 
			return False

	

	def supprimerCommande(self):
		# Permet de supprimer une commande
		print()
		part1 = self.menuChoixPart()
		print()
		a = 0
		continuer = True
		while continuer:
			a = intInput("Choisissez le numero de la commande que vous souhaitez supprimer (mettez 0 pour rien supprimer) : ")
			if a == 0:
				continuer = False
			elif part1 and a > 0 and a <= len(self.rappel.listeCommandePart1):
				continuer = False
				rappel.delCommande(a,True)
				print("Suppression réalisée avec succès !")
			elif not part1 and a > 0 and a <= len(self.rappel.listeCommandePart2):
				continuer = False
				rappel.delCommande(a,False)
				print("Suppression réalisée avec succès !")
			else :
				print("Ce nombre ne correspond pas à une commande, merci de donner un choix valable !")
				print()

		print()
		sleep(3)
		self.menuAjout()


	def modifierCommande(self):
		# Permet de modifier l'ordre des commandes
		pass



	def definirDateHeure(self):
		# Permet de définir  l'heure
		print()
		print("----------------------------")
		print()
		print("Le reveil est actuellement défini ")
		print()
		liste = ["Menu ajout","Rappel journalier","Rappel hebdomadaire","Rappel unique", "Rappel unique dans 1 minute","Rappel unique dans 5 minutes"]
		a = Outils.menu("DEFINIR L'HEURE/LA DATE DU RAPPEL",liste,False)
		print("----------------------------")
		print()
		if a == 0:
			self.menuAjout()
		if a == 1 :
			self.rappelJournalier()
		if a == 2:
			self.rappelHebdomadaire()
		if a == 3:
			self.rappelUnique()
		if a == 4:
			self.rappel.definirHeureDate(2,self.datePlusMinutes(1))
			self.menuAjout()
		if a == 5:
			self.rappel.definirHeureDate(2,self.datePlusMinutes(5))
			self.menuAjout()

	def datePlusMinutes(self,nb):
		# Renvoie une liste avec le temps dans une minute
		now = datetime.datetime.now()
		now_plus_1 = now + datetime.timedelta(minutes = nb)
		liste = [now_plus_1.year,now_plus_1.month, now_plus_1.day, now_plus_1.hour, now_plus_1.minute]
		return liste

	def rappelJournalier(self):
		# Permet de définir l'heure du rapport journallier
		print()
		continuer = True
		if self.rappel.typeRappel == 1:
			print("Heure actuellement définie pour ce rappel : "+self.listeDateHeure[0])
		a = Outils.intInput("Donnez l'heure du rappel : ")
		print()
		if self.rappel.typeRappel == 1:
			print("Minute actuellement définie pour ce rappel : "+self.listeDateHeure[0])
		b = Outils.intInput("Donnez la minute du rappel : ")
		listeDateHeure = [a,b]
		self.rappel.definirHeureDate(0,listeDateHeure)
		print()
		self.menuAjout()


	def rappelHebdomadaire(self):
		# Permet de definir l'heure et le jour du rappel de hebdomadaire
		print()
		continuer = True

		if self.rappel.typeRappel == 1:
			print("Jour actuellement définie pour ce rappel : "+self.listeDateHeure[0])
		c = Outils.intInput("Donnez le jour du rappel (entre 0 et 6 pour) : ")
		print()
		if self.rappel.typeRappel == 1:
			print("Heure actuellement définie pour ce rappel : "+self.listeDateHeure[1])
		a = Outils.intInput("Donnez l'heure du rappel : ")
		print()
		if self.rappel.typeRappel == 1:
			print("Minute actuellement définie pour ce rappel : "+self.listeDateHeure[2])
		b = Outils.intInput("Donnez la minute du rappel : ")
		listeDateHeure = [c,a,b]
		self.rappel.definirHeureDate(1,listeDateHeure)
		print()
		self.menuAjout()


	def rappelUnique(self):
		# Permet de définir l'heure et la date du rapport unique
		print()
		if self.rappel.typeRappel == 2:
			print("Numéro du jour actuellement définie pour ce rappel : "+self.listeDateHeure[0])
		a = Outils.intInput("Donnez le jour du rappel (un entier est attendu) : ")
		print()
		if self.rappel.typeRappel == 2:
			print("Numéro du mois actuellement définie pour ce rappel : "+self.listeDateHeure[1])
		b = Outils.intInput("Donnez le mois du rappel (un entier est attendu) : ")
		if self.rappel.typeRappel == 2:
			print("Année actuellement définie pour ce rappel : "+self.listeDateHeure[2])
		c = Outils.intInput("Donnez l'année du rappel : ")
		print()
		if self.rappel.typeRappel == 2:
			print("Heure actuellement définie pour ce rappel : "+self.listeDateHeure[3])
		d = Outils.intInput("Donnez l'heure du rappel : ")
		print()
		if self.rappel.typeRappel == 2:
			print("Minute actuellement définie pour ce rappel : "+self.listeDateHeure[4])
		e = Outils.intInput("Donnez la minute du rappel : ")
		listeDateHeure = [a,b,c,d,e]
		self.rappel.definirHeureDate(2,listeDateHeure)
		print()
		self.menuAjout()


interface = InterfaceReveil()
	