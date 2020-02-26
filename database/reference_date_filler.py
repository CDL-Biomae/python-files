from tools import QueryScript
import env

def run():
    reference_date_table = QueryScript(
        f" DROP TABLE IF EXISTS reference_date; CREATE TABLE reference_date (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), step INT(11), barrel VARCHAR(255), version INT);")
    reference_date_table.execute(True)
    SQL_request = f" INSERT INTO reference_date (name, step, barrel, version) VALUES (%s, %s, %s, %s)"
    values = [("Transplantation Alimentation", 50, "R0"),
              ("Recuperation Alimentation", 60, "R7"),
              ("Lancement Alimentation", 20, None),
              ("Recuperation reprotoxicite", 140, "RN"),
              ("Arret Reprotoxicite", 170, None),
              ("Lancement Chimie", 50, "C0"),
              ("Recuperation Chimie", 100, "R21")]

    reference_date_table.setScript(SQL_request)
    reference_date_table.setRows(values)
    reference_date_table.executemany()


if __name__ == '__main__':
    run()
