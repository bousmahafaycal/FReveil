from time import sleep
from rappel import *
from reveil import *
import datetime
from liste_rappel import *

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
			self.initialisation()
			self.voirRapp(1)
		elif a == 3:
			self.voirRapp(2)
		elif a == 4:
			self.voirRapp(0)

	def voirRapp(self,id):
		# Menu permettant de choisir le type de rappel souhaitant être vu si id == 0, modifié si id == 1, supprimer si id == 2
		print()
		liste = ["Menu principal","Rappels journaliers","Rappels hebdomadaires","Rappels uniques"]
		if id == 0:
			chaine = "MENU VOIR RAPPELS : choisissez quel type de rappel souhaitez-vous voir ?"
		elif id == 1:
			chaine = "MENU MODIFIER RAPPELS : choisissez quel type de rappel souhaitez-vous modifier ?"
		else :
			chaine = "MENU SUPPRIMER RAPPELS : choisissez quel type de rappel souhaitez-vous supprimer ?"
		a = Outils.menu(chaine,liste)
		print()
		if a == 0:
			self.menuPrincipal()
		else:
			if id == 0:
				self.voirRappType(a-1)
			elif id == 1:
				self.modifierRappel(a-1)
			else:
				self.supprimerRappel(a-1)

	def voirRappType(self, type):
		# Permet de voir la liste des rappels du type donné. 
		rappel = ListeRappel(type)
		liste = rappel.getListeRappel() 
		if type == 0:
			print("Liste des rappels journaliers : ")
		elif type == 1:
			print("Liste des rappels hebdomadaires : ")
		elif type == 2:
			print("Liste des rappels uniques : ")
		chaine = ""
		for i in range(0,len(liste)):
			chaine = str(i+1)+" : "
			if type == 0:
				chaine += liste[i].listeDateHeure[0]+"h"+liste[i].listeDateHeure[1]
			elif type == 1:
				chaine += liste[i].getNomJour(liste[i].listeDateHeure[0])+ " à "+liste[i].listeDateHeure[1]+"h"+liste[i].listeDateHeure[2]
			elif type == 2:
				chaine += liste[i].listeDateHeure[0]+"/"+liste[i].listeDateHeure[1]+"/"+liste[i].listeDateHeure[2]+" à "+liste[i].listeDateHeure[3]+"h"+liste[i].listeDateHeure[4]

			print(chaine)
		print()
		input("Appuyez sur entrée pour revenir au menu précédent")
		print()
		self.voirRapp()


	def modifierRappel(self,type):
		# Menu permettant de choisir le type de rappel souhaitant être modifié
		self.initialisation()
		print()
		listeRappel = ListeRappel(type)
		liste = []
		liste.append("Revenir au menu précédent")
		for i in range(len(listeRappel.getListeRappel())):
			liste.append(listeRappel.afficherRappel(i))

		a = Outils.menu("Choisissez le module à modifier : ",liste)
		if a == 0:
			self.voirRapp(1)
		else:
			self.rappel = listeRappel.getRappel(a-1)
			self.menuModification(a-1,type)

	def supprimerRappel (self,type):
		# Permet de supprimer un rappel
		print()
		listeRappel = ListeRappel(type)
		liste = []
		liste.append("Revenir au menu précédent")
		for i in range(len(listeRappel.getListeRappel())):
			liste.append(listeRappel.afficherRappel(i))

		a = Outils.menu("Choisissez le module à supprimer : ",liste)
		if a == 0:
			self.voirRapp(2)
		else:
			listeRappel.delRappel(a-1)
			print("Le module a été supprimé avec succès")
			sleep(1)
			print()
			self.voirRapp(2)

	def initialisation(self):
		# initialise les variables notammant pour ajouter un rappel
		self.rappel = Rappel()
		self.conf = Config()
		self.reveil = Reveil()



	def menuModification(self,z,type):
		# Menu permettant la modification d'un rappel
		print()
		print(str(self.rappel.listeDateHeure))
		print(str(self.rappel.typeRappel))
		print(str(self.rappel.listeCommandePart1))
		print(str(self.rappel.listeCommandePart2))
		print()
		liste = ["Menu modifier rappel","Definir la date et/ou l'heure","Afficher les commandes de ce rappel","Ajouter des commandes","Supprimer des commandes","Modifier l'ordre des commandes"]
		a = Outils.menu("MENU MODIFICATION D'UN RAPPEL",liste)
		print()
		if a == 0:
			# Faire la sauvegarde
			#print(str(self.rappel.typeRappel)+" \n"+str(self.rappel.listeCommandePart1)+"\n"+str(self.rappel.listeCommandePart2))
			if self.rappel.typeRappel !=  -1  and (len(self.rappel.listeCommandePart1) != 0 or len(self.rappel.listeCommandePart2) != 0):			
				if 	self.menuSauvegarder(z,type) != 2:
					self.voirRapp(1)
				else: 
					self.menuModification(z,type)

			else:
				self.menuConfirmation(z,type)
		if a == 1 :
			self.definirDateHeure(1,z,type)
		if a == 2:
			self.afficheCommande(1,z,type)
		if a == 3:
			self.ajouterCommande(1,z,type)
		if a == 4:
			self.supprimerCommande(1,z,type)
		if a == 5:
			self.modifierCommande(1,z,type)			
		

	def menuConfirmation(self,id = 0, z = -1, type = -1):
		# Menu demandant la confirmation du départ sans sauvegarder
		print()
		print("Vous n'avez pas défini quand est-ce que le rappel devra être appelé et/ou vous n'avez pas défini de commande à lancer pour ce rappel.")
		print()
		liste = ["Oui","Non"]
		if id == 0: # Un ajout classique
			chaine = "Souhaitez vous revenir au menu principal sans sauvegarder ?"
		else :
			chaine = "Souhaitez vous revenir au menu modification sans sauvegarder ?"
		a = Outils.menu(chaine,liste,False)
		print()
		if a == 0:

			print("Ce rappel n'a pas été sauvegardé")
			sleep(1)
			print()

			if id == 0:
				self.menuPrincipal()
			else :
				self.voirRapp(1)
			
		else:
			if id == 0:
				self.menuAjout()
			if id == 1:
				self.menuModification(z,type)

	def menuAjout(self):
		# Menu permettant l'ajout d'un rappel
		print()
		liste = ["Menu principal","Definir la date et/ou l'heure","Afficher les commandes de ce rappel","Ajouter des commandes","Supprimer des commandes","Modifier l'ordre des commandes"]
		a = Outils.menu("MENU AJOUT",liste)
		print()
		if a == 0:
			# Faire la sauvegarde
			#print(str(self.rappel.typeRappel)+" \n"+str(self.rappel.listeCommandePart1)+"\n"+str(self.rappel.listeCommandePart2))
			if self.rappel.typeRappel !=  -1  and (len(self.rappel.listeCommandePart1) != 0 or len(self.rappel.listeCommandePart2) != 0):			
				if 	self.menuSauvegarder() != 2:
					self.menuPrincipal()
				else: 
					self.menuAjout()

			else:
				self.menuConfirmation()

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
			
		


	def menuSauvegarder(self,z = -1,type = -1):
		# Demande à l'utilisateur si il souhaite sauvegarder le rappel
		# La procedure de suppression est un peu complexe car il faut prendre en compte le cas ou le rappel ajouté décale la liste de rappel
		print()
		liste = ["Oui","Non"]
		a = Outils.menu("Souhaitez vous sauvegarder le rappel ?",liste,False)
		print()
		if a == 0:
			if z != 1 and type != -1:
				listeRappel = ListeRappel(type)
				liste = listeRappel.getListeRappel()
				rappel = listeRappel.getRappel(z)
				#z = listeRappel.getIdRappel(rappel)
				listeRappel.delRappel(a-1)
				#print(str(rappel.createPath(rappel.getEndroit())))
			if not self.rappel.save():
				if z != 1 and type != -1:
					rappel.save()
				print("Sauvegarde impossible : merci de modifier l'heure/la date car un réveil existe déja pour cette heure/date ci.")
				print("Si vous souhaitez ajouter des commandes à cette heure-ci, merci de modifier le rappel déja existant.")
				print()

				return 2
			
				

			print("Ce rappel a été sauvegardé")
			sleep(1)
			return 0
		else:
			print("Ce rappel n'a pas été sauvegardé")
			sleep(1)
			return 1



	def afficheCommande(self,id = 0,z = -1,type = -1):
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
		if id == 0:
			self.menuAjout()
		else :
			self.menuModification(z,type)

	def seeModule(self):
		# Voir une liste des modules
		self.conf  = Config()
		print("Voici la liste des modules actuellement disponible : ")
		for i in range(0,len(self.conf.listeModule)):
			print(str(i+1)+" - "+self.conf.listeModule[i][0])
		print()

	def ajouterCommande(self,id = 0,z = -1,type = -1):
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
		if id == 0:
			self.menuAjout()
		else :
			self.menuModification(z,type)


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

	

	def supprimerCommande(self,id = 0,z = -1,type = -1):
		# Permet de supprimer une commande
		print()
		part1 = self.menuChoixPart()
		print()
		a = 0
		continuer = True
		while continuer:
			a = Outils.intInput("Choisissez le numero de la commande que vous souhaitez supprimer (mettez 0 pour rien supprimer) : ")
			if a == 0:
				continuer = False
				print("Aucune supression n'a été réalisée !")
			elif part1 and a > 0 and a <= len(self.rappel.listeCommandePart1):
				continuer = False
				self.rappel.delCommande(a-1,True)
				print("Suppression réalisée avec succès !")
			elif not part1 and a > 0 and a <= len(self.rappel.listeCommandePart2):
				continuer = False
				self.rappel.delCommande(a-1,False)
				print("Suppression réalisée avec succès !")
			else :
				print("Ce nombre ne correspond pas à une commande, merci de donner un choix valable !")
				print()

		print()
		sleep(1)
		if id == 0:
			self.menuAjout()
		else :
			self.menuModification(z,type)


	def modifierCommande(self,id = 0,z = -1,type = -1):
		# Permet de modifier l'ordre des commandes
		print()
		part1 = self.menuChoixPart()
		print()
		a = 0
		continuer = True
		menu = False
		while continuer:
			a = Outils.intInput("Choisissez le numero de la commande que vous souhaitez insérer ailleurs (mettez 0 pour rien modifier) : ")
			if a == 0:
				continuer = False
				menu = True
				print("Modification annulée !")
			elif part1 and a > 0 and a <= len(self.rappel.listeCommandePart1):
				continuer = False
			elif not part1 and a > 0 and a <= len(self.rappel.listeCommandePart2):
				continuer = False
			else :
				print("Ce nombre ne correspond pas à une commande, merci de donner un choix valable !")
				print()

		
		if not menu :
			b =a 
			continuer = True
			while continuer:
				a = Outils.intInput("Choisissez le numero de la commande où vous souhaitez insérer votre commande (mettez 0 pour rien modifier) : ")
				if a == 0:
					continuer = False
					menu = True
					print("Modification annulée !")
				elif part1 and a > 0 and a <= len(self.rappel.listeCommandePart1):
					continuer = False
					#self.rappel.delCommande(a,True)
					print("Modification réalisée avec succès !")
				elif not part1 and a > 0 and a <= len(self.rappel.listeCommandePart2):
					continuer = False
					#self.rappel.delCommande(a,False)
					print("Modification réalisée avec succès !")
				else :
					print("Ce nombre ne correspond pas à une commande, merci de donner un choix valable !")
					print()

			if not menu:
				self.rappel.insererCommande(b-1, a-1, part1)

		print()
		sleep(1)
		if id == 0:
			self.menuAjout()
		else :
			self.menuModification(z,type)




	def definirDateHeure(self,id = 0,z = -1,type = -1):
		# Permet de définir  l'heure
		print()
		print("----------------------------")
		print()
		print()
		if id == 0:
			liste = ["Menu ajout","Rappel journalier","Rappel hebdomadaire","Rappel unique", "Rappel unique dans 1 minute","Rappel unique dans 5 minutes"]
		else :
			liste = ["Menu modification","Rappel journalier","Rappel hebdomadaire","Rappel unique", "Rappel unique dans 1 minute","Rappel unique dans 5 minutes"]

		a = Outils.menu("DEFINIR L'HEURE/LA DATE DU RAPPEL",liste,False)
		print("----------------------------")
		print()
		if a == 0:
			self.menuAjout()
		if a == 1 :
			self.rappelJournalier(id,z,type)
		if a == 2:
			self.rappelHebdomadaire(id,z,type)
		if a == 3:
			self.rappelUnique(id,z,type)
		if a == 4:
			self.rappel.definirHeureDate(2,self.datePlusMinutes(1))
			if id == 0:
				self.menuAjout()
			else :
				self.menuModification(z,type)
		if a == 5:
			self.rappel.definirHeureDate(2,self.datePlusMinutes(5))
			if id == 0:
				self.menuAjout()
			else :
				self.menuModification(z,type)

	def datePlusMinutes(self,nb,id = 0,z = -1,type = -1):
		# Renvoie une liste avec le temps dans une minute
		now = datetime.datetime.now()
		now_plus_1 = now + datetime.timedelta(minutes = nb)
		liste = [now_plus_1.year,now_plus_1.month, now_plus_1.day, now_plus_1.hour, now_plus_1.minute]
		return liste

	def rappelJournalier(self,id = 0,z = -1,type = -1):
		# Permet de définir l'heure du rapport journallier
		print()
		continuer = True
		if self.rappel.typeRappel == 1:
			print("Heure actuellement définie pour ce rappel : "+str(self.rappel.listeDateHeure[0]))
		a = Outils.intInput("Donnez l'heure du rappel : ")
		print()
		if self.rappel.typeRappel == 1:
			print("Minute actuellement définie pour ce rappel : "+str(self.rappel.listeDateHeure[1]))
		b = Outils.intInput("Donnez la minute du rappel : ")
		listeDateHeure = [a,b]
		self.rappel.definirHeureDate(0,listeDateHeure)
		print()
		if id == 0:
			self.menuAjout()
		else :
			self.menuModification(z,type)


	def rappelHebdomadaire(self,id = 0,z = -1,type = -1):
		# Permet de definir l'heure et le jour du rappel de hebdomadaire
		print()
		continuer = True

		if self.rappel.typeRappel == 1:
			print("Jour actuellement définie pour ce rappel : "+str(self.rappel.listeDateHeure[0]))
		c = Outils.intInput("Donnez le jour du rappel (entre 0 pour lundi et 6 pour dimanche) : ")
		print()
		if self.rappel.typeRappel == 1:
			print("Heure actuellement définie pour ce rappel : "+str(self.rappel.listeDateHeure[1]))
		a = Outils.intInput("Donnez l'heure du rappel : ")
		print()
		if self.rappel.typeRappel == 1:
			print("Minute actuellement définie pour ce rappel : "+str(self.rappel.listeDateHeure[2]))
		b = Outils.intInput("Donnez la minute du rappel : ")
		listeDateHeure = [c,a,b]
		self.rappel.definirHeureDate(1,listeDateHeure)
		print()
		if id == 0:
			self.menuAjout()
		else :
			self.menuModification(z,type)


	def rappelUnique(self,id = 0,z = -1,type = -1):
		# Permet de définir l'heure et la date du rapport unique
		print()
		if self.rappel.typeRappel == 2:
			print("Numéro du jour actuellement définie pour ce rappel : "+str(self.rappel.listeDateHeure[2]))
		a = Outils.intInput("Donnez le jour du rappel (un entier est attendu) : ")
		print()
		if self.rappel.typeRappel == 2:
			print("Numéro du mois actuellement définie pour ce rappel : "+str(self.rappel.listeDateHeure[1]))
		b = Outils.intInput("Donnez le mois du rappel (un entier est attendu) : ")
		if self.rappel.typeRappel == 2:
			print("Année actuellement définie pour ce rappel : "+str(self.rappel.listeDateHeure[0]))
		c = Outils.intInput("Donnez l'année du rappel : ")
		print()
		if self.rappel.typeRappel == 2:
			print("Heure actuellement définie pour ce rappel : "+str(self.rappel.listeDateHeure[3]))
		d = Outils.intInput("Donnez l'heure du rappel : ")
		print()
		if self.rappel.typeRappel == 2:
			print("Minute actuellement définie pour ce rappel : "+str(self.rappel.listeDateHeure[4]))
		e = Outils.intInput("Donnez la minute du rappel : ")
		listeDateHeure = [c,b,a,d,e]
		self.rappel.definirHeureDate(2,listeDateHeure)
		print()
		if id == 0:
			self.menuAjout()
		else :
			self.menuModification(z,type)


interface = InterfaceReveil()
	