import env
import xlrd
from tools import QueryScript


def fill_reference_tables(cas, xl_path="reference_clean.xlsx"):
    # To open Workbook
    wb = xlrd.open_workbook(xl_path)

    # Constants   FROM {env.DATABASE_TREATED}.r1 sheet
    sheet = wb.sheet_by_name('r1')
    if cas == 1:
      QueryScript(f" DROP TABLE IF EXISTS r1").execute(admin=True)
      r1_table = QueryScript(f" CREATE TABLE r1 (id INT AUTO_INCREMENT PRIMARY KEY, parameter VARCHAR(255), min FLOAT, max FLOAT, version INT)")
      r1_table.execute(admin=True)
    SQL_request = QueryScript(f" INSERT INTO r1 (parameter, min, max, version) VALUES (%s, %s, %s, %s)")
    values = []
    index=1
    is_readable = True
    while is_readable:
      try:
        if sheet.cell_value(index, 0):
          values.append((sheet.cell_value(index,0),float(sheet.cell_value(index, 1)) if sheet.cell_value(index,1) else None,float(sheet.cell_value(index, 2)) if sheet.cell_value(index,2) else None))
          index+=1
        else :
          index+=1
      except IndexError :
        is_readable =False

    SQL_request.setRows(values)
    SQL_request.executemany()

    # Constants   FROM {env.DATABASE_TREATED}.r2 sheet
    sheet = wb.sheet_by_name('r2_constant')
    if cas == 1:
      QueryScript(f" DROP TABLE IF EXISTS r2_constant").execute(admin=True)
      r2_constant_table = QueryScript(f" CREATE TABLE r2_constant (id INT AUTO_INCREMENT PRIMARY KEY, nature VARCHAR(255), name VARCHAR(255), value FLOAT, version INT)")
      r2_constant_table.execute(admin=True)
    SQL_request = QueryScript(f" INSERT INTO r2_constant (nature, name, value, version) VALUES (%s, %s, %s, %s)")
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

    SQL_request.setRows(values)
    SQL_request.executemany()



    # Threshold   FROM {env.DATABASE_TREATED}.r2 sheet
    sheet = wb.sheet_by_name('r2_threshold')
    if cas == 1:
      QueryScript(f" DROP TABLE IF EXISTS r2_threshold").execute(admin=True)
      r2_threshold_table = QueryScript(f" CREATE TABLE r2_threshold (id INT AUTO_INCREMENT PRIMARY KEY, parameter VARCHAR(255), population VARCHAR(255), type VARCHAR(255), time VARCHAR(255), threshold FLOAT, unit VARCHAR(255), rule VARCHAR(255), meaning VARCHAR(255), version INT)")
      r2_threshold_table.execute(admin=True)
    SQL_request = QueryScript(f" INSERT INTO r2_threshold (parameter, population, type, time, threshold, unit, rule, meaning, version) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")
    values = []
    index=1
    is_readable = True
    while is_readable :
      try:
        if(sheet.cell_value(index,1)):
          values.append((sheet.cell_value(index,0),sheet.cell_value(index,1),sheet.cell_value(index,2),sheet.cell_value(index,3),float(sheet.cell_value(index,4)) if isinstance(sheet.cell_value(index,4),float) else None, sheet.cell_value(index,5),sheet.cell_value(index,6),sheet.cell_value(index,10)))
          index+=1
        else:
          index+=1
      except IndexError :
        is_readable=False

    SQL_request.setRows(values)
    SQL_request.executemany()



    # Information   FROM {env.DATABASE_TREATED}.r3 sheet
    sheet = wb.sheet_by_name('r3')
    if cas == 1:
      QueryScript(f" DROP TABLE IF EXISTS r3").execute(admin=True)
      r3_table = QueryScript(f" CREATE TABLE r3 (id INT AUTO_INCREMENT PRIMARY KEY, unit VARCHAR(255), sandre VARCHAR(255), parameter VARCHAR(255), NQE VARCHAR(255), 7j_threshold FLOAT, 7j_graduate_25 FLOAT, 7j_graduate_50 FLOAT, 7j_graduate_75 FLOAT,  21j_threshold FLOAT, 21j_graduate_25 FLOAT, 21j_graduate_50 FLOAT, 21j_graduate_75 FLOAT, case_number VARCHAR(255), familly VARCHAR(255), maximum FLOAT, freq_quanti FLOAT, version INT)")
      r3_table.execute(admin=True)
    SQL_request = QueryScript(f" INSERT INTO r3 (unit, sandre, parameter, NQE, 7j_threshold, 7j_graduate_25, 7j_graduate_50, 7j_graduate_75, 21j_threshold, 21j_graduate_25, 21j_graduate_50, 21j_graduate_75, case_number, familly, maximum, freq_quanti, version) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
    values = []
    index=1
    is_readable=True
    while is_readable :
      try:
        if(sheet.cell_value(index,1)):
          values.append((sheet.cell_value(index,0),int(sheet.cell_value(index,1)) if isinstance(sheet.cell_value(index,1), float) else sheet.cell_value(index,1),sheet.cell_value(index,2),sheet.cell_value(index,3),float(sheet.cell_value(index,4)) if isinstance(sheet.cell_value(index,4),float) else None,float(sheet.cell_value(index,5)) if isinstance(sheet.cell_value(index,5),float) else None, float(sheet.cell_value(index,6)) if isinstance(sheet.cell_value(index,6),float) else None,float(sheet.cell_value(index,7)) if isinstance( sheet.cell_value(index,7),float) else None,float(sheet.cell_value(index,8)) if isinstance(sheet.cell_value(index,8),float) else None,float(sheet.cell_value(index,9)) if isinstance(sheet.cell_value(index,9),float) else None,float(sheet.cell_value(index,10)) if isinstance(sheet.cell_value(index,10),float) else None,float(sheet.cell_value(index,11)) if isinstance(sheet.cell_value(index,11),float) else None, sheet.cell_value(index,12),sheet.cell_value(index,13), 0.0 if isinstance(sheet.cell_value(index,14),str) else sheet.cell_value(index,14), 0.0 if isinstance(sheet.cell_value(index,15),str) else sheet.cell_value(index,15)))
          index+=1
        else:
          index+=1
      except IndexError:
        is_readable=False

    SQL_request.setRows(values)
    SQL_request.executemany()


def run(cas, xl_path):
    ## On a 3 cas pour les requêtes SQL
    # Cas 1: 'première_version'
    # Cas 2: 'update_version'
    # Cas 3: 'nouvelle_version'

    ## Cas 1: Création et remplissage de la base de données
    if cas == 1:
      
        print("--> reference table")
        fill_reference_tables(1, xl_path)
        print("--> reference table ready")

    ## Cas 2: Mise à jour de la dernière version connue
    if cas == 2:
        pass  # Il n'y a pas de mise à jour

    ## Cas 3: Ajout d'une nouvelle version
    if cas == 3:
        print("--> reference table")
        fill_reference_tables(3, xl_path)
        print("--> reference table ready")


