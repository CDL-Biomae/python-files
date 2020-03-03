from calcul.chemistry import survival
from tools import QueryScript
import pandas as pd
import env

def list_pack_from_list_mp(list_mp):
    if len(list_mp) > 1:
        query_tuple_mp = tuple(list_mp)
    else:
        query_tuple_mp = f"({list_mp[0]})"
    output = QueryScript(
        f" SELECT DISTINCT key_dates.measurepoint_fusion_id, pack.id   FROM {env.DATABASE_RAW}.pack JOIN {env.DATABASE_TREATED}.key_dates ON key_dates.measurepoint_id = pack.measurepoint_id WHERE key_dates.version={env.VERSION} AND key_dates.measurepoint_fusion_id IN {query_tuple_mp} and pack.nature = 'chemistry';"
    ).execute()

    list_pack = []
    list_mp_output = [x[0] for x in output]
    for mp in list_mp:
        try:
            idx = list_mp_output.index(mp)
        except ValueError:
            pack = None
        else:
            pack = output[idx][1]

        list_pack.append(pack)

    return list_pack

def create_dataframe(list_mp):
    list_pack = list_pack_from_list_mp(list_mp)
    matrix = []

    for pack in list_pack:
        survie = survival(pack)
        matrix.append(survie)

    df = pd.DataFrame(matrix)
    df.columns = ['Survie biotest chimie']

    return df


def create_survie_dataframe(head_dataframe, list_campaigns, dict_mp):
    list_dataframe = []
    for campaign_str in list_campaigns:
        list_mp = dict_mp[campaign_str]
        df = create_dataframe(list_mp)
        list_dataframe.append(df)

    df_values = pd.concat(list_dataframe)
    df_concat = pd.concat([head_dataframe, df_values], axis=1)
    df_survie = df_concat.sort_values(['Numéro', 'Campagne'])

    return df_survie
