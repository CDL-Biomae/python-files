from tools import QueryScript
from tools import list_agency_finder
import pandas as pd

## OUTILS ##
def agency_mp(list_mp):
    list_agency = list_agency_finder(list_mp)
    return list_agency


def campaign(campaign_ref):
    return int(campaign_ref[-2:])


def measure_points(campaign_ref):
    output = QueryScript(
        f"SELECT DISTINCT(measurepoint_fusion_id) FROM key_dates WHERE measurepoint_id IN (SELECT id FROM measurepoint WHERE reference LIKE '{campaign_ref}%');"
    ).execute()
    if len(output) == 0:
        raise NameError('\n\n     /!\\ La référence de campagne demandée n\'existe pas dans la base de donnée /!\\')
    return output


def number_name_mp(list_mp):
    output = QueryScript(
        f"SELECT measurepoint.id, substring(place.reference, -2, 2), measurepoint.name FROM measurepoint JOIN place ON place.id = measurepoint.place_id WHERE measurepoint.id in {tuple(list_mp)}"
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
    df = dataframe.dropna(how='all', axis='columns')
    return df


def create_dataframe(campaign_str):
    campaign_id = campaign(campaign_str)
    list_mp = measure_points(campaign_str)
    list_number, list_name = number_name_mp(list_mp)
    list_agency = agency_mp(list_mp)

    matrix = []

    for i in range(len(list_mp)):
        number = int(list_number[i])
        name = list_name[i]
        agency = list_agency[i]

        temp = [campaign_id, number, name, agency]
        matrix.append(temp)

    df = pd.DataFrame(matrix)
    df.columns = ['Campagne', 'Numéro', 'Station de mesure', 'Code Agence']

    return df


## DONNE LE DEBUT DE CHAQUE TABLEAU DU EXCEL ##
def create_head_dataframe(list_campaigns):
    list_dataframe = []
    for campaign_str in list_campaigns:
        df = create_dataframe(campaign_str)
        list_dataframe.append(df)

    df_concat = pd.concat(list_dataframe)
    df_cleaned = clean(df_concat)
    return df_cleaned

