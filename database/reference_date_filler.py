from tools import QueryScript
import env


def fill_reference_date_table():
    '''Fonction remplissant la table de référence des dates, celle-ci ne sert pas mais permet de "traduire" lorsque l'on fait un appel à la date key_dates '''
    reference_date_table = QueryScript(
        f" DROP TABLE IF EXISTS reference_date; CREATE TABLE reference_date (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), step INT(11), barrel VARCHAR(255), version INT);")
    reference_date_table.execute(True)
    SQL_request = f" INSERT INTO reference_date (name, step, barrel, version) VALUES (%s, %s, %s, %s)"
    values = [("Transplantation Alimentation", 50, "R0"),
              ("Recuperation Alimentation", 60, "R7"),
              ("Lancement Alimentation", 20, None),
              ("Recuperation reprotoxicite", 140, "RN"),
              ("Arret Reprotoxicite", 170, None),
              ("Lancement Chimie", 50, "C0"),
              ("Recuperation Chimie", 100, "R21")]

    reference_date_table.setScript(SQL_request)
    reference_date_table.setRows(values)
    reference_date_table.executemany()


def run(cas):
    # On a 3 cas pour les requêtes SQL
    # Cas 1: 'première_version'
    # Cas 2: 'update_version'
    # Cas 3: 'nouvelle_version'

    # Cas 1: Création et remplissage de la base de données
    if cas == 1:
        fill_reference_date_table()

    # Cas 2: Mise à jour de la dernière version connue
    if cas == 2:
        pass  # Les références des dates clées ne change pas quand on update la table

    # Cas 3: Ajout d'une nouvelle version
    if cas == 3:
        pass  # Les références des dates clées ne change pas quand on ajoute une nouvelle version
