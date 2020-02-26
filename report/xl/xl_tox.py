from tools import QueryScript 
import pandas as pd

import env




def create_dataframe(list_mp):
    matrix = []
    matrixchek =[]


    for mp in list_mp:
        place_id = QueryScript(f"  SELECT place_id   FROM {env.DATABASE_RAW}.measurepoint WHERE id={mp}").execute()
        if place_id not in matrixchek:
             resulat = QueryScript(f" SELECT Male_Survival_7_days, alimentation, neurotoxicity, female_survivor, number_days_exposition, number_female_concerned, index_fertility_average, number_female_analysis, molting_cycle,number_female_concerned_area,endocrine_disruption   FROM {env.DATABASE_TREATED}.toxtable WHERE version={env.VERSION} AND place_id={place_id[0]}").execute()
             matrixchek.append(place_id)
             matrix.append(['']+resulat[0][:3]+['']+resulat[0][3:])

  
    df = pd.DataFrame(matrix)
    df.columns = ['','Survie Male - 7 jours', 'Alimentation',
                'Neurotoxicité AChE','', 'Survie Femelle','Nombre joursexposition in situ',
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

   

          