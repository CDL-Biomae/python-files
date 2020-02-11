from tools import QueryScript
import pandas as pd

def create_dataframe(list_mp):
    output = QueryScript(
        f"SELECT agency.network, agency.hydroecoregion, agency.stream, agency.zipcode, agency.city, agency.latitude, agency.longitude, agency.lambertY, agency.lambertX, measurepoint.latitudeSpotted, measurepoint.longitudeSpotted FROM agency JOIN place on agency.id = place.agency_id JOIN measurepoint on place.id = measurepoint.place_id WHERE measurepoint.id IN {tuple(list_mp)};"
    ).execute()

    matrix = []
    for row in output:
        [network, hydroecoregion, stream, zipcode, city, latitude, longitude, lambertY, lambertX, real_latitude, real_longitude] = row

        address = f"{zipcode} {city}"
        coor_ref = f"{latitude}; {longitude}"
        coor_ref_lambert = f"Y {lambertY}; X {lambertX}"
        coor_real = f"{real_latitude}; {real_longitude}"

        print(coor_ref, coor_real)
        temp = [network, hydroecoregion, stream, address, coor_ref, coor_ref_lambert, coor_real]
        matrix.append(temp)

    df = pd.DataFrame(matrix)
    df.columns = ['Type de réseau', 'Hydroécorégion', 'Masse d\'eau', 'Adresse', 'Coordonnées de référence', 'Coordonnées de référence (lambert)', 'Coordonnées réelles']
    return df

def create_stations_dataframe(head_dataframe, list_campaigns, dict_mp):
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


