from outils import *
from config import *

class Rappel :
	# Classe permettant de gérer un rappel
	def __init__(self):
		self.initialisation()

	def initialisation(self):
		self.listeDateHeure = []
		self.listeCommandePart1 = []
		self.listeCommandePart2 = []
		self.listeArgumentPart1 = []
		self.listeArgumentPart2 = []
		self.typeRappel = -1
		self.conf = Config()
		

	def lireConfig(self):
		# Fonction permettant d'actualiser la config du réveil.
		# Dans la config, on met l'endroit ou les modules sont stockés, le nom de tous les modules, l'endroit ou les réveils sont stockés (chaque type)
		self.conf.openConfig()

	def save(self):
		# Sauvegarde le rappel
		print("LOL"+self.getEndroit())
		endroit = self.createPath(self.getEndroit())
		if (endroit == ""):
			return False
		if Outils.testPresence(endroit):
			##print("Un fichier existe déja ici : "+endroit)
			return False
		chaine = "\n"
		print("RETURN PASSE")
		for i in range(0,len(self.listeCommandePart1)):
			chaine2 = Outils.constitueBalise("Nom",self.listeCommandePart1[i])
			for i2 in range(0,len(self.listeArgumentPart1[i])):
				chaine2+= Outils.constitueBalise("Argument", self.listeArgumentPart1[i][i2])
			chaine += Outils.constitueBalise("Module",chaine2)+"\n"
		chaine3 = Outils.constitueBalise("Part 1",chaine)+"\n\n"
		print("chaine3 ; "+chaine3)
		chaine = "\n"
		for i in range(0,len(self.listeCommandePart2)):
			chaine2 = Outils.constitueBalise("Nom",self.listeCommandePart2[i])
			for i2 in range(0,len(self.listeArgumentPart2[i])):
				chaine2+= Outils.constitueBalise("Argument", self.listeArgumentPart2[i][i2])
			chaine += Outils.constitueBalise("Module",chaine2)+"\n"

		chaine3 += Outils.constitueBalise("Part 2",chaine)+"\n"
		print("chaine32 ; "+chaine3)
		print("endroit : "+endroit)
		Outils.ecrireFichier(endroit,chaine3)
		return True


	def getEndroit(self):
		# Renvoie l'endroit du fichier si le type et la liste forment un couple possible
		endroit = ""
		if (self.typeRappel == 0 and len(self.listeDateHeure) == 2):
			endroit = str(self.listeDateHeure[0])+"_"+str(self.listeDateHeure[1])+".f"

		elif (self.typeRappel == 1 and len(self.listeDateHeure) == 3):
			endroit = str(self.listeDateHeure[0])+"_"+str(self.listeDateHeure[1])+"_"+str(self.listeDateHeure[2])+".f"

		elif (self.typeRappel == 2 and len(self.listeDateHeure) == 5):
			endroit = str(self.listeDateHeure[0])+"_"+str(self.listeDateHeure[1])+"_"+str(self.listeDateHeure[2])+"_"+str(self.listeDateHeure[3])+"_"+str(self.listeDateHeure[4])+".f"
		##print(endroit)
		return endroit

	def createPath(self,endroit):
		# Cree le path pour le fichier
		self.lireConfig()
		if self.typeRappel == 0:
			endroit = self.conf.pathReveilHeure + endroit
		if self.typeRappel == 1:
			endroit = self.conf.pathReveilJour+endroit
		if self.typeRappel == 2:
			endroit = self.conf.pathReveilDate+endroit
		##print(endroit)
		return endroit

	def openChaine(self,chaine):
		# Ouvre un rappel à partir d'une chaine contenant toutes les données
		self.initialisation()
		chainePart1 = Outils.recupereBaliseAuto(chaine,"Part 1",1)
		chainePart2 = Outils.recupereBaliseAuto(chaine,"Part 2",1)
		print("chaine ; "+chaine)
		print("compter"+str(Outils.compter(chaine,"<Type>")))
		if Outils.compter(chaine,"<Type>") != 0:

			self.typeRappel = int(Outils.recupereBaliseAuto(chaine,"Type",1))
			nb = Outils.compter(chaine,"<ListeDateHeure>")
			for i in range (0,nb):
				print("ListeDATEherure :"+Outils.recupereBaliseAuto(chaine,"ListeDateHeure",i+1))
				self.listeDateHeure.append(int(Outils.recupereBaliseAuto(chaine,"ListeDateHeure",i+1)))

		print("TYPE "+str(self.typeRappel)+" :LISTE: "+str(self.listeDateHeure))
		nb = Outils.compter(chainePart1,"<Module>")
		# A FINIR
		for i in range(0,nb):
			chaineModule = Outils.recupereBaliseAuto(chainePart1,"Module",i+1)
			##print(chaineModule)
			chaineNom = Outils.recupereBaliseAuto(chaineModule,"Nom",1)
			arguments = []
			nbArgument = Outils.compter(chaineModule,"<Argument>")
			for i2 in range (0,nbArgument):
				arguments.append(Outils.recupereBaliseAuto(chaineModule,"Argument",i2+1))
			self.addCommande(chaineNom,arguments)


		nb = Outils.compter(chainePart2,"<Module>")
		for i in range(0,nb):
			chaineModule = Outils.recupereBaliseAuto(chainePart2,"Module",i+1)
			chaineNom = Outils.recupereBaliseAuto(chaineModule,"Nom",1)
			arguments = []
			nbArgument = Outils.compter(chaineModule,"<Argument>")
			for i2 in range (0,nbArgument):
				arguments.append(Outils.recupereBaliseAuto(chaineModule,"Argument",i2+1))
			self.addCommande(chaineNom,arguments,False)

	def openRappel(self,type,listeDateHeure):
		# Ouvre le rappel si il existe
		##print("openRappel")
		self.initialisation()
		self.typeRappel = type
		self.listeDateHeure = listeDateHeure
		endroit = self.getEndroit()
		if (endroit == ""):
			return False
		endroit = self.createPath(endroit)

		if not Outils.testPresence(endroit):
			return False
		##print(endroit)
		chaine = Outils.lireFichier(endroit)
		self.openChaine(chaine)
		return True
			##print("chaineNom dans rappel.py : "+chaineNom)


		#print("open réalisé : arguments part 1 : "+str(self.listeArgumentPart1)) 
		#print("open réalisé : arguments part 2 : "+str(self.listeArgumentPart2)) 

	def addCommande(self,nom,argument = [], part1=True):
		# Permet d'ajouter une commande
		if part1:
			self.listeCommandePart1.append(nom)
			self.listeArgumentPart1.append(argument)

		else:
			self.listeCommandePart2.append(nom)
			self.listeArgumentPart2.append(argument)
		return True

	def delCommande(self,nb, part1 = True):
		# supprime la commande nb si elle existe

		if part1:
			if nb < 0 or nb >= len(self.listeCommandePart1):
				return False
			del(self.listeCommandePart1[nb])
			del(self.listeArgumentPart1[nb])
		else :
			if nb < 0 or nb >= len(self.listeCommandePart2):
				return False
			del(self.listeCommandePart2[nb])
			del(self.listeArgumentPart2[nb])
		return True

	def insererCommande(self,nb1, nb2, part1 = True):
		# Permet d'inserer la commande nb1 à la place nb2
		if part1:
			if nb1 < 0 or nb2 < 0 or nb2 >= len(self.listeCommandePart1) or nb1 >= len(self.listeCommandePart1):
				return False
			commande = self.listeCommandePart1[nb1]
			argument = self.listeArgumentPart1[nb1]
			self.delCommande(nb1)
			self.listeCommandePart1.insert(nb2, commande)
			self.listeArgumentPart1.insert(nb2,argument)
		else :
			if nb1 < 0 or nb2 < 0 or nb2 >= len(self.listeCommandePart2) or nb1 >= len(self.listeCommandePart2):
				return False
			commande = self.listeCommandePart2[nb1]
			argument = self.listeArgumentPart2[nb1]
			self.delCommande(nb1,False)
			self.listeCommandePart2.insert(nb2, commande)
			self.listeArgumentPart2.insert(nb2,argument)

		return True


	def definirHeureDate(self,type,listeDateHeure):
		# Fonction permettant de définir l'heure et la date
		if (type == 0 and len(listeDateHeure) == 2) or ( type == 1 and len(listeDateHeure) == 3) or (type == 2 and len(listeDateHeure)== 5):
			self.typeRappel = type
			self.listeDateHeure = listeDateHeure
			return True

		return False


	def getNomJour(self):
		# Renvoie le jour en chaine si c'est un reveil hebdomadaire
		liste["lundi","mardi","mercredi","jeudi","vendredi","samedi","dimanche"]
		if self.typeRappel == 1:
			return liste[self.listeDateHeure[0]]
		return ""

	def afficherRappel(self):
		# Permet d'afficher quand est-ce que le rappel va être appelé de manière formatée
		chaine = ""
		if self.typeRappel == 0:
			chaine += self.listeDateHeure[0]+"h"+self.listeDateHeure[1]
		elif self.typeRappel == 1:
			chaine += self.getNomJour(self.listeDateHeure[0])+ " à "+self.listeDateHeure[1]+"h"+self.listeDateHeure[2]
		elif self.typeRappel == 2:
			chaine += self.listeDateHeure[0]+"/"+self.listeDateHeure[1]+"/"+self.listeDateHeure[2]+" à "+self.listeDateHeure[3]+"h"+self.listeDateHeure[4]
		return chaine