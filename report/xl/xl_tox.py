from tools import QueryScript 
from calcul import  survie_7jour,alimentation, neurotoxicity,female_survivor,number_days_exposition,number_female_concerned,index_fertility_average,number_female_analysis,number_female_concerned_area,endocrine_disruption,molting_cycle
from database import create_tox_calcul_table
import pandas as pd


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
    for mp in list_mp:
        place_id = QueryScript(f"SELECT place_id FROM measurepoint WHERE id={mp}").execute()
        measurepoint_placeid = QueryScript(f"SELECT id FROM measurepoint WHERE place_id={place_id[0]}").execute()
        if measurepoint_placeid not in matrix:
                matrix.append(measurepoint_placeid)
        else:
                print("measure point id exist before")


    for element in matrix:
        measurepoint_result_tox_table_calcule(element)


def create_tox_dataframe_tabletox_by_list_campaigns(list_campaigns, dict_mp):
       for campaign_str in list_campaigns:
            list_mp = dict_mp[campaign_str]
            create_table_Tox(list_mp)  

        

def create_table_byplaceid():
    matrix = [] 
    place_id = QueryScript(f"SELECT place_id FROM biomae.measurepoint").execute()

    for place in place_id:
        measurepoint_placeid = QueryScript(f"SELECT id FROM measurepoint WHERE place_id={place}").execute()
        if measurepoint_placeid not in matrix:
                matrix.append(measurepoint_placeid)


    for element in matrix:
        measurepoint_result_tox_table_calcule(element)



def create_dataframe(list_mp):
    matrix = []
    matrixchek =[]


    for mp in list_mp:
        place_id = QueryScript(f"SELECT place_id FROM measurepoint WHERE id={mp}").execute()
        if place_id not in matrixchek:
             resulat = QueryScript(f"SELECT survie_7jour, alimentation, neurotoxicity, female_survivor, number_days_exposition, number_female_concerned, index_fertility_average, number_female_analysis, molting_cycle,number_female_concerned_area,endocrine_disruption FROM toxtable WHERE place_id={place_id[0]}").execute()
             matrixchek.append(place_id)
             matrix.append(resulat[0])
             
            

    

    df = pd.DataFrame(matrix)
    df.columns = ['Survie Male - 7 jours', 'Alimentation',
                'Neurotoxicité AChE', 'Survie Femelle','Nombre joursexposition in situ',
                'n','Fécondité','n','Cycle de mue','n','Perturbation endocrinienne']

    df = df.dropna(how='all', axis='columns')
    return df

   

def create_tox_dataframe(head_dataframe, list_campaigns, dict_mp):
    list_dataframe = []
    for campaign_str in list_campaigns:
        list_mp = dict_mp[campaign_str]
        df = create_dataframe(list_mp)  
        list_dataframe.append(df)  
    df_values = pd.concat(list_dataframe)
    df_concat = pd.concat([head_dataframe, df_values], axis=1)
    df_campaigns = df_concat.sort_values(['Numéro', 'Campagne'])
    return df_campaigns

   

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
            
            tmp[1]= str(survie_7jour(pack[1]))    
            tmp[2]= str(alimentation(pack[1]))

        if(pack[0]=='neurology'):
            print("neurotoxicity :" +str(neurotoxicity(pack[1])))
           
            tmp[3]= str(neurotoxicity(pack[1]))
           

        if(pack[0]=='reproduction'):
            print(" female_survivor :" +str(female_survivor(pack[1]))+
                  " nombre jour d'exepostion :" + str(number_days_exposition(pack[1]))+
                  " n :" + str(number_female_concerned(pack[1]))+
                  " fécondité :" + str(index_fertility_average(pack[1]))+
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
    
          