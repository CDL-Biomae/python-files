from tools import QueryScript
from calcul import  survie_7jour,alimentation, neurotoxicity,female_survivor,number_days_exposition,number_female_concerned,index_fertility_average,number_female_analysis,number_female_concerned_area,endocrine_disruption,molting_cycle

def create_tox_calcul_table(values):
    tox_table = QueryScript(
        " CREATE TABLE IF NOT EXISTS toxtable (id INT AUTO_INCREMENT PRIMARY KEY, place_id INT, Male_Survival_7_days varchar(255), alimentation varchar(255), neurotoxicity varchar(255), female_survivor varchar(255), number_days_exposition varchar(255), number_female_concerned varchar(255),index_fertility_average varchar(255),number_female_analysis varchar(255),molting_cycle varchar(255),number_female_concerned_area varchar(255),endocrine_disruption varchar(255));")
    tox_table.execute()
    SQL_request = "INSERT INTO toxtable (place_id, Male_Survival_7_days, alimentation, neurotoxicity, female_survivor, number_days_exposition, number_female_concerned, index_fertility_average, number_female_analysis, molting_cycle,number_female_concerned_area,endocrine_disruption ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s)"
    tox_table.setScript(SQL_request)
    tox_table.setRows(values)
    tox_table.executemany()

def all_measure_points(campaign_ref):
    output = QueryScript(
        f"SELECT id FROM measurepoint WHERE reference LIKE '{campaign_ref}%';"
    )
    return output.execute()

def create_dict_mp2(list_campaigns):
    dict = {}
    for c in list_campaigns:
        list_mp = all_measure_points(c)
        dict[c] = list_mp
    return dict



def create_table_Tox(list_mp):
    matrix = [] 
    for i in range(len(list_mp)):
        place_id = QueryScript(f"SELECT place_id FROM measurepoint WHERE id={list_mp[i]}").execute()
        measurepoint_placeid = QueryScript(f"SELECT id FROM measurepoint WHERE place_id={place_id[0]}").execute()
        if measurepoint_placeid not in matrix:
                matrix.append(measurepoint_placeid)
    for i in range(len(matrix)):
        measurepoint_result_tox_table_calcule(matrix[i])


def create_tox_dataframe_tabletox_by_list_campaigns(list_campaigns, dict_mp):
       for campaign_str in list_campaigns:
            list_mp = dict_mp[campaign_str]
            create_table_Tox(list_mp)  

        

def create_table_byplaceid():
    matrix = [] 
    place_id = QueryScript(f"SELECT place_id FROM biomae.measurepoint").execute()

    for i in range(len(place_id)):
        measurepoint_placeid = QueryScript(f"SELECT id FROM measurepoint WHERE place_id={place_id[i]}").execute()
        if measurepoint_placeid not in matrix:
                matrix.append(measurepoint_placeid)
    for i in range(len(matrix)):
        measurepoint_result_tox_table_calcule(matrix[i])

        

def measurepoint_result_tox_table_calcule(measurepoint_id):

    place_id = QueryScript(f"SELECT place_id FROM measurepoint WHERE id={measurepoint_id[0]}").execute()
    if len(measurepoint_id) > 1:
         packs = QueryScript(f"SELECT nature, id FROM pack WHERE measurepoint_id in {tuple(measurepoint_id)}").execute()
    else:
         packs = QueryScript(f"SELECT nature, id FROM pack WHERE measurepoint_id={measurepoint_id[0]}").execute()
    toxcalcule = []
    tmp = [1] * 12
    tmp[0]= place_id[0]
    
    for pack in packs :    
     
        if(pack[0]=='alimentation'):
            print("survie_7jour :" +str(survie_7jour(pack[1]))+" alimentation :" +str(alimentation(pack[1])) )
            
            tmp[1]= str(round(survie_7jour(pack[1])))    
            tmp[2]= str("%.1f" % alimentation(pack[1]))

        if(pack[0]=='neurology'):
            print("neurotoxicity :" +str( neurotoxicity(pack[1])))
           
            tmp[3]= str("%.1f" % neurotoxicity(pack[1]))
           

        if(pack[0]=='reproduction'):
            print(" female_survivor :" +str(female_survivor(pack[1]))+
                  " nombre jour d'exepostion :" + str(number_days_exposition(pack[1]))+
                  " n :" + str(number_female_concerned(pack[1]))+
                  " fécondité :" + str("%.1f" % index_fertility_average(pack[1]))+
                  " n :" + str(number_female_analysis(pack[1]))+
                  " cycle de mue :" + str(molting_cycle(pack[1]))+
                  " n :" + str(number_female_concerned_area(pack[1])[0])+
                  " perturbation endocrinienne :" + str(endocrine_disruption(pack[1]))
             )
            tmp[4]=str(female_survivor(pack[1]))
            tmp[5]=str(number_days_exposition(pack[1]))
            tmp[6]=str(number_female_concerned(pack[1]))
            tmp[7]=str(index_fertility_average(pack[1]))
            tmp[8]=str(number_female_analysis(pack[1]))
            tmp[9]=str(molting_cycle(pack[1]))
            tmp[10]=str(number_female_concerned_area(pack[1])[0])
            tmp[11]=str(endocrine_disruption(pack[1]))

    toxcalcule.append(tmp)      
    create_tox_calcul_table(toxcalcule) 
    return tmp