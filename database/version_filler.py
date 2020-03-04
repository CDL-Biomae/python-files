from tools import QueryScript
import env

def create_version_table():
    QueryScript(f"DROP TABLE IF EXISTS version; CREATE TABLE version (id INT AUTO_INCREMENT PRIMARY KEY, date VARCHAR(255), comment VARCHAR(255))").execute(True)
    
def create_new_version(date=None, comment=None):
    query = QueryScript(f" INSERT INTO version (date, comment) VALUES (%s, %s)")
    
    query.setRows([(date,comment)])
    query.executemany(True)


def run(cas, date, comment):
    ## On a 3 cas pour les requêtes SQL
    # Cas 1: 'première_version'
    # Cas 2: 'update_version'
    # Cas 3: 'nouvelle_version'

    ## Cas 1: Création et remplissage de la base de données
    if cas == 1:
        create_version_table()
        create_new_version()

    ## Cas 2: Mise à jour de la dernière version connue
    if cas == 2:
        pass  # On a rien à faire quand la version ne change pas

    ## Cas 3: Ajout d'une nouvelle version
    if cas == 3:
        create_new_version(date, comment)
