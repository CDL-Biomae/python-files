from calcul import chemistry
import pandas as pd
from tools import QueryScript

## CREATE DATAFRAME ##
def create_dataframe(list_mp):
    elements_metal = QueryScript("SELECT ")
    matrix = []

    for i in range(len(list_mp)):
        mp = list_mp[i]
        pack = QueryScript(f"SELECT id FROM pack WHERE nature='chemistry' AND measurepoint_id={mp}").execute()
        if len(pack)>0:
            [metal, organic] = chemistry.data(pack[0])[2:4]
            matrix.append([''] + metal + [''] + organic)
        else:
            matrix.append([''] + ['ND' for el in elements_metal] + [''] + ['ND' for el in elements_organic])
    df = pd.DataFrame(matrix)
    df.columns = [''] + list(elements_metal.values()) + [''] + list(elements_organic.values())
    df = df.dropna(how='all', axis='columns')

    return df

## MAIN FUNCTION ##
def create_nqe_dataframe(head_dataframe, list_campaigns, dict_mp):
    list_dataframe = []
    for campaign_str in list_campaigns:
        list_mp = dict_mp[campaign_str]
        df = create_dataframe(list_mp[:1])
        list_dataframe.append(df)

    df_values = pd.concat(list_dataframe)
    df_concat = pd.concat([head_dataframe, df_values], axis=1)
    df_campaigns = df_concat.sort_values(['Numéro', 'Campagne'])

    return df_campaigns

        
        