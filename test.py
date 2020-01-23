from query import Query

New_Query = Query(script="CREATE TABLE r2_constant (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), nature VARCHAR(255), value VARCHAR(255))")

print(New_Query.execute())