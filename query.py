import mysql.connector
from mysql.connector import errorcode



def query_function(elements_queried,table,limit=1000) :
  
  try:
    connection = mysql.connector.connect(user='cdl', password='Centrale_Digital_Lab',
                                  host='192.168.1.61',
                                  database='biomae')
    
    
    cursor = connection.cursor()
    query = ("SELECT {} FROM {} LIMIT {}".format(
      elements_queried, table, limit))
    cursor.execute(query)
    output = []
    for ligne in cursor:
        print(ligne[0])
    
    return output

  except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
      print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
      print("Database does not exist")
    else:
      print(err)

  
  cursor.close()
  connection.close()