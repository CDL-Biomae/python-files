import mysql.connector
from mysql.connector import errorcode

class Query:
  
  def __init__(self, table=None, column="*", limit=None,filtre=None, interval=None):
    if column==None :
      self.column = "*"
    else :
      self.setColumn(column)
    self.setFiltre(filtre)
    self.table = table
    self.limit = limit
    self.interval = interval
  
  def __str__(self) :
    if self.limit==None and self.interval==None and self.filtre==None :
      return "SELECT {} FROM {}".format(
      self.column, self.table)
    elif self.limit!=None and self.interval==None and self.filtre==None :
      return "SELECT {} FROM {} LIMIT {}".format(
      self.column, self.table, self.limit)
    elif self.limit==None and self.interval!=None and self.filtre ==None :
      return "SELECT {} FROM {} WHERE {} BETWEEN {} AND {}".format(
      self.column, self.table, self.interval[0], self.interval[1], self.interval[2])
    elif self.limit!=None and self.interval!=None and self.filtre ==None :
      return "SELECT {} FROM {} WHERE {} BETWEEN {} AND {} LIMIT {}".format(
      self.column, self.table, self.interval[0], self.interval[1], self.interval[2], self.limit)
    elif self.limit==None and self.interval==None and self.filtre != None :
      return "SELECT {} FROM {} WHERE {}".format(
      self.column, self.table, self.filtre)
    elif self.limit==None and self.interval!=None and self.filtre != None :
      return "SELECT {} FROM {} WHERE {} AND {} BETWEEN {} AND {}".format(
      self.column, self.table, self.filtre, self.interval[0], self.interval[1], self.interval[2])
    elif self.limit!=None and self.interval==None and self.filtre != None :
      return "SELECT {} FROM {} WHERE {} LIMIT {}".format(
      self.column, self.table, self.filtre, self.limit)
    elif self.limit!=None and self.interval!=None and self.filtre != None :
      return "SELECT {} FROM {} WHERE {} WHERE {} BETWEEN {} AND {} LIMIT {}".format(
      self.column, self.table, self.filtre, self.interval[0], self.interval[1], self.interval[2], self.limit)

  def getTable(self):
    return self.table
  
  def setTable(self, table):
    self.table=table
    
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

  def getInterval(self):
    return self.interval
  
  def setInterval(self, interval=None):
    self.interval=interval

  def getFiltre(self):
    return self.filtre
  
  def setFiltre(self, filtre=None):
    if(len(filtre)>=0 and isinstance(filtre, list)):
      self.filtre=filtre[0]
      for element in filtre[1:] :
        self.filtre+=" AND "+element
    else : 
      self.filtre=filtre

  def execute(self) :
    if self.table==None :
      return "Table argument is missing"
    try:
      connection = mysql.connector.connect(user='cdl', password='Centrale_Digital_Lab',
                                    host='192.168.1.61',
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

    