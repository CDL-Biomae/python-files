from tools import QueryScript, list_to_dict
import pandas as pd

import env

def create_dataframe(list_mp):
    matrix = []

    output = QueryScript(
        f" SELECT measurepoint_fusion_id, round(male_survival_7_days), round(alimentation, 1), round(neurotoxicity, 1), round(female_survivor), number_days_exposition, number_female_concerned, round(index_fertility_average, 1), number_female_analysis, molting_cycle,number_female_concerned_area,endocrine_disruption FROM {env.DATABASE_TREATED}.toxtable WHERE version={env.VERSION} AND measurepoint_fusion_id IN {tuple(list_mp)};"
    ).execute()

    dict_output = list_to_dict(output)

    for mp_fusion in list_mp:
        try:
            data = dict_output[mp_fusion]
        except KeyError:
            data = [None]*11
            matrix.append([''] + data[:3] + [''] + data[3:])
        else:
            matrix.append(['']+data[0:3]+['']+data[3:])

  
    df = pd.DataFrame(matrix)
    df.columns = ['','Survie Male - 7 jours', 'Alimentation',
                'Neurotoxicité AChE','', 'Survie Femelle','Nombre jours exposition in situ',
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

   

          