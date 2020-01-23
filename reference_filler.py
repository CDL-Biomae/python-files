import xlrd 
from query import Query

file_name = ("AG-003-01_Macros.xlsm") 
  
# To open Workbook 
wb = xlrd.open_workbook(file_name) 
sheet = wb.sheet_by_name('r2') 

r2_constant_table = Query(script="DROP TABLE IF EXISTS r2_constant; CREATE TABLE r2_constant (id INT AUTO_INCREMENT PRIMARY KEY, nature VARCHAR(255), name VARCHAR(255), value VARCHAR(255))")
r2_constant_table.execute()
SQL_request = "INSERT INTO r2_constant (id, nature, name, value) VALUES (%s, %s, %s, %s)"
values = []

# All alimentation constants
for i in range(14) :
  values.append((i+1,"alimentation",str(sheet.cell_value(4+i, 13)),sheet.cell_value(4+i, 14)))

for i in range(6) :
  values.append((i+15,"AChE",str(sheet.cell_value(20+i, 13)),sheet.cell_value(20+i, 14)))
for i in range(20) :
  values.append((i+21,"Repro",str(sheet.cell_value(28+i, 13)),sheet.cell_value(28+i, 14)))

r2_constant_table.setScript(SQL_request)
r2_constant_table.setRows(values)
r2_constant_table.executemany()
