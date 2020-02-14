from tools import QueryScript


def create_empty_date_table():
    key_dates_table = QueryScript(
        "DROP TABLE IF EXISTS toxtable; CREATE TABLE toxtable (id INT AUTO_INCREMENT PRIMARY KEY, measurepoint_id INT, pack_id INT, date DATETIME, measurepoint_fusion_id INT);")
    key_dates_table.execute()
    print('La table key_dates a été créée')