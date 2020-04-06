from calcul import chemistry, elements_crustacean, elements_fish
import pandas as pd
from tools import QueryScript


## CREATE DATAFRAME ##
def create_dataframe(dict_pack):
    '''
    Créé une dataframe à partir d'un référence de campagne.
    Les colonnes de la dataframe sont les sandres précisés dans /calcul/chemistry/nqe
    Les colonnes vides sont supprimées
    :param dict_pack:
    :return: dataframe:
    '''
    matrix = []
    data = chemistry.result_by_packs_and_sandre(dict_pack)
    for mp in dict_pack:
        if data[mp]:
            matrix.append([''] + [data[mp][sandre] if data[mp][sandre] !='0.0' else 'ND' for sandre in elements_crustacean ]+[''] + [data[mp][sandre] if data[mp][sandre] !='0.0' else 'ND' for sandre in elements_fish ] + [mp])
        else :
            matrix.append([''] + ['ND' for sandre in elements_crustacean ]+[''] + ['ND' for sandre in elements_fish ] + [mp])
            
    
    df = pd.DataFrame(matrix)
    df.columns = [''] + [element for element in elements_crustacean]  + [''] + [element for element in elements_fish] + ['']
    df = df.dropna(how='all', axis='columns')

    return df



## MAIN FUNCTION ##
def create_nqe_dataframe(head_dataframe, dict_pack):
    
    head_dataframe = head_dataframe.reset_index(drop=True)
    df_values = create_dataframe(dict_pack)
    df_concat = pd.concat([head_dataframe, df_values], axis=1)
    df_campaigns = df_concat.sort_values(['Numéro', 'Campagne'])

    return df_campaigns


        
        
