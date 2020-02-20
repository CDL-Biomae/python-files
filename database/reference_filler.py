import env
import xlrd
from tools import QueryScript

file_name = env.REFERENCE_EXCEL

def run():
  # To open Workbook 
  wb = xlrd.open_workbook(file_name) 
  
  # Constants from r1 sheet
  sheet = wb.sheet_by_name('r1')
  QueryScript("DROP TABLE IF EXISTS r1").execute()
  r1_table = QueryScript("CREATE TABLE r1 (id INT AUTO_INCREMENT PRIMARY KEY, parameter VARCHAR(255), min FLOAT, max FLOAT)")
  r1_table.execute()
  SQL_request = "INSERT INTO r1 (parameter, min, max) VALUES (%s, %s, %s)"
  values = []
  index=1
  is_readable = True
  while is_readable :
    try :
      if(sheet.cell_value(index, 0)):
        values.append((sheet.cell_value(index,0),float(sheet.cell_value(index, 1)) if sheet.cell_value(index,1) else None,float(sheet.cell_value(index, 2)) if sheet.cell_value(index,2) else None))
        index+=1
      else :
        index+=1
    except IndexError :
      is_readable =False

  r1_table.setScript(SQL_request)
  r1_table.setRows(values)
  r1_table.executemany()
  
  # Constants from r2 sheet
  sheet = wb.sheet_by_name('r2_constant') 
  QueryScript("DROP TABLE IF EXISTS r2_constant").execute()
  r2_constant_table = QueryScript("CREATE TABLE r2_constant (id INT AUTO_INCREMENT PRIMARY KEY, nature VARCHAR(255), name VARCHAR(255), value FLOAT)")
  r2_constant_table.execute()
  SQL_request = "INSERT INTO r2_constant (nature, name, value) VALUES (%s, %s, %s)"
  values = []
  index=0
  current_nature = ''
  is_readable =True
  while is_readable:
    try :
      if(sheet.cell_value(index, 0)):
        current_nature = sheet.cell_value(index,0)
        index+=1
        
      elif(sheet.cell_value(index,1)):
        values.append((current_nature,str(sheet.cell_value(index, 1)),float(sheet.cell_value(index, 2))if sheet.cell_value(index,2) else None))
        index+=1
      else:
        index+=1
    except IndexError :
      is_readable =False
      
  r2_constant_table.setScript(SQL_request)
  r2_constant_table.setRows(values)
  r2_constant_table.executemany()



  # Threshold from r2 sheet
  sheet = wb.sheet_by_name('r2_threshold') 
  QueryScript("DROP TABLE IF EXISTS r2_threshold").execute()
  r2_threshold_table = QueryScript("CREATE TABLE r2_threshold (id INT AUTO_INCREMENT PRIMARY KEY, parameter VARCHAR(255), population VARCHAR(255), type VARCHAR(255), time VARCHAR(255), threshold FLOAT, unit VARCHAR(255), rule VARCHAR(255), meaning VARCHAR(255), version VARCHAR(255))")
  r2_threshold_table.execute()
  SQL_request = "INSERT INTO r2_threshold (parameter, population, type, time, threshold, unit, rule, meaning, version) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
  values = []
  index=1
  is_readable = True
  while is_readable :
    try:
      if(sheet.cell_value(index,1)):
        values.append((sheet.cell_value(index,0),sheet.cell_value(index,1),sheet.cell_value(index,2),sheet.cell_value(index,3),float(sheet.cell_value(index,4)) if isinstance(sheet.cell_value(index,4),float) else None, sheet.cell_value(index,5),sheet.cell_value(index,6),sheet.cell_value(index,10), sheet.cell_value(index,11)))
        index+=1
      else:
        index+=1
    except IndexError :
      is_readable=False

  r2_threshold_table.setScript(SQL_request)
  r2_threshold_table.setRows(values)
  r2_threshold_table.executemany()



  # Information from r3 sheet
  sheet = wb.sheet_by_name('r3')
  QueryScript("DROP TABLE IF EXISTS r3").execute()
  r3_table = QueryScript("CREATE TABLE r3 (id INT AUTO_INCREMENT PRIMARY KEY, unit VARCHAR(255), sandre VARCHAR(255), parameter VARCHAR(255), NQE VARCHAR(255), 7j_threshold FLOAT, 7j_graduate_25 FLOAT, 7j_graduate_50 FLOAT, 7j_graduate_75 FLOAT,  21j_threshold FLOAT, 21j_graduate_25 FLOAT, 21j_graduate_50 FLOAT, 21j_graduate_75 FLOAT, case_number VARCHAR(255), familly VARCHAR(255), maximum FLOAT, freq_quanti FLOAT)")
  r3_table.execute()
  SQL_request = "INSERT INTO r3 (unit, sandre, parameter, NQE, 7j_threshold, 7j_graduate_25, 7j_graduate_50, 7j_graduate_75, 21j_threshold, 21j_graduate_25, 21j_graduate_50, 21j_graduate_75, case_number, familly, maximum, freq_quanti) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
  values = []
  index=0
  is_readable=True
  while is_readable :
    try:
      if(sheet.cell_value(index,1)):
        values.append((sheet.cell_value(index,0),sheet.cell_value(index,1),sheet.cell_value(index,2),sheet.cell_value(index,3),float(sheet.cell_value(index,4)) if isinstance(sheet.cell_value(index,4),float) else None,float(sheet.cell_value(index,5)) if isinstance(sheet.cell_value(index,5),float) else None, float(sheet.cell_value(index,6)) if isinstance(sheet.cell_value(index,6),float) else None,float(sheet.cell_value(index,7)) if isinstance( sheet.cell_value(index,7),float) else None,float(sheet.cell_value(index,8)) if isinstance(sheet.cell_value(index,8),float) else None,float(sheet.cell_value(index,9)) if isinstance(sheet.cell_value(index,9),float) else None,float(sheet.cell_value(index,10)) if isinstance(sheet.cell_value(index,10),float) else None,float(sheet.cell_value(index,11)) if isinstance(sheet.cell_value(index,11),float) else None, sheet.cell_value(index,12),sheet.cell_value(index,13), 0.0 if isinstance(sheet.cell_value(index,14),str) else sheet.cell_value(index,14), 0.0 if isinstance(sheet.cell_value(index,15),str) else sheet.cell_value(index,15)))
        index+=1
      else:
        index+=1
    except IndexError:
      is_readable=False


  r3_table.setScript(SQL_request)
  r3_table.setRows(values)
  r3_table.executemany()