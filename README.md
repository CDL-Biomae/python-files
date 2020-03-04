### Description du fonctionnement de l'application 

Pour lancer le programme, il faut au préalable installer les dépendances indiquées dans requires.txt.
Pour les installer, écrire les commandes suivantes dans un invite de commandes :
```
pip install --upgrade pip
pip install -r requires.txt
```
Assurez-vous d'avoir le fichier env.py dans le même dossier que requires.txt

## Remplissage de la base de données

Les coordonnées de vos bases de données sont précisées dans le fichier env.py sous les noms DATABASE_RAW (données brutes) et DATABASE_TREATED (données traitées) ... Il faut ajouter les différents identifiants et adresses IP à cet endroit

Pour remplir la base de données par les références et les résultats des moyennes de températures et autres dates clés, il faut avoir le fichier reference.xlsx dans le dossier principal (le même que celui contenant requires.txt)
Pour inforamtion : les différents noms de colonne du excel ne doivent pas changer car le remplissage est calibré sur les noms et le nombre de colonne précisé à la fin du projet Digital Lab de 2020.

Ensuite lancer la commande suivante :
```
python database.py
```
Si aucun message d'erreur n'est apparu, la base de données a été remplie avec succès !!


## Création des livrables excel et word

L'écriture des différents livrables se fait à partir du fichier main.py du dossier report.
Pour l'appeler il suffit de l'importer et lui donner un nom de campagne ou de contrat:

Dans create_xl_annexes.py
```
from report import main
main(<NOM DE/DES CAMPAGNE/S OU CONTRAT/S>)
```

## Création du Rapport d'expérimentation (Word) - Application

Pour créer un rapport d'expérimentation, il faut entrer le nom de la campagne et faire ajouter. Il est possible d'en ajouter plusieurs, que l'on voit en dessous. On précise en cochant ou non la case "Agence de l'eau" si c'en est une, la case étant coché initialement. Ensuite, on choisit la version que l'on souhaite utiliser pour les références, la dernière étant sélectionnée par défaut. Ensuite, on précise dans le champ "Numéro de la campagne", le numéro de celle-ci dans l'année. Si rien n'est renseigné, il y aura des "XX" à la place. Ce choix s'applique pour tous les rapports sélectionnés, donc si ce nombre est différent pour chacun, il faut les lancer un par un.
Puis on coche "Rapport d'expérimentation (Word)". On peut choisir ensuite le dossier de destinatation où sera enregistré le rapport, et le dosser où sont les photos. 
Dans le dossier il faut qu'il y ait des dossiers nommés en fonction d'un point de mesure (ex : AG-003-01-01-01), et que dans chacun de ces dossiers il y ait 4 photos, de 4 natures différentes (amont, aval, panorama, zoom). Les photos doivent respecter la nomenclature suivant : "stepXX_PDA1_AG-003-01-01-01_Amont_5445664_65454.png". Les éléments importants sont la séparation par des Underscores (_, touche 8), que le 3e élément (ainsi séparé) soit la référence du point de mesure (ex : AG-003-01-01-01) et le 4e soit le point de vue de la photo (amont, aval, panorama, zoom). 
Si on oublie de renseigner ces dossiers, lorsque l'on clique sur lancer, les fenêtres de sélection s'ouvriront, d'abord pour choisir la destination d'enregistrement, puis le dossier de photos.


##  Création du Rapport d'expérimentation (Word) - Comppréhension du code

Par ailleurs, pour faire les cartes il faut un compte sur Mapbox, lorsque ceci est fait il faut changer la variable 'ACCESS_TOKEN_MAPBOX' dans env.py par la clef du compte. Celle-ci se trouve sur le site Mapbox.com, dans Account, il faut copier la Default public token.