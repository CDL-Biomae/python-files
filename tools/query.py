import env
import mysql.connector
from mysql.connector import errorcode

class QueryScript() :
  '''
  Prend deux arguments facultatif: script et rows. script est la requête SQL désirée écrite en string. rows est une liste de tuples contenant les lignes qui peuvent être insérées dans une table.
  Pour lancer une requête du type SELECT lancer execute(). Si vous lancer DROP ou CREATE, lancer execute(admin=True) qui va spécifié que vous travailler sur la base de données brut.
  Si vous lancer une INSERT, lancer executemany() avec rows non nul.
  '''
  def __init__(self, script='', rows=None):
    if script!='':
      self.script = script
    else :
      self.errorScript()
      self.script = script
    self.rows = rows
  def __str__(self):
    return self.script
    
  def errorScript(self):
    print('Script description is missing')
  
  def getRows(self):
    return self.rows
  
  def setRows(self, rows):
    self.rows = rows
    
  def getScript(self):
    return self.script
  
  def setScript(self, script=None):
    self.script=script
    
  def execute(self, admin=False) :
    try:
      connection = mysql.connector.connect(user=env.DATABASE_USER, password=env.DATABASE_PASSWORD,
                                    host=env.DATABASE_IP, database=env.DATABASE_TREATED if admin else None)
      
      cursor = connection.cursor()

    except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
        return 
      elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
        return 
      else:
        print(err)
        return 
    
    query = (self.__str__())
    if not cursor:
      print("Database not connected")
      return
    cursor.execute(query)
    
    output = []
    
    for ligne in cursor:
      if (len(ligne)==1) :
        output.append(ligne[0])
      else :
        output.append(list(ligne))
    
    cursor.close()
    connection.close()
    
    return output
    
  def executemany(self, admin=False) :
    if self.script!=None and self.rows==None :
      return "Rows argument is missing"
    if self.script==None  :
      return "Script argument is missing"
    try:
      connection = mysql.connector.connect(user=env.DATABASE_USER, password=env.DATABASE_PASSWORD,
                                    host=env.DATABASE_IP, database=env.DATABASE_TREATED)
      
      cursor = connection.cursor()
        
      query = (self.__str__())
      if not admin :
        cursor.execute(f" SELECT max(id) FROM {env.DATABASE_TREATED}.version")
        version = tuple([element[0] for element in cursor])
        new_rows = [row + version for row in self.rows]
        self.setRows(new_rows)
        
      cursor.executemany(query, self.rows)
      connection.commit()
      
      print(cursor.rowcount, "was inserted.")

    except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
      elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
      else:
        print(err)

    return None