from calcul import chemistry, elements_crustacean, elements_fish
import pandas as pd
from tools import QueryScript

## CREATE DATAFRAME ##
def create_dataframe(list_mp):
    matrix = []

    for i in range(len(list_mp)):
        mp = list_mp[i]
        pack = QueryScript(f"SELECT id FROM pack WHERE nature='chemistry' AND measurepoint_id={mp}").execute()
        if len(pack)>0:
            crustacean = chemistry.result_by_pack_and_sandre(pack[0],list(elements_crustacean.keys()))
            fish = chemistry.result_by_pack_and_sandre(pack[0],list(elements_fish.keys()))
        else:
            crustacean =  [['ND' for el in elements_crustacean],list(elements_crustacean.keys())]
            fish =  [['ND' for el in elements_fish],list(elements_fish.keys())]
        matrix.append([''] + crustacean[0] + [''] + fish[0])
    df = pd.DataFrame(matrix)
    df.columns = [''] + list(elements_crustacean.values()) + [''] + list(elements_fish.values())
    df = df.dropna(how='all', axis='columns')

    return df

## MAIN FUNCTION ##
def create_nqe_dataframe(head_dataframe, list_campaigns, dict_mp):
    list_dataframe = []
    for campaign_str in list_campaigns:
        list_mp = dict_mp[campaign_str]
        df = create_dataframe(list_mp)
        list_dataframe.append(df)

    df_values = pd.concat(list_dataframe)
    df_concat = pd.concat([head_dataframe, df_values], axis=1)
    df_campaigns = df_concat.sort_values(['Numéro', 'Campagne'])

    return df_campaigns

        
        