from calcul import chemistry
import pandas as pd
from tools import QueryScript

## CREATE DATAFRAME ##
def create_dataframe(list_mp):
    elements_metal = QueryScript("SELECT sandre, parameter FROM r3 WHERE 21j_threshold IS NOT NULL AND familly='Métaux'").execute()
    elements_organic = QueryScript("SELECT sandre, parameter FROM r3 WHERE 21j_threshold IS NOT NULL AND familly!='Métaux'").execute()
    matrix = []

    for mp in list_mp:
        pack = QueryScript(f"SELECT id FROM pack WHERE nature='chemistry' AND measurepoint_id={mp}").execute()
        if len(pack)>0:
            metal = chemistry.result_by_pack_and_sandre(pack[0],[int(float(element[0])) for element in elements_metal])
            organic = chemistry.result_by_pack_and_sandre(pack[0],[int(float(element[0])) for element in elements_organic])
        else:
            metal =  [['ND' for el in elements_metal],[int(float(element[0])) for element in elements_metal]]
            organic =  [['ND' for el in elements_organic],[int(float(element[0])) for element in elements_organic]]
        matrix.append([''] + metal[0] + [''] + organic[0])
    df = pd.DataFrame(matrix)
    df.columns = [''] + [element[1] for element in elements_metal]  + [''] + [element[1] for element in elements_organic]
    df = df.dropna(how='all', axis='columns')

    return df

def create_empty_dataframe(list_mp):
    elements_metal = QueryScript("SELECT sandre, parameter FROM r3 WHERE 21j_threshold IS NOT NULL AND familly='Métaux'").execute()
    elements_organic = QueryScript("SELECT sandre, parameter FROM r3 WHERE 21j_threshold IS NOT NULL AND familly!='Métaux'").execute()
    matrix = []


    for mp in list_mp:
        metal_list = ['' for element in elements_metal]
        metal = [metal_list, metal_list]
        organic_list = ['' for element in elements_organic]
        organic = [organic_list, organic_list]
        matrix.append([''] + metal[0] + [''] + organic[0])
    df = pd.DataFrame(matrix)
    df.columns = [''] + [element[1] for element in elements_metal]  + [''] + [element[1] for element in elements_organic]
    df = df.dropna(how='all', axis='columns')

    return df

## MAIN FUNCTION ##
def create_bbac_dataframe(head_dataframe, list_campaigns, dict_mp):
    list_dataframe = []
    for campaign_str in list_campaigns:
        list_mp = dict_mp[campaign_str]
        df = create_dataframe(list_mp)
        list_dataframe.append(df)

    df_values = pd.concat(list_dataframe)
    df_concat = pd.concat([head_dataframe, df_values], axis=1)
    df_campaigns = df_concat.sort_values(['Numéro', 'Campagne'])

    return df_campaigns

def create_bbac2_dataframe(head_dataframe, list_campaigns, dict_mp):
    list_dataframe = []
    for campaign_str in list_campaigns:
        list_mp = dict_mp[campaign_str]
        df = create_empty_dataframe(list_mp)
        list_dataframe.append(df)

    df_values = pd.concat(list_dataframe)
    print(head_dataframe.shape, df_values.shape)
    df_concat = pd.concat([head_dataframe, df_values], axis=1)
    df_campaigns = df_concat.sort_values(['Numéro', 'Campagne'])

    return df_campaigns

        
        