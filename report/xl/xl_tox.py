from tools import QueryScript, list_to_dict
import pandas as pd
import env

def create_dataframe(list_mp):
    '''
    Créé une dataframe à partir d'une liste de points de mesures
    Les colonnes de la dataframe sont ['','Survie Male - 7 jours', 'Alimentation',
                                       'Neurotoxicité AChE','', 'Survie Femelle','Nombre jours exposition in situ',
                                       'n','Fécondité','n','Cycle de mue','n','Perturbation endocrinienne','']
    Les colonnes '' sont utilisées pour faire des séparations de tableau
    :param list_mp:
    :return: dataframe:
    '''
    matrix = []
    if len(list_mp) > 1:
        query_tuple_mp = tuple(list_mp)
    else:
        query_tuple_mp = f"({list_mp[0]})"
    output = QueryScript(
        f" SELECT measurepoint_id, round(male_survival_7_days), round(alimentation, 1), round(neurotoxicity, 1), round(female_survivor), number_days_exposition, number_female_concerned, round(percent_inhibition_fecondite, 1), number_female_analysis, molting_cycle,number_female_concerned_area,endocrine_disruption,measurepoint_id FROM {env.DATABASE_TREATED}.toxtable WHERE version=  {env.CHOSEN_VERSION()} AND measurepoint_id IN {query_tuple_mp};"
    ).execute()

    dict_output = list_to_dict(output)

    for mp in list_mp:
        try:
            data = dict_output[mp]
        except KeyError:
            data = [None]*11
            matrix.append([''] + data[:3] + [''] + data[3:])
        else:
            matrix.append(['']+data[0:3]+['']+data[3:])

    df = pd.DataFrame(matrix)
    df.columns = ['','Survie Male - 7 jours', 'Alimentation',
                'Neurotoxicité AChE','', 'Survie Femelle','Nombre jours exposition in situ',
                'n','Fécondité','n','Cycle de mue','n','Perturbation endocrinienne','']

   
    return df

   
# creation final de l'excel ou il y'a les agnces et les ligne de toxtable qui correspend 
def create_tox_dataframe(head_dataframe, list_campaigns, dict_mp):
    '''
    Créé une dataframe qui contient les données de l'onglet 'Tox' de l'Excel
    :param head_dataframe: cf initialization.py
    :param list_campaigns: list des references de campagne
    :param dict_mp: {'ref_campagne': [mp, ...], ...}
    :return:
    '''
    list_dataframe = []
    for campaign_str in list_campaigns:
        list_mp = dict_mp[campaign_str]
        df = create_dataframe(list_mp)  
        list_dataframe.append(df)  
    df_values = pd.concat(list_dataframe)
    df_concat = pd.concat([head_dataframe, df_values], axis=1)
    df_campaigns = df_concat.sort_values(['Numéro', 'Campagne'])
    return df_campaigns
