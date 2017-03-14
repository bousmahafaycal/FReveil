# FReveil
Ce projet a été développé par Fayçal Bousmaha.


## Introduction
### Le concept
Ce projet consiste en la création d'un réveil intelligent alliant informatique et électronique et dont on peut étendre les fonctionnalités via un système de modules 
qui peuvent être développés par des développeurs tiers. 
Le FReveil permet de donner une meilleure expérience de réveil qu'un réveil classique. 
Grace aux technologies utilisées, il peut donner des informations à l'oral ou intéragir avec le monde réel.


Chaque rappel est constitué de 2 parties :
- une pemière où les modules appelés lors de cette partie sont lancés en boucle jusqu'à ce que l'utilisateur "appuie" sur le bouton
- une seconde où les modules sont lancés après que l'utilisateur "ait appuyé" sur le bouton


Un appui sur le bouton n'est pas forcément physique. On peut simuler l'appui sur le bouton via l'application Android ou via l'interface
de configuration du FReveil. Deux modes existent dans ce réveil : 
- le mode présent
- le mode absent


A chaque fois que l'utilisateur sort de chez lui, il doit passer le réveil en mode absent (il peut le faire l'application Android ou 
l'interface de configuration, un bouton physique sera ultérieurement déployé). Les modules peuvent récuperer le mode dans lequel on est 
et adapté leur comportement en fonction. Par exemple, on pourrait imaginer qu'au lieu de donner une information à l'oral, le module
enverrait une notification sur le téléphone de l'utilisateur si le mode actuel est le mode absent.

### Contexte de création
C'est un projet personnel que j'ai réalisé seul. 
Mes parents souhaitant que je me lève seul, il me fallait trouver une solution pour me réveiller.



Souhaitant me faire accepter à la licence CDAISI de Valenciennes, et ayant lu sur internet qu'ils recrutaient 
des personnes sachant "bricoler" de leur coté, j'ai  décidé de montrer certaines de mes compétences informatiques via ce projet.


Me rappelant que j'avais déja réaliser un réveil pour mon ancien assistant virtuel (pas encore mit sur github), j'ai décidé de recréer
un réveil. Cette fois-ci, il devrait toutefois être de meilleur qualité. 
J'ai alors tout recommencer depuis le début et je l'ai recoder plus "proprement". 
Cette fois, il peut gérer de l'éléctronique. 
En effet, dans l'ancien réveil, il fallait que je me connecte chaque matin en ssh pour pouvoir l'arreter. 
Via un bouton physique permettant d'arreter la phase ou le réveil sonne en boucle, cela ne sera plus nécéssaire. 


De plus, il pourra être rapidement améliorable par des développeurs tiers. 
Pour cela, un système de modules a été réalisé. 
Chaque développeur peut créer son propre module (via le FReveilModuleCreator : <https://github.com/bousmahafaycal/FReveilModuleCreator>). 
On peut ensuite facilement ajouter son propre module au FReveil (un tuto est disponible ci-dessous dans la section Tester le FReveil).


## Application Android
Une application Android a été développé afun de pouvoir gérer le FReveil. En voici le lien :  
<https://github.com/bousmahafaycal/FReveilAndroid>

## Arduino
Le FReveil gérant l'éléctronique, suivez le lien ci-dessous pour voir comment la mettre en place :  
<https://github.com/bousmahafaycal/FReveilArduino>

## Les modules
Voici une liste des modules existant (mise à jour du 14/03/2017) :
- FReveil_synthese : <https://github.com/bousmahafaycal/FReveil_synthese>
- FReveil_synthese_heure : <https://github.com/bousmahafaycal/FReveil_synthese_heure>
- FReveil_synthese_meteo : <https://github.com/bousmahafaycal/FReveil_synthese_meteo>
- FReveil_musique : <https://github.com/bousmahafaycal/FReveil_musique>
- FReveil_citation : <https://github.com/bousmahafaycal/FReveil_citation> 


Si vous souhaitez créer votre propre module, je vous invite à consulter le lien suivant : 
<https://github.com/bousmahafaycal/FReveilModuleCreator>).

## Tester le FReveil
Dans un premier temps, vous devez cloner le projet sur votre disque dur.

### Ajouter un module
Pour ajouter un module, vous devez (pour le moment) obligatoirement le mettre sur votre disque dur.
Les modules douvent obligatoirement être créer via le FReveilModuleCreator :   
<https://github.com/bousmahafaycal/FReveilModuleCreator>  


Ensuite, vous devez lancer l'interface de configuration avec la commande suivante :  


`
python3 interface_config.py
`


Enfin, laissez vous guider par les instructions afficher à l'écran.

### Lancer le FReveil
Pour lancer le FReveil, il suffit de lancer la commande suivante : 


`
python3 lancement.py
`

### Ajouter un rappel
Pour ajouter un rappel, vous pouvez passer par l'application Android (<https://github.com/bousmahafaycal/FReveilAndroid>) ou bien utiliser l'interface en console via la commande suivante : 


`
python3 interface_reveil.py
`

Enfin, laissez vous guider par les instructions afficher à l'écran.


## A améliorer
- Système de log
- Lancer une partie d'un module en arrière plan dès le lancement du rappel.
- Sécurisation : Crypter les échanges serait une bonne idée afin d'éviter que quelqu'un s'introduisant dans le réseau local puisse
supprimer les rappels facilement.
- Interface graphique Windows, Mac & Linux (avec capacité de se connecter à distance au serveur)
- Permettre à chaque module d'utiliser le serveur
- Permettre à chaque module d'utiliser l'éléctronique
- Création d'un blog et d'une communauté autour du projet
- Créer plus de modules notamment éléctronique (par exemple, un module qui fait le café/chocolat)
- Création d'un store de modules (comme le Google Play mais pour les modules du FReveil)
- Ajouter une autre partie à ce réveil (la partie compréhension et réponse) afin de créer un assistant virtuel complet facilement améliorable
- Ajouter la possibilité de créer un rappel qui se lancera immédiatement
- Créer un système de template de rappel : en ouvrant un template, on peutavoir un certain nombre de commandes 
déja rempli ce qui facilite la création d'un  rappel.
- Permettre la gestion du FReveil via internet




## Photos
### Première photo

### Seconde photo
