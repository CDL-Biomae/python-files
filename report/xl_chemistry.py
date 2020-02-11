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
            [crustacean, fish] = chemistry.data(pack[0])[:2]
            matrix.append([''] + crustacean + [''] + fish)
        else:
            matrix.append([''] + ['ND' for el in elements_crustacean] + [''] + ['ND' for el in elements_fish])
    df = pd.DataFrame(matrix)
    df.columns = [''] + list(elements_crustacean.values()) + [''] + list(elements_fish.values())
    df = df.dropna(how='all', axis='columns')

    return df


## MAIN FUNCTION ##
def create_nqe_dataframe(head_dataframe, list_campaigns, dict_mp):
    list_dataframe = []
    for campaign_str in list_campaigns:
        list_mp = dict_mp[campaign_str]
        df = create_dataframe(list_mp[:2])
        list_dataframe.append(df)

    df_values = pd.concat(list_dataframe)
    print(head_dataframe.shape)
    print(df_values.shape)
    df_concat = pd.concat([head_dataframe, df_values], axis=1)
    df_campaigns = df_concat.sort_values('Numéro')

    return df_campaigns

        
        