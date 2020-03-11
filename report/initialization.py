from tools import QueryScript, list_agency_finder, translate
import pandas as pd
import env

## OUTILS ##
def agency_mp(list_mp):
    list_agency = list_agency_finder(list_mp)
    return list_agency


def campaign(campaign_ref):
    '''
    Permet de récupérer le numéro de campagne, càd les deux derniers numéros quand on lit sa référence
    :param campaign_ref:
    :return: numéro: numéro de campagne
    '''
    return int(campaign_ref[-2:])


def measure_points(campaign_ref):
    '''
    Récupère les points de mesure (fusion s'il y en a) associés à une référence de campagne
    :param campaign_ref:
    :return: list_mp: Liste de points de mesures
    '''
    output = QueryScript(
        f"SELECT DISTINCT(measurepoint_fusion_id) FROM {env.DATABASE_TREATED}.key_dates WHERE measurepoint_id IN (SELECT id FROM {env.DATABASE_RAW}.Measurepoint WHERE reference LIKE '{campaign_ref}%') and version=  {env.CHOSEN_VERSION()};"
    ).execute()
    if len(output) == 0:
        raise NameError('\n\n     /!\\ La référence de campagne demandée n\'existe pas dans la base de donnée /!\\')
    return output


def number_name_mp(list_mp):
    '''
    Renvoie les numéro et les noms associés à une liste de points de mesure
    :param list_mp:
    :return: list_number, list_name: Liste des numéro et liste des noms
    '''
    if len(list_mp) > 1:
        query_tuple_mp = tuple(list_mp)
    else:
        query_tuple_mp = f"({list_mp[0]})"
    output = QueryScript(
        f"SELECT Measurepoint.id, substring(place.reference, -2, 2), Measurepoint.name FROM {env.DATABASE_RAW}.Measurepoint JOIN {env.DATABASE_RAW}.Place ON place.id = Measurepoint.place_id WHERE Measurepoint.id in {query_tuple_mp}"
    ).execute()

    list_number = []
    list_name = []
    list_mp_output = [x[0] for x in output]
    for mp_id in list_mp:
        try:
            idx_code = list_mp_output.index(mp_id)
        except ValueError:
            list_number.append(None)
            list_name.append(None)
        else:
            list_number.append(output[idx_code][1])
            list_name.append(output[idx_code][2])

    return list_number, list_name


## CREATION D'UNE DATAFRAME POUR UNE REFERENCE DE CAMPAGNE ##
def clean(dataframe):
    '''
    Enlève les colonnes vides d'une dataframe
    :param dataframe:
    :return: dataframe_cleaned:
    '''
    df = dataframe.dropna(how='all', axis='columns')
    return df


def create_dataframe(campaign_str):
    '''
    Créé une dataframe à partir d'un référence de campagne.
    Les colonnes de la dataframe sont ['Campagne', 'Numéro', 'Station de mesure', 'Code Agence']
    :param campaign_str:
    :return: dataframe:
    '''
    campaign_id = campaign(campaign_str)
    list_mp = measure_points(campaign_str)
    list_number, list_name = number_name_mp(list_mp)
    list_agency = agency_mp(list_mp)

    matrix = []

    for i in range(len(list_mp)):
        number = int(list_number[i])
        name = list_name[i]
        agency = list_agency[i]

        temp = [campaign_id, number, translate(name), agency]
        matrix.append(temp)

    df = pd.DataFrame(matrix)
    df.columns = ['Campagne', 'Numéro', 'Station de mesure', 'Code Agence']
    return df


## DONNE LE DEBUT DE CHAQUE TABLEAU DU EXCEL ##
def create_head_dataframe(list_campaigns):
    '''
    Créé une dataframe qui correspond au premières colonnes de chaque excel.
    Cette dataframe est réalisé grâce à une concaténation des résultats des appels à la fonction create_dataframe.
    :param list_campaigns:
    :return:
    '''
    list_dataframe = []
    for campaign_str in list_campaigns:
        df = create_dataframe(campaign_str)
        list_dataframe.append(df)

    df_concat = pd.concat(list_dataframe)
    df_cleaned = df_concat
    return df_cleaned

