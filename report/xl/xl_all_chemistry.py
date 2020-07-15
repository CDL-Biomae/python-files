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
    sandre_data = QueryScript(f" SELECT distinct sandre  FROM {env.DATABASE_RAW}.Analysis WHERE name!='' AND sandre!=''").execute()
    sandre_data = sorted(sandre_data)
    columns = []
    for sandre in sandre_data :
        try : 
            sandre_transformed = int(float(sandre))
        except ValueError :
            sandre_transformed = sandre
        columns.append(sandre_transformed)

    
    matrix = []

    for measurepoint_id in measurepoint_list:
        if measurepoint_id in result_dict :
            matrix.append([''] + [result_dict[measurepoint_id][sandre] if sandre in result_dict[measurepoint_id] and  result_dict[measurepoint_id][sandre] !='0.0' else None  for sandre in columns] + [measurepoint_id])
        else :
            matrix.append([''] + [None  for sandre in columns] + [measurepoint_id])
 

    df = pd.DataFrame(matrix)
    df.columns = [''] + columns + ['']
    df = df.dropna(how='all', axis='columns')

    return df

## MAIN FUNCTION ##
def create_all_chemistry_dataframe(head_dataframe, result_dict, measurepoint_list):
    
    df_values = create_dataframe(result_dict, measurepoint_list)
    head_dataframe = head_dataframe.reset_index(drop=True)
    df_concat = pd.concat([head_dataframe, df_values], axis=1)
    df_campaigns = df_concat.sort_values(['Numéro', 'Campagne'])

    return df_campaigns

        
        
