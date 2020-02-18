### Description du fonctionnement de l'application 

Pour lancer le programme, il faut au préalable installer les dépendances indiquées dans requires.txt.
Pour les installer, écrire les commandes suivantes dans un invite de commandes :
```
pip install --upgrade pip
pip install -r requires.txt
```
Assurez-vous d'avoir le fichier env.py dans le même dossier que requires.txt

## Remplissage de la base de données

Les coordonnées de votre base de données sont précisées dans le fichier env.py sous les noms DATABASE ... Il faut ajouter les différents identifiants et adresses IP à cet endroit

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