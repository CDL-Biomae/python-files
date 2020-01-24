import xlrd 
from query import Query

file_name = ("AG-003-01_Macros.xlsm") 

def run():
    
  # To open Workbook 
  wb = xlrd.open_workbook(file_name) 


  # Constants from r2 sheet
  sheet = wb.sheet_by_name('r2') 

  r2_constant_table = Query(script="DROP TABLE IF EXISTS r2_constant; CREATE TABLE r2_constant (id INT AUTO_INCREMENT PRIMARY KEY, nature VARCHAR(255), name VARCHAR(255), value VARCHAR(255))")
  r2_constant_table.execute()
  SQL_request = "INSERT INTO r2_constant (id, nature, name, value) VALUES (%s, %s, %s, %s)"
  values = []

  for i in range(14) :
    if(sheet.cell_value(4+i, 14)):
      values.append((i+1,"alimentation",str(sheet.cell_value(4+i, 13)),sheet.cell_value(4+i, 14)))

  for i in range(6) :
    values.append((i+15,"AChE",str(sheet.cell_value(20+i, 13)),sheet.cell_value(20+i, 14)))
  for i in range(21) :
    if(sheet.cell_value(28+i, 14)):
      values.append((i+21,"Repro",str(sheet.cell_value(28+i, 13)),sheet.cell_value(28+i, 14)))

  r2_constant_table.setScript(SQL_request)
  r2_constant_table.setRows(values)
  r2_constant_table.executemany()






  # Threshold from r2 sheet
  r2_threshold_table = Query(script="DROP TABLE IF EXISTS r2_threshold; CREATE TABLE r2_threshold (id INT AUTO_INCREMENT PRIMARY KEY, parameter VARCHAR(255), population VARCHAR(255), type VARCHAR(255), time VARCHAR(255), threshold VARCHAR(255), unit VARCHAR(255), rule VARCHAR(255), meaning VARCHAR(255), version VARCHAR(255))")
  r2_threshold_table.execute()
  SQL_request = "INSERT INTO r2_threshold (id, parameter, population, type, time, threshold, unit, rule, meaning, version) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
  values = []

  for i in range(3,40) :
    if(sheet.cell_value(i, 1)):
      values.append((i-2,sheet.cell_value(i,1),sheet.cell_value(i,2),sheet.cell_value(i,3),sheet.cell_value(i,4),sheet.cell_value(i,5), sheet.cell_value(i,6),sheet.cell_value(i,7),sheet.cell_value(i,11), sheet.cell_value(i,12)))

  r2_threshold_table.setScript(SQL_request)
  r2_threshold_table.setRows(values)
  r2_threshold_table.executemany()



  # Information from r3 sheet
  sheet = wb.sheet_by_name('r3')
  r3_table = Query(script="DROP TABLE IF EXISTS r3; CREATE TABLE r3 (id INT AUTO_INCREMENT PRIMARY KEY, unit VARCHAR(255), sandre VARCHAR(255), parameter VARCHAR(255), NQE VARCHAR(255), 7j_threshold VARCHAR(255), 7j_graduate_25 VARCHAR(255), 7j_graduate_50 VARCHAR(255), 7j_graduate_75 VARCHAR(255),  21j_threshold VARCHAR(255), 21j_graduate_25 VARCHAR(255), 21j_graduate_50 VARCHAR(255), 21j_graduate_75 VARCHAR(255), case_number VARCHAR(255), familly VARCHAR(255))")
  r3_table.execute()
  SQL_request = "INSERT INTO r3 (id, unit, sandre, parameter, NQE, 7j_threshold, 7j_graduate_25, 7j_graduate_50, 7j_graduate_75, 21j_threshold, 21j_graduate_25, 21j_graduate_50, 21j_graduate_75, case_number, familly) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
  values = []

  for i in range(2,346):
    values.append((i,sheet.cell_value(i,0),sheet.cell_value(i,1),sheet.cell_value(i,2),sheet.cell_value(i,3),sheet.cell_value(i,4),sheet.cell_value(i,5), sheet.cell_value(i,6),sheet.cell_value(i,7),sheet.cell_value(i,8),sheet.cell_value(i,9),sheet.cell_value(i,10),sheet.cell_value(i,11), sheet.cell_value(i,12),sheet.cell_value(i,13)))

  r3_table.setScript(SQL_request)
  r3_table.setRows(values)
  r3_table.executemany()