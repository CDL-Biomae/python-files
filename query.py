import mysql.connector
from mysql.connector import errorcode

class Query:
  
  def __init__(self, table=None, column="*", limit=None):
    if column==None :
      self.column = "*"
    else :
      self.setColumn(column)
    self.table = table
    self.limit = limit
  
  def __str__(self) :
    if self.limit==None :
      return "SELECT {} FROM {}".format(
      self.column, self.table)
    else :
      return "SELECT {} FROM {} LIMIT {}".format(
      self.column, self.table, self.limit)

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

    