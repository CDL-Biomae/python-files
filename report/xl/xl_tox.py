from tools import QueryScript 
from calcul import survie_7jour,molting_cycle,alimentation,number_female_concerned_area,endocrine_disruption,female_survivor,neurotoxicity,index_fertility_average,number_days_exposition,number_female_concerned,number_female_analysis
from report import measurepoint_result
import pandas as pd

def create_dataframe(list_mp):
    matrix = []
    list_pi = []
    
    print(list_mp)

    for i in range(len(list_mp)):
       measurepoint_result(list_mp[i])

 

           
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


