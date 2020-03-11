from calcul.chemistry import survival
from tools import QueryScript
import pandas as pd
import env

def list_pack_from_list_mp(list_mp):
    '''
    Permet de récupérer une liste de pack de type chimie à partir d'une liste de points de mesures.
    :param list_mp:
    :return: list_pack:
    '''
    if len(list_mp) > 1:
        query_tuple_mp = tuple(list_mp)
    else:
        query_tuple_mp = f"({list_mp[0]})"
    output = QueryScript(
        f" SELECT DISTINCT key_dates.measurepoint_fusion_id, Pack.id   FROM {env.DATABASE_RAW}.Pack JOIN {env.DATABASE_TREATED}.key_dates ON key_dates.measurepoint_id = Pack.measurepoint_id WHERE key_dates.version=  {env.CHOSEN_VERSION()} AND key_dates.measurepoint_fusion_id IN {query_tuple_mp} and Pack.nature = 'chemistry';"
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
    '''
    Créé une dataframe à partir d'une liste de points de mesures
    La colonne de la dataframe est ['Survie biotest chimie']
    :param list_mp:
    :return: dataframe:
    '''
    list_pack = list_pack_from_list_mp(list_mp)
    matrix = []

    for pack in list_pack:
        survie = survival(pack)
        matrix.append(survie)

    df = pd.DataFrame(matrix)
    df.columns = ['Survie biotest chimie']

    return df


def create_survie_dataframe(head_dataframe, list_campaigns, dict_mp):
    '''
    Créé une dataframe qui contient les données de l'onglet 'survie' de l'Excel
    :param head_dataframe: cf initialization.py
    :param list_campaigns: list des references de campagne
    :param dict_mp: {'ref_campagne': [mp, ...], ...}
    :return:
    '''
    list_dataframe = []
    for campaign_str in list_campaigns:
        list_mp = dict_mp[campaign_str]
        df = create_dataframe(list_mp)
        list_dataframe.append(df)

    df_values = pd.concat(list_dataframe)
    df_concat = pd.concat([head_dataframe, df_values], axis=1)
    df_survie = df_concat.sort_values(['Numéro', 'Campagne'])

    return df_survie
