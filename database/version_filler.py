from tools import QueryScript
from datetime import datetime
import env

def create_version_table():
    QueryScript("DROP TABLE IF EXISTS version").execute(admin=True)
    QueryScript(f"CREATE TABLE version (id INT AUTO_INCREMENT PRIMARY KEY, date VARCHAR(255), comment VARCHAR(255))").execute(admin=True)
    
def create_new_version(date=None, comment=None):
    query = QueryScript(f" INSERT INTO version (date, comment) VALUES (%s, %s)")
    
    query.setRows([(date, comment)])
    query.executemany(True)
    version = env.LATEST_VERSION()
    version_file = open("version.txt", "w")
    version_file.write(f"CHOSEN_VERSION={version}")
    version_file.close()


def update_version():
    new_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    QueryScript(f'UPDATE {env.DATABASE_TREATED}.version SET date="{new_date}" WHERE id={env.CHOSEN_VERSION()}').execute(admin=True)
    print(f'Updating version {env.CHOSEN_VERSION()} at {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')

def run(cas, date, comment):
    ## On a 3 cas pour les requêtes SQL
    # Cas 1: 'première_version'
    # Cas 2: 'update_version'
    # Cas 3: 'nouvelle_version'

    ## Cas 1: Création et remplissage de la base de données
    if cas == 1:
        create_version_table()
        create_new_version(date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    ## Cas 2: Mise à jour de la dernière version connue
    if cas == 2:
        update_version()

    ## Cas 3: Ajout d'une nouvelle version
    if cas == 3:
        create_new_version(date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), comment=comment)
