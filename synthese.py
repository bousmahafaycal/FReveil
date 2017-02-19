""" By Fayçal Bousmaha Un objet permettant d'utiliser la synthese vocale 
avec des fonctions définies """ 
from outils import * 
import os,time 
from config import *

class Synthese :

	def syntheseHeure (self):
		temps_tab = time.localtime()
		heures = str(temps_tab[3])
		minutes = str(temps_tab[4])
		flag = 0
		if heures == "0":
		    heures = "minuit"
		    flag = flag + 2
		if heures == "12":
		    heures = "midi"
		    flag = flag + 2
		if minutes == "30":
		    minutes = "et demi"
		    flag = flag + 1
		if minutes == "0":
		    minutes = "pile"
		    flag = flag + 1
		if minutes == "15":
		    minutes = "et quart"
		    flag = flag + 1
		if minutes == "1":
		    minutes = "une"
		if heures == "1":
		    heures = "une"

		chaine =  "Il est " + heures  + " heures et " + minutes+" minutes."
		if flag == 1:
		    chaine =  "Il est " + heures  + " heures " + minutes
		if flag  == 2:
		    chaine =  "Il est " + heures  + " et " + minutes+" minutes."
		if flag == 3:
		    chaine =  "Il est " + heures  + " " + minutes
		self.synthese(chaine);

	def syntheseDate (self):
		pass;

	def syntheseVdm (self):
		pass;


		# Fonctions pour utiliser la synthese vocale

	def separation(self,chaine): # Cette fonction permet de separer une chaine de caractere en des portions de 80 caracteres maximum. On sépare si l'on peut sur un point, sinon sur deux points, sinon sur une virgule et sinon sur un espace
	    chaine = chaine.replace("\"","")
	    a = 1
	    liste = []
	    debut = 0
	    point = 0
	    deuxpoints = 0
	    virgule = 0
	    for i in range (0,len(chaine)):
	        if chaine[i]==".": # J'ai mis le point, le point d'exclamation et le point d'interrogation au meme niveau de force pour l' intonnation et donc la séparation. Ainsi l'indice du dernier point, point d'exclamation ou point d'interrogation est mis dans la meme variable.
	            point = i
	        if chaine[i]=="?": # J'ai mis le point, le point d'exclamation et le point d'interrogation au meme niveau de force pour l' intonnation et donc la séparation. Ainsi l'indice du dernier point, point d'exclamation ou point d'interrogation est mis dans la meme variable.
	            point = i
	        if chaine[i]=="!": # J'ai mis le point, le point d'exclamation et le point d'interrogation au meme niveau de force pour l' intonnation et donc la séparation. Ainsi l'indice du dernier point, point d'exclamation ou point d'interrogation est mis dans la meme variable.
	            point = i
	        if chaine[i]==":": # J'ai mis les deux points et les points virgules au meme niveau de force pour les intonnations et donc pour la séparation. Ainsi l'indice du dernier deux points ou points virgule est mis dans la meme variable.
	            deuxpoints = i
	        if chaine[i]==";": # J'ai mis les deux points et les points virgules au meme niveau de force pour les intonnations et donc pour la séparation. Ainsi l'indice du dernier deux points ou points virgule est mis dans la meme variable.
	            deuxpoints = i
	        if chaine[i]==",":
	            virgule = i
	        if chaine[i]==" ":
	            espace = i


	        if i == 80*a:
	            if point > 80*a - 55:
	                liste.append(chaine[debut:point])
	                debut = point + 1
	            elif deuxpoints > 80*a - 55:
	                liste.append(chaine[debut:deuxpoints])
	                debut = deuxpoints + 1
	            elif virgule > 80*a - 35:
	                liste.append(chaine[debut:virgule])
	                debut = virgule + 1
	            else :
	                liste.append(chaine[debut:espace])
	                debut = espace + 1
	            a = a +1

	    if len(chaine) % 80 !=0:
	        liste.append(chaine[debut:])
	    print(str(liste))
	    return(liste)

	def separation_retour_chariot(self,chaine):
	    liste = []
	    a = len(chaine)
	    debut = 0
	    for i in range (0,a):
	        if chaine[i] == "\n":
	            liste.append(chaine[debut:i])
	            debut = i + 1
	    if chaine [debut:] != "":
	        liste.append(chaine[debut:])

	    return liste

	"""def synthese(self,chaine): # Fonction qui est appelee pour utiliser la synthese vocale. Celle ci a un systeme de separation pour ne pas passer outre la limitation de 100 caracteres qu'impose la synthese de google, a un systeme qui permet d'encoder le texte a envoyer pour tous les caracteres speciaux
		path = ""#"/root/Donnees/"
		#print("Synthese")
		if Outils.testPresence("synthese.f") == 1:
		    Outils.ecrireFichier("synthese.f",chaine,1) # Le 1 en dernier parametre permet que la fonction Outils.ecrireFichier comprenne qu'il faut ajouter à la fin du fichier et non pas ecraser le fichier puis ecrire ce que l'on a a ecrire
		    #print("return")
		    return 0
		Outils.ecrireFichier("synthese.f","")
		self.syntheseLecture(chaine)

		while 1:
			if Outils.testPresence("synthese.f") == 0 :
				#print("return 0")
				return 0
			elif Outils.lireFichier("synthese.f") == "":
			    os.remove("synthese.f")
			    #print("return 0 - 2")
			    return 0
			else :
			    chaine2 = Outils.lireFichier("synthese.f")
			    os.remove("synthese.f")
			    liste = self.separation_retour_chariot(chaine2)
			    a = len(liste)
			    for i in range (0,a):
			    	#print("syntheseLecture1")
			    	self.syntheseLecture(liste[i])
		"""	        

	def synthese(self,chaine):
		# Synthese vocale avec le gestionnaire de ressources audio
		conf = Config ()
		id = conf.getId()
		a =  0
		while a != 1:
			a = conf.setLockAudio(True,id)
		self.syntheseLecture(chaine)

		conf.setLockAudio(False,id)


	def syntheseLecture(self,chaine):
		print("synthese lecture")
		liste = self.separation(chaine)
		a = len(liste)
		for i in range (0,a):
		    chaine2 = self.encode_url_q(liste[i])
		    chaine2 = "mpg321 -q -g 500 \"http://translate.google.com/translate_tts?client=tw-ob&tl=fr&ie=UTF-8&q="+chaine2+ "\""
		    os.system(chaine2)
		    time.sleep(0.75) # Ce délais a été instauré afin qu'il n'y ai pas trop de requetes au serveur google dnas un délais petit. Si c'est le cas, le serveur de google refuse certaines connexions ...

	def encode_url_q(self,chaine): # Fonction qui permet d'encoder quelque chose que l'on souhaite envoyer à internet en parmètres
		chaine = chaine.replace(" ","%20")
		chaine = chaine.replace("'","%27")
		chaine = chaine.replace(",","%2C")

		chaine = chaine.replace("é","%C3%A9")
		chaine = chaine.replace("è","%C3%A8")
		chaine = chaine.replace("à","%C3%A0")
		chaine = chaine.replace("ê","%C3%AA")
		chaine = chaine.replace("?","%3F")
		chaine = chaine.replace("@","%40")
		return chaine


#a = Synthese()
"""a = Synthese();
a.synthese("zbeub zbeub");
print("zbeub")"""

#a= Synthese();
#while True:
#a.synthese("Fayçal t'es trop beau");
