from calcul import elements_crustacean, elements_fish
import pandas as pd
from tools import QueryScript


## CREATE DATAFRAME ##
def create_dataframe(result_dict, measurepoint_list):
    '''
    Créé une dataframe à partir d'un référence de campagne.
    Les colonnes de la dataframe sont les sandres précisés dans /calcul/chemistry/nqe
    Les colonnes vides sont supprimées
    :param result_dict:
    :return: dataframe:
    '''
    matrix = []
    for measurepoint_id in measurepoint_list:
            if measurepoint_id in result_dict:
                matrix.append([''] + [result_dict[measurepoint_id][sandre] if sandre in result_dict[measurepoint_id] and result_dict[measurepoint_id][sandre] !='0.0' else 'ND' for sandre in elements_crustacean ]+[''] + [result_dict[measurepoint_id][sandre] if sandre in result_dict[measurepoint_id] and result_dict[measurepoint_id][sandre] !='0.0' else 'ND' for sandre in elements_fish ] + [measurepoint_id])
            else :
                matrix.append([''] + ['ND' for sandre in elements_crustacean ]+[''] + ['ND' for sandre in elements_fish ] + [measurepoint_id])
            
    
    df = pd.DataFrame(matrix)
    df.columns = [''] + [element for element in elements_crustacean]  + [''] + [element for element in elements_fish] + ['']
    df = df.dropna(how='all', axis='columns')

    return df



## MAIN FUNCTION ##
def create_nqe_dataframe(head_dataframe, result_dict, measurepoint_list):
    
    df_values = create_dataframe(result_dict, measurepoint_list)
    head_dataframe = head_dataframe.reset_index(drop=True)
    df_concat = pd.concat([head_dataframe, df_values], axis=1)
    df_campaigns = df_concat.sort_values(['Numéro', 'Campagne'])

    return df_campaigns
        
        
