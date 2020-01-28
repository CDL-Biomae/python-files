import env
import mysql.connector
from mysql.connector import errorcode

class Query:
  
  def __init__(self, table=None, column="*", limit=None, group=None, filtre=None, interval=None, distinct=False):
    self.distinct = distinct
    if table!=None :
      self.table = table
    else :
      self.table = None
      self.error()
    if column==None :
      self.column = "*"
    else :
      self.setColumn(column)
    self.script = script
    self.rows = rows
    self.setFiltre(filtre)
    self.group = group
    self.limit = limit
    self.interval = interval
  
  def __str__(self) :
    if(self.script==None):
      SQL_request = "SELECT "
      SQL_request += "DISTINCT "*self.distinct+self.column+" FROM "+self.table
      
      if(self.filtre or self.interval) :
        SQL_request +=" WHERE "
        if(self.filtre and self.interval) :
          SQL_request += self.filtre + " AND " + self.interval[0] + " BETWEEN " + self.interval[1] + " AND " + self.interval[2]
        elif(self.filtre) :
          SQL_request += self.filtre
        else :
          SQL_request += self.interval[0] + " BETWEEN " + self.interval[1] + " AND " + self.interval[2]
      if(self.group):
        SQL_request += " GROUP BY " + self.group
      if(self.limit):
        SQL_request += " LIMIT "+self.limit
  
      return SQL_request
    else :
      return self.script
  def error(self):
    print('ERROR : table argument is missing')
   
  def getTable(self):
    return self.table
  
  def setTable(self, table):
    self.table=table

  def getDistinct(self):
    return self.distinct
  
  def setDistinct(self, distinct):
    self.distinct=distinct
    
  def getColumn(self):
    return self.column
  
  def setColumn(self, column):
    if(len(column)>=0 and isinstance(column, list)):
      self.column=column[0]
      for element in column[1:] :
        self.column+=", "+element
    else : 
      self.column=column
      
  def getLimit(self):
    return self.limit
  
  def setLimit(self, limit=None):
    self.limit=limit

  def getGroup(self):
    return self.group
  
  def setGroup(self, group=None):
    self.group=group

  def getInterval(self):
    return self.interval
  
  def setInterval(self, interval=None):
    self.interval=interval
    
  def getFiltre(self):
    return self.filtre
  
  def setFiltre(self, filtre=None):
    if(filtre!=None and len(filtre)>=0 and isinstance(filtre, list)):
      self.filtre=filtre[0]
      for element in filtre[1:] :
        self.filtre+=" AND "+element
    else : 
      self.filtre=filtre
      
  def execute(self) :
    if self.script==None and self.table==None :
      return []
    try:
      connection = mysql.connector.connect(user=env.DATABASE_USER, password=env.DATABASE_PASSWORD,
                                    host=env.DATABASE_IP,
                                    database='biomae')
      
      cursor = connection.cursor()

    except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
      elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
      else:
        print(err)
        
    query = (self.__str__())
    
    cursor.execute(query)
    
    output = []
    
    for ligne in cursor:
      if (len(ligne)==1) :
        output.append(ligne[0])
      else :
        output.append(ligne)
    
    cursor.close()
    connection.close()
    
    return output
  
  

class QueryScript(Query) :
  def __init__(self, script=None, rows=None):
    if script!=None:
      self.script = script
    else :
      self.errorScript()
      self.script = 
    self.rows = rows

  def errorScript():
    print('Script description is missing')
  
  def getRows(self):
    return self.rows
  
  def setRows(self, rows):
    self.rows=
    
  def getScript(self):
    return self.script
  
  def setScript(self, script=None):
    self.script=script
    
  def executemany(self) :
    if self.script!=None and self.rows==None :
      return "Rows argument is missing"
    if self.script==None  :
      return "Script argument is missing"
    try:
      connection = mysql.connector.connect(user=env.DATABASE_USER, password=env.DATABASE_PASSWORD,
                                    host=env.DATABASE_IP,
                                    database='biomae')
      
      cursor = connection.cursor()
        
      query = (self.__str__())
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