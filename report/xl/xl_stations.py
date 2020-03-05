from tools import QueryScript, list_to_dict, translate
import pandas as pd
import env

def create_dataframe(list_mp):
    '''
    Créé une dataframe à partir d'une liste de points de mesures
    Les colonnes de la dataframe sont ['Type de réseau', 'Hydroécorégion', 'Masse d\'eau', 'Adresse', 'Coordonnées de référence', 'Coordonnées de référence (Lambert)', 'Coordonnées réelles']
    Les colonnes vides sont supprimées
    :param list_mp:
    :return: dataframe:
    '''
    if len(list_mp) > 1:
        query_tuple_mp = tuple(list_mp)
    else:
        query_tuple_mp = f"({list_mp[0]})"
    output_agency = QueryScript(
        f"  SELECT measurepoint.id, agency.network, agency.hydroecoregion FROM {env.DATABASE_RAW}.agency JOIN {env.DATABASE_RAW}.place on agency.id = place.agency_id JOIN {env.DATABASE_RAW}.measurepoint on place.id = measurepoint.place_id WHERE measurepoint.id IN {query_tuple_mp};"
    ).execute()
    output_measurepoint = QueryScript(
        f"  SELECT id, stream, zipcode, city, latitude, longitude, lambertY, lambertX, latitudeSpotted, longitudeSpotted   FROM {env.DATABASE_RAW}.measurepoint WHERE id IN {query_tuple_mp};"
    ).execute()

    dict_output_agency = list_to_dict(output_agency)
    dict_output_measurepoint = list_to_dict(output_measurepoint)
    matrix = []
    for mp in list_mp:
        try:
            data_agency = dict_output_agency[mp]
        except KeyError:
            data_agency = ['ND']*2
        try:
            data_measurepoint = dict_output_measurepoint[mp]
        except KeyError:
            data_measurepoint = ['ND']*9

        [network, hydroecoregion, ] = [translate(x) for x in data_agency]
        [stream, zipcode, city, latitude, longitude, lambertY, lambertX, real_latitude, real_longitude] = [translate(x) for x in data_measurepoint]

        address = f"{zipcode} {city}"
        coor_ref = f"{latitude}, {longitude}"
        coor_ref_lambert = f"Y {lambertY}, X {lambertX}"
        coor_real = f"{real_latitude}, {real_longitude}"

        temp = [network, hydroecoregion, stream, address, coor_ref, coor_ref_lambert, coor_real]
        matrix.append(temp)

    df = pd.DataFrame(matrix)
    df.columns = ['Type de réseau', 'Hydroécorégion', 'Masse d\'eau', 'Adresse', 'Coordonnées de référence', 'Coordonnées de référence (Lambert)', 'Coordonnées réelles']
    return df

def create_stations_dataframe(head_dataframe, list_campaigns, dict_mp):
    '''
    Créé une dataframe qui contient les données de l'onglet 'stations' de l'Excel
    :param head_dataframe: cf initialization.py
    :param list_campaigns: list des references de campagne
    :param dict_mp: {'ref_campagne': [mp, ...], ...}
    :return:
    '''
    campaign_str = list_campaigns[0]
    list_mp = dict_mp[campaign_str]
    nb_mp = len(list_mp)

    df_head = head_dataframe.head(nb_mp)
    df_filtered = df_head[['Numéro', 'Station de mesure', 'Code Agence']]
    df_renamed = df_filtered.rename(columns={"Numéro": "#"})

    df_values = create_dataframe(list_mp)
    df_concat = pd.concat([df_renamed, df_values], axis=1)
    df_stations = df_concat.sort_values('#')

    return df_stations


