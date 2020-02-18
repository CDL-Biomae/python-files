from tools import QueryScript 
from calcul import  survie_7jour,alimentation, neurotoxicity,female_survivor,number_days_exposition,number_female_concerned,index_fertility_average,number_female_analysis,number_female_concerned_area,endocrine_disruption,molting_cycle
from database import create_tox_calcule_table
import pandas as pd



def create_dataframe(list_mp):
    matrix = [] 
    for i in range(len(list_mp)):
        place_id = QueryScript(f"SELECT place_id FROM measurepoint WHERE id={list_mp[i]}").execute()
        measurepoint_placeid = QueryScript(f"SELECT id FROM measurepoint WHERE place_id={place_id[0]}").execute()
        matrix.append(measurepoint_placeid)
    for i in range(len(matrix)):
       measurepoint_result(matrix[i])
    
      
    #df = pd.DataFrame(matrix)
    #df.columns = ['Survie Male - 7 jours', 'Alimentation','Neurotoxicité AChE', 'Survie Femelle','Nombre joursexposition in situ', 'n','indice/n','Cycle de mue','n','Perturbation endocrinienne']
    #df = df.dropna(how='all', axis='columns')
    #return df

   

def create_tox_dataframe(head_dataframe, list_campaigns, dict_mp):
    list_dataframe = []



    for campaign_str in list_campaigns:
        list_mp = dict_mp[campaign_str]
        create_dataframe(list_mp)
       
       
       
        #list_dataframe.append(df)
    #df_values = pd.concat(list_dataframe)
    #df_concat = pd.concat([head_dataframe, df_values], axis=1)
    #df_campaigns = df_concat.sort_values('Numéro')

    #return df_campaigns

   

def measurepoint_result(measurepoint_id):

    place_id = QueryScript(f"SELECT place_id FROM measurepoint WHERE id={measurepoint_id[0]}").execute()
    if len(measurepoint_id) > 1:
         packs = QueryScript(f"SELECT nature, id FROM pack WHERE measurepoint_id in {tuple(measurepoint_id)}").execute()
    else:
         packs = QueryScript(f"SELECT nature, id FROM pack WHERE measurepoint_id={measurepoint_id[0]}").execute()
    
    print(packs)
    tmp = [1] * 12
    tmp[0]= place_id[0]
    for pack in packs :    
         
        toxcalcule = [] 
     
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
    create_tox_calcule_table(toxcalcule)  
    
          