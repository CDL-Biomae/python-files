from tools import QueryScript

def create_tox_calcul_table(values):
    tox_table = QueryScript(
        " CREATE TABLE IF NOT EXISTS toxtable (id INT AUTO_INCREMENT PRIMARY KEY, place_id INT, survie_7jour varchar(255), alimentation varchar(255), neurotoxicity varchar(255), female_survivor varchar(255), number_days_exposition varchar(255), number_female_concerned varchar(255),index_fertility_average varchar(255),number_female_analysis varchar(255),molting_cycle varchar(255),number_female_concerned_area varchar(255),endocrine_disruption varchar(255));")
    tox_table.execute()
    SQL_request = "INSERT INTO toxtable (place_id, survie_7jour, alimentation, neurotoxicity, female_survivor, number_days_exposition, number_female_concerned, index_fertility_average, number_female_analysis, molting_cycle,number_female_concerned_area,endocrine_disruption ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s)"
    tox_table.setScript(SQL_request)
    tox_table.setRows(values)
    tox_table.executemany()

  
   
    
