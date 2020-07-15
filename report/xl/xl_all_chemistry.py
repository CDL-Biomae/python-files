import pandas as pd
from tools import QueryScript
import env

## CREATE DATAFRAME ##
def create_dataframe(result_dict, measurepoint_list):
    '''
    Créé une dataframe à partir d'un référence de campagne.
    Les colonnes de la dataframe sont les sandres des différentes familles d'éléments
    Les colonnes vides sont supprimées
    :param result_dict:
    :return: dataframe:
    '''
    sandre_and_family_data = QueryScript(f" SELECT sandre, familly  FROM {env.DATABASE_TREATED}.r3 WHERE version=  {env.CHOSEN_VERSION()}").execute()
    family_dict = {}
    for sandre, family in sandre_and_family_data :
        try : 
            sandre_transformed = int(float(sandre))
        except ValueError :
            sandre_transformed =  sandre
        if family in family_dict :
            family_dict[family].append(sandre_transformed)
        else :
            family_dict[family] = [sandre_transformed]

    columns = ['']
    for family in family_dict :
        columns += family_dict[family] + ['']

    
    matrix = []

    for measurepoint_id in measurepoint_list:
        if measurepoint_id in result_dict :
            matrix.append([result_dict[measurepoint_id][sandre] if sandre in result_dict[measurepoint_id] and  result_dict[measurepoint_id][sandre] !='0.0' else 'ND' if not sandre=='' else ''  for sandre in columns] + [measurepoint_id])
        else :
            matrix.append(['ND' if not sandre=='' else ''  for sandre in columns] + [measurepoint_id])
 

    df = pd.DataFrame(matrix)
    df.columns = columns + ['']
    df = df.dropna(how='all', axis='columns')

    return df

## MAIN FUNCTION ##
def create_all_chemistry_dataframe(head_dataframe, result_dict, measurepoint_list):
    
    df_values = create_dataframe(result_dict, measurepoint_list)
    head_dataframe = head_dataframe.reset_index(drop=True)
    df_concat = pd.concat([head_dataframe, df_values], axis=1)
    df_campaigns = df_concat.sort_values(['Numéro', 'Campagne'])

    return df_campaigns

        
        
