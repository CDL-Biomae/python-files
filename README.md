# Description du fonctionnement de l'application utilisée par Biomae pour gérer ces données et la création de livrable

Assurez-vous d'avoir le fichier env.py dans le même dossier que requires.txt. Il doit figurer dans env.py les identifiants de la base de données à laquelle vous souhaitez vous connectez. DATABASE_USER, DATABASE_PASSWORD ET DATABASE_IP sont ces identifiants.
DATABASE_RAW et DATABASE_TREATED sont fournis par Zabé comme étant le nom de base respectivement de la base de données brutes et traitées.

# Application Centrale Digital App

## Onglet créateur de livrables

Pour lancer l'application, écrivez dans un terminal de commande la ligne suivante :
```
python app.py
```
Cela peut prendre de 2sec à 30 sec en fonction de la vitesse de votre appareil.

Vous arrivez donc sur une interface qui vous permet de créer des livrables. 
Pour ajouter une campagne dans la création de livrable, écrivez son nom du type 'AG-003-01', puis "Ajouter" cette référence (la touche Enter fonctionne aussi). Une sécurité est placée pour éviter les erreurs : si la référence précisée n'est pas dans la base de données ou a déjà été ajoutée, rien ne se passera.
Un menu déroulant permet de choisir la version de la base de données traitées voulue pour la génération de rapport. Par défaut, la version choisie est la dernière en date. 
Le bouton "Lancer" apparaît lorsqu'une option Excel ou Word est sélectionnée. Les différentes options qui en dépendent s'affichent lorsque l'option du livrable voulu est choisie. Le dossier de destination correspond à l'endroit où vont atterrir les livrables. La source des photos correspond au dossier contenant les phtos nécessaires.

### Précision sur l'onglet word

Pour créer un rapport d'expérimentation, il faut entrer le nom de la campagne et faire ajouter. Il est possible d'en ajouter plusieurs, que l'on voit en dessous. On précise en cochant ou non la case "Agence de l'eau" si c'en est une, la case étant coché initialement. Ensuite, on choisit la version que l'on souhaite utiliser pour les références, la dernière étant sélectionnée par défaut. Ensuite, on précise dans le champ "Numéro de la campagne", le numéro de celle-ci dans l'année. Si rien n'est renseigné, il y aura des "XX" à la place. Ce choix s'applique pour tous les rapports sélectionnés, donc si ce nombre est différent pour chacun, il faut les lancer un par un.

Puis on coche "Rapport d'expérimentation (Word)". On peut choisir ensuite le dossier de destinatation où sera enregistré le rapport, et le dosser où sont les photos. 

Dans le dossier il faut qu'il y ait des dossiers nommés en fonction d'un point de mesure (ex : AG-003-01-01-01), et que dans chacun de ces dossiers il y ait 4 photos, de 4 natures différentes (amont, aval, panorama, zoom). Les photos doivent respecter la nomenclature suivant : "stepXX_PDA1_AG-003-01-01-01_Amont_5445664_65454.png". Les éléments importants sont la séparation par des Underscores (_, touche 8), que le 3e élément (ainsi séparé) soit la référence du point de mesure (ex : AG-003-01-01-01) et le 4e soit le point de vue de la photo (amont, aval, panorama, zoom). 

Si on oublie de renseigner ces dossiers, lorsque l'on clique sur lancer, les fenêtres de sélection s'ouvriront, d'abord pour choisir la destination d'enregistrement, puis le dossier de photos.

Par ailleurs, pour faire les cartes il faut un compte sur Mapbox, lorsque ceci est fait il faut changer la variable 'ACCESS_TOKEN_MAPBOX' dans env.py par la clef du compte. Celle-ci se trouve sur le site Mapbox.com, dans Account, il faut copier la Default public token.

### Lancement

Lorsque tous les informations désirées sont sélectionnées, appuyer sur le bouton "Lancer". Cela va geler l'application tant que le(s) livrable(s) ne sont pas terminés d'être créés. 
L'avancée de la création des livrables est maintenant affichée dans la console que vous avez lancé pour allumer l'application (ainsi que les éventuelles erreurs).

## Onglet Gestionnaire de base de données

Cet onglet permet de changer de mettre à jour la base de données traitées ou de changer totalement de version.
Si vous avez connaissance d'ajout de données brutes (point de mesure, résultats divers, modifications ...) vous pouvez rafraîchir la base de données traitées avec le bouton "Rafraîchir la base de données traitées" qui gèlera l'application le temps de mettre à jour l'entièreté des données traitées. Cela va automatiquement modifier la dernière version inscrite. 
Si vous avez besoin de créer une nouvelle version, veuillez renseigner le ficher excel contenant les références de calculs et de seuils dans en cliquant sur "Choisir le fichier excel de référence". Cela va automatiquement inscrire les deux informations possibles de la version à savoir la date (celle du jour actuel) ainsi qu'un éventuel commentaire que vous voulez préciser à la nouvelle version. Il ne reste plus qu'à cliquer sur "Ajouter cette version" qui remplira dans la base de données traitées une nouvelle série de données traitées calculées à partir des références précisées ave le fichier excel. Cela peut prendre une dizaine de minutes en fonction de la vitesse de connection de vogtre appareil.


# Prérequis avant lancement de l'application

Pour lancer l'application, il faut au préalable avoir le dossier sur son ordinateur. Pour cela deux choix possibles :
- l'avoir sur une clé et le copier coller
- cloner le projet de github. Pour cela, il faut télécharger git sur son appareil et lancer dans une invite de commande :
```
git clone https://github.com/CDL-Biomae/python-files
```
Cela va créer le dossier là où l'invite de commande a été lancé. Ensuite il faut placer le fichier env.py qui ne peut se transmettre par github mais par particulier. 
Dans ce même fichier ajouter les coordonnées de la base de données telle que vous le souhaitez pour vous connectez (les variables commençant par DATABASE).
A partir de ce moment, pour lancer le programme, il faut au préalable installer les dépendances indiquées dans requires.txt.
Pour les installer, écrire les commandes suivantes dans un invite de commandes (il faut avoir au minimum python installé sur votre appareil ainsi que dans le PATH):
```
pip install --upgrade pip
pip install -r requires.txt
```