from tools import QueryScript
import env

def create_version_table():
    QueryScript(f" CREATE TABLE version (id INT AUTO_INCREMENT PRIMARY KEY, date VARCHAR(255), comment VARCHAR(255))").execute()
    
def new_version(date=None, comment=None):
    query = QueryScript(f" INSERT INTO version (date, comment) VALUES (%s, %s)")
    
    query.setRows([(date,comment)])
    query.executemany(True)