from calcul import chemistry, elements_crustacean, elements_fish
import pandas as pd
from tools import QueryScript


## CREATE DATAFRAME ##
def create_dataframe(dick_pack_fusion):
    matrix = []
    data = chemistry.result_by_packs_and_sandre(dick_pack_fusion)
    for mp in dick_pack_fusion:
        matrix.append([''] + [data[mp][sandre] for sandre in elements_crustacean ]+[''] + [data[mp][sandre] for sandre in elements_fish ])
    df = pd.DataFrame(matrix)
    df.columns = [''] + [element for element in elements_crustacean]  + [''] + [element for element in elements_fish]
    df = df.dropna(how='all', axis='columns')

    return df



## MAIN FUNCTION ##
def create_nqe_dataframe(head_dataframe, dick_pack_fusion):
    
    head_dataframe = head_dataframe.reset_index(drop=True)
    df_values = create_dataframe(dick_pack_fusion)
    df_concat = pd.concat([head_dataframe, df_values], axis=1)
    df_campaigns = df_concat.sort_values(['Numéro', 'Campagne'])

    return df_campaigns


        
        
