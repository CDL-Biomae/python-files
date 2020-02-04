import xlrd 
from tools import QueryScript

file_name = "reference.xlsx"

def run():
  print("ouverture")
  # To open Workbook 
  wb = xlrd.open_workbook(file_name) 

  print("premiere feuille")
  # Constants from r2 sheet
  sheet = wb.sheet_by_name('r2') 

  r2_constant_table = QueryScript("DROP TABLE IF EXISTS r2_constant; CREATE TABLE r2_constant (id INT AUTO_INCREMENT PRIMARY KEY, nature VARCHAR(255), name VARCHAR(255), value FLOAT);")
  r2_constant_table.execute()
  SQL_request = "INSERT INTO r2_constant (nature, name, value) VALUES (%s, %s, %s)"
  values = []

  for i in range(14) :
    if(sheet.cell_value(4+i, 14)):
      values.append(("alimentation",str(sheet.cell_value(4+i, 13)),float(sheet.cell_value(4+i, 14))))

  for i in range(6) :
    values.append(("AChE",str(sheet.cell_value(20+i, 13)),float(sheet.cell_value(20+i, 14))))
  for i in range(21) :
    if(sheet.cell_value(28+i, 14)):
      values.append(("Repro",str(sheet.cell_value(28+i, 13)),float(sheet.cell_value(28+i, 14))))
  for i in range(20):
    values.append(("temperature_repro",str(sheet.cell_value(52+i, 13)),float(sheet.cell_value(52+i, 14))))

  r2_constant_table.setScript(SQL_request)
  r2_constant_table.setRows(values)
  r2_constant_table.executemany()



  # Threshold from r2 sheet
  r2_threshold_table = QueryScript("DROP TABLE IF EXISTS r2_threshold; CREATE TABLE r2_threshold (id INT AUTO_INCREMENT PRIMARY KEY, parameter VARCHAR(255), population VARCHAR(255), type VARCHAR(255), time VARCHAR(255), threshold FLOAT, unit VARCHAR(255), rule VARCHAR(255), meaning VARCHAR(255), version VARCHAR(255));")
  r2_threshold_table.execute()
  SQL_request = "INSERT INTO r2_threshold (parameter, population, type, time, threshold, unit, rule, meaning, version) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
  values = []

  for i in range(3,40) :
    if(sheet.cell_value(i, 1)):
      values.append((sheet.cell_value(i,1),sheet.cell_value(i,2),sheet.cell_value(i,3),sheet.cell_value(i,4),float(sheet.cell_value(i,5)) if isinstance(sheet.cell_value(i,5),float) else None, sheet.cell_value(i,6),sheet.cell_value(i,7),sheet.cell_value(i,11), sheet.cell_value(i,12)))

  r2_threshold_table.setScript(SQL_request)
  r2_threshold_table.setRows(values)
  r2_threshold_table.executemany()



  # Information from r3 sheet
  sheet = wb.sheet_by_name('r3')
  r3_table = QueryScript("DROP TABLE IF EXISTS r3; CREATE TABLE r3 (id INT AUTO_INCREMENT PRIMARY KEY, unit VARCHAR(255), sandre VARCHAR(255), parameter VARCHAR(255), NQE VARCHAR(255), 7j_threshold FLOAT, 7j_graduate_25 FLOAT, 7j_graduate_50 FLOAT, 7j_graduate_75 FLOAT,  21j_threshold FLOAT, 21j_graduate_25 FLOAT, 21j_graduate_50 FLOAT, 21j_graduate_75 FLOAT, case_number VARCHAR(255), familly VARCHAR(255), maximum FLOAT, freq_quanti FLOAT);")
  r3_table.execute()
  SQL_request = "INSERT INTO r3 (unit, sandre, parameter, NQE, 7j_threshold, 7j_graduate_25, 7j_graduate_50, 7j_graduate_75, 21j_threshold, 21j_graduate_25, 21j_graduate_50, 21j_graduate_75, case_number, familly, maximum, freq_quanti) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
  values = []
  for i in range(2,346):
    values.append((sheet.cell_value(i,0),sheet.cell_value(i,1),sheet.cell_value(i,2),sheet.cell_value(i,3),float(sheet.cell_value(i,4)) if isinstance(sheet.cell_value(i,4),float) else None,float(sheet.cell_value(i,5)) if isinstance(sheet.cell_value(i,5),float) else None, float(sheet.cell_value(i,6)) if isinstance(sheet.cell_value(i,6),float) else None,float(sheet.cell_value(i,7)) if isinstance( sheet.cell_value(i,7),float) else None,float(sheet.cell_value(i,8)) if isinstance(sheet.cell_value(i,8),float) else None,float(sheet.cell_value(i,9)) if isinstance(sheet.cell_value(i,9),float) else None,float(sheet.cell_value(i,10)) if isinstance(sheet.cell_value(i,10),float) else None,float(sheet.cell_value(i,11)) if isinstance(sheet.cell_value(i,11),float) else None, sheet.cell_value(i,12),sheet.cell_value(i,13), 0.0 if isinstance(sheet.cell_value(i,14),str) else sheet.cell_value(i,14), 0.0 if isinstance(sheet.cell_value(i,15),str) else sheet.cell_value(i,15)))

  r3_table.setScript(SQL_request)
  r3_table.setRows(values)
  r3_table.executemany()