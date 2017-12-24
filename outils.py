# -*- coding: utf-8 -*-
"""
Created on Sat Oct  1 15:37:38 2016
@author: Fayçal Bousmaha


Contient la classe Outils
Fonctions dispos :
    - maxColonne (liste,a)
    - idMaxColonne(liste, a):
    - compareDeuxMots (mot, mot2)
    - compareMotif(chaine,motif)
    - recupereBalise(chaine, baliseOuvrante, nbOuvrante, baliseFermante, nbFermante, crochet)
    - findNb (chaine, recherche, debut, nb)
    - constitueBalise(nom,balise)
    
"""
import os
from shutil import copytree, ignore_patterns, rmtree

class Outils:
    
    # Fonction qui renvoie le max d'un tab à double dimension dans la colonne donnée
    def maxColonne(liste,a):
        max = liste[0][a];
        for i in range (0,len(liste)):
            if (liste[i][a] > max ):
                max = liste [i][a];
        return max;
    
    
    """ Fonction qui renvoie l'id du max d'un tab à double dimension dans la colonne donnée """
    def idMaxColonne(liste, a):
        id = 0;
        max = liste[0][a];
        for i in range (0,len(liste)):
            if (liste[i][a] > max ):
                max = liste [i][a];
                id = i;
        return id;
        
    """
    Fonction qui compare deux mots selon la définition d'Olivier en 1993.
    La fonction compareMotif est inutile sauf si on souhaite gagner en rapidité, 
    or ici je n'utilises pas l'algo le plus rapide. Un simple find (ou indexOf en C# ou en java)
    aurait permis d'éviter la fonction compareMotif.
    """
    def compareDeuxMots (mot, mot2):
        interm = mot;
        if (len(mot2) > len(mot)):
            mot = mot2;
            mot2 = interm;
            
        maxi = 0;
        compteur = 0;
        for i in range(0,len(mot2)):
            for i2 in range (2,len (mot2)):
                    interm = mot2[i:i2];
                    if (Outils.compareMotif(mot, interm)):
                        compteur = len(interm);

                    if (compteur > maxi):
                        maxi = compteur;
                        #print("interm : " + interm);
                    
            compteur = 0;
        
        return maxi;
    
    """ 
    Fonction qui renvoie True si le motif est présent dans la chaine, et False sinon.
    Fonction pas opti, voir livre "Programmation efficace" de Christophe Dürr.
    """
    def compareMotif(chaine,motif):
        indice = 0;
        chaine = chaine[indice:];
        for i in range (0,len(chaine) - len(motif) + 1):
            for i2 in range (0, len(motif)):
            
                if (chaine[i + i2] != motif[i2]):
                    break;

                if (i2 == len(motif) - 1):
                    return True;
            
        return False;
        
    """
    Fonction qui récupere ce qui est à l'interieur d'une balise
    
    ATTENTION : Voici des erreurs  fréquentes :
        - balise ouvrante doit etre sans le premier crochet : 
            ° Exemple : pour parler de la balise <b>, on met seulement "b"
        - idem pour la balise fermante
        - nbOuvrante commence à 1 et pas à 0
        - nbFermante idem
        - le nbFermante est compté à partir de la balise ouvrante utilisée.
        - crochet est un booleen
    """
    def recupereBalise(chaine, baliseOuvrante, nbOuvrante, baliseFermante, nbFermante, crochet):
        
        crochetOuvrant = "<";
        crochetFermant = ">";
        if (crochet):
            crochetOuvrant = "[";
            crochetFermant = "]";
        
        debut = Outils.findNb(chaine, crochetOuvrant + baliseOuvrante, 0, nbOuvrante);
        #print("debut : " + debut);
        chaine = chaine[debut:];
        debut = chaine.find(crochetFermant) + 1;
        #print("debut2 : " + debut);
        chaine = chaine[debut:];
        fin = Outils.findNb(chaine, crochetOuvrant + "/" + baliseFermante, 0, nbFermante);
        chaine = chaine[0:fin];
        return chaine;
    
    """
    Fonction qui cherche et envoie l'indice de l'occurence numéro nb de recherche dans chaine à 
    partir de la variable debut.
    
    ATTENTION : nb commence à 1
    """
    def findNb (chaine, recherche, debut, nb):
        a = 0;
        for i in range (0,nb):
            a = chaine.find(recherche, debut);
            debut = a + 1;
            

        
        return a;
        
        
    
    def recupereAttributBalise(chaine, baliseOuvrante, nbOuvrante, nomAttribut, crochet, 
                               guillemetSimple):
        
        crochetOuvrant = "<";
        crochetFermant = ">";
        if (crochet): 
            crochetOuvrant = "[";
            crochetFermant = "]";

        
        guillemet = "\"";
        if (guillemetSimple):
            guillemet = "'";
        

        debut = Outils.findNb(chaine, crochetOuvrant + baliseOuvrante, 0, nbOuvrante)+1;
        chaine = chaine[debut:];
        fin = chaine.find(crochetFermant);
        chaine = chaine[:fin];

        debut = chaine.find(nomAttribut);
        chaine = chaine[debut:];
        debut = chaine.find(guillemet)+1;
        chaine = chaine[debut:];
        fin = chaine.find(guillemet);
        chaine = chaine[:fin];
        

        return chaine;
        
        
    def recupereBaliseAuto(chaine, baliseOuvrante, nbOuvrante, baliseFermante = "", crochet = False):
        if baliseFermante == "":
            baliseFermante = baliseOuvrante
        # NbOuvrante commence à 1
        crochetOuvrant = "<";
        crochetFermant = ">";
        if (crochet): 
            crochetOuvrant = "[";
            crochetFermant = "]";


        nb = 1;
        nbTotal = 0;
        test = False;
        chaine2 = "";
        while (nb != 0):
            if (test == False):
                nb = 0;
                test = True;
                
            chaine2 = Outils.recupereBalise(chaine, baliseOuvrante, nbOuvrante, baliseFermante,nbTotal+1, crochet);
            nb = Outils.compter(chaine2,crochetOuvrant+baliseFermante) - Outils.compter(chaine2, crochetOuvrant+"/"+baliseFermante);
            nbTotal = Outils.compter(chaine2, crochetOuvrant + baliseFermante);

        return chaine2;


    # Fonction permettant de constituer une balise
    def constitueBalise(balise, chaine, crochet = False):
        delDeb = "<"
        delFin = ">"

        if (crochet):
            delDeb = "["
            delFin = "]"

        chaine = delDeb+balise+delFin+chaine+delDeb+"/"+balise+delFin
        return chaine


   

        
    # Fonction permettant de compter le nombre d'occurences dans une chaine de caracteres.   
    def compter(chaine, recherche):
        return chaine.count(recherche);

    # Fonction retournant une liste des fichiers contenu dans un dossier
    def getDossier(path):
        liste = os.listdir(path)
        return liste


    # Fonction qui supprime un dossier ainsi que tout son contenu
    def supprimeDossier(path):
        rmtree(path)

    # Fonction créeant les dossier si ceux ci n'existent pas
    def creeDossier(path):
        if (not Outils.testPresenceRep(path)):
            os.makedirs(path)

    # Fonction permettant de copier un dossier à un autre endroit
    def copieDossier (cible, destination):
        copytree(cible, destination)
        
    # Fonction permettant de lire le contenu d'un fichier.
    def lireFichier(endroit_fichier): # Fonction qui renvoie le contenu du fichier en chaine de caractere
        mon_fichier = open(endroit_fichier, "r")
        chaine = mon_fichier.read()
        mon_fichier.close()
        return chaine

    # Fonction permettant d'écrire dans un fichier, 
    # mettre le troisième paramètre à 1 pour activer le mode ajout
    def ecrireFichier(endroit_fichier,chaine,ajout = 0): # Fonction qui ecrit une chaine dans un fichier
        if ajout == 1 and Outils.testPresence(endroit_fichier) == 1 and Outils.lireFichier(endroit_fichier)!= "": # Si l'on souhaite le mode ajout, que le fichier existe et qu'il ne soit pas nulle alors :
            chaine = Outils.lireFichier(endroit_fichier) + "\n"+ chaine # On recupere le contenu du fichier, on ajoute un retour chariot et la chaine precise en parametre.
    
        mon_fichier = open(endroit_fichier, "w")
        mon_fichier.write(chaine)
        mon_fichier.close()
        return 1
        

    # Fonction qui supprime un fichier
    def supprimerFichier(endroit_fichier):
        if Outils.testPresence(endroit_fichier):
            os.remove(endroit_fichier)
            return True
        return False

    # Fonction qui test la présence d'un fichier.
    def testPresence(endroit_fichier): # Teste la présence d'un fichier
        try :
            open(endroit_fichier,"r")
            return 1
        except:
            return 0

    # Fonction qui test la présence d'un répertoire
    def testPresenceRep(path):
        return os.path.isdir(path)


    def intInput(chaine=""):
        
        continuer = True
        while continuer:
            #if chaine != "":
                #print (chaine)
            a = input(chaine)
            try:
                b = int(a)
                continuer = False
            except:
                print()
                print("Merci de bien vouloir recommencer, un entier est attendu : ")

        return b


    def menu(question,liste,barre = True):
        # Fonction permettant de créer un menu selon une liste  de choix et une question
        print()
        if barre:
            print("----------------------------")
        continuer = True
        a = 0
        while continuer:
            print(question)
            for i in range(len(liste)):
                print(str(i+1)+" : "+liste[i])

            print()
            print("Merci de bien vouloir rentrer le nombre corrrespondant à votre choix :")
            a = Outils.intInput("Quel est votre choix ? ")

            if (a > 0 and a <= len(liste)):
                continuer = False
            else :
                print()
                print("Merci de bien vouloir recommencer !")

        if barre:
            print("----------------------------")
        return a-1


       


        
#print(Outils.compareDeuxMots("afc barcaa","bbbcasfccaa barcelone"));
#print(Outils.findNb("blabla","a",3,1));
#print(Outils.recupereAttributBalise("<b alla='aaa'>bbb</b>","b",1,"alla",False,True));
#print(Outils.recupereBaliseAuto("<b alla='aaa'>bbb</b>","b",1,"b",False));
#liste = [];
#liste.append([1,2,3]);
#liste.append([4,2,3]);
#liste.append([7,5,1]);
#
#print(Outils.maxColonne(liste,0));             
#print(Outils.idMaxColonne(liste,0));       

            
#chaine = "\r\n            <a href=\"/america-mg-sport-recife-m1273637\" onclick=\"return bcTrack.trackOnClick(this, { event : spTrack.keys.matchTitle, title : &#39;America MG - Sport Recife&#39;, &#39;Event Name&#39; : &#39;Br&#233;sil Campeonato&#39;, &#39;Match&#39; : &#39;America MG - Sport Recife_1273637&#39; , &#39;Sport&#39; : &#39;Football&#39; });\">America MG - Sport Recife</a>\r\n        \r\n"
#print(Outils.recupereBaliseAuto(chaine,"a",1,"a",False));

