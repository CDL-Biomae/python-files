from tools import QueryScript, list_to_dict, translate
import pandas as pd
import env

def create_stations_dataframe(head_dataframe, campaigns_dict, measurepoint_list, agency_code_list, place_list):

    df_renamed = head_dataframe.rename(columns={"Numéro": "#"})
    place_length = len(place_list)
    campaigns_number = len(list(campaigns_dict.keys()))
    global_matrix = []
    agency_data = QueryScript(f"  SELECT code, network, hydroecoregion FROM {env.DATABASE_RAW}.Agency  WHERE code IN {tuple(agency_code_list) if len(agency_code_list)>1 else '('+(str(agency_code_list[0]) if len(agency_code_list) else '0')+')'};").execute()
    measurepoint_data = QueryScript(f"  SELECT id, stream, zipcode, city, latitude, longitude, lambertY, lambertX, latitudeSpotted, longitudeSpotted   FROM {env.DATABASE_RAW}.Measurepoint WHERE id IN {tuple(measurepoint_list) if len(measurepoint_list)>1 else '('+(str(measurepoint_list[0]) if len(measurepoint_list) else '0')+')'};").execute()
    for campaign_id in campaigns_dict:


        matrix = [[None]*7]*place_length
        for place_id in campaigns_dict[campaign_id]["place"]:
           
            temp = [None]*7
            for code, network, hydroecoregion in agency_data:
                if "agency" in campaigns_dict[campaign_id]["place"][place_id] and code==campaigns_dict[campaign_id]["place"][place_id]["agency"]:
                    temp[0],temp[1]=translate(network), hydroecoregion

            for measurepoint_id in campaigns_dict[campaign_id]["place"][place_id]["measurepoint"]:
                for row in measurepoint_data:
                    [mp_id, stream, zipcode, city, latitude, longitude, lambertY, lambertX, latitudeSpotted, longitudeSpotted] = [translate(x) for x in row]
                    if mp_id==measurepoint_id:
                        if not temp[2]:
                            temp[2] = stream
                        if not temp[3]:
                            temp[3] = f"{zipcode} {city}" if zipcode and city else None
                        if not temp[4]:
                            temp[4] = f"{latitude}, {longitude}" if latitude and longitude else None
                        if not temp[5]:
                            temp[5] = f"Y {lambertY}, X {lambertX}" if lambertX and lambertY else None
                        if not temp[6]:
                            temp[6] = f"{latitudeSpotted}, {longitudeSpotted}" if latitudeSpotted and longitudeSpotted else None
            matrix[place_list.index(campaigns_dict[campaign_id]["place"][place_id]["number"])] = temp
        global_matrix.append(matrix)

    matrix_filled = [[None]*7]*place_length
    if campaigns_number>1:
        for campaign in global_matrix :
            for place_number in range(place_length) :
                for index, content in enumerate(campaign[place_number]):
                    if content and not matrix_filled[place_number][index]:
                        matrix_filled[place_number] = campaign[place_number]
    if campaigns_number==1:
        matrix_filled=global_matrix[0]

    for place_number, place in enumerate(matrix_filled) :
        for index, content in enumerate(place) :
            if not content :
                matrix_filled[place_number][index] = 'ND'
   
    df_values = pd.DataFrame(matrix_filled, columns=['Type de réseau', 'Hydroécorégion', 'Masse d\'eau', 'Adresse', 'Coordonnées de référence', 'Coordonnées de référence (Lambert)', 'Coordonnées réelles'])
    df_values.columns = ['Type de réseau', 'Hydroécorégion', 'Masse d\'eau', 'Adresse', 'Coordonnées de référence', 'Coordonnées de référence (Lambert)', 'Coordonnées réelles']
    df_concat = pd.concat([df_renamed, df_values], axis=1)
    df_stations = df_concat.sort_values('#')

    return df_stations


