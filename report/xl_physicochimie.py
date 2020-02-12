from tools import QueryScript
import pandas as pd
from calcul.exposure_conditions.exposure_conditions import conditions

def list_of_list_to_dict(list_of_list):
    dictionnary = {}
    for line in list_of_list:
        key, value = line[0], line[1:]
        dictionnary[key] = value
    return dictionnary


def test_chimie_superieur_repro(list_mp):
    output_date1 = QueryScript(
        f"SELECT measurepoint_id, date FROM key_dates WHERE date_id = 1 and measurepoint_fusion_id IN {tuple(list_mp)}"
    ).execute()
    output_date4 = QueryScript(
        f"SELECT measurepoint_id, date FROM key_dates WHERE date_id = 4 and measurepoint_fusion_id IN {tuple(list_mp)}"
    ).execute()
    output_date6 = QueryScript(
        f"SELECT measurepoint_id, date FROM key_dates WHERE date_id = 6 and measurepoint_fusion_id IN {tuple(list_mp)}"
    ).execute()
    output_date7 = QueryScript(
        f"SELECT measurepoint_id, date FROM key_dates WHERE date_id = 7 and measurepoint_fusion_id IN {tuple(list_mp)}"
    ).execute()

    dict_date1 = list_of_list_to_dict(output_date1)
    dict_date4 = list_of_list_to_dict(output_date4)
    dict_date6 = list_of_list_to_dict(output_date6)
    dict_date7 = list_of_list_to_dict(output_date7)

    n = len(list_mp)
    dict_date1467 = {}  # {mp: [date1, date4, date6, date7]}
    for mp in list_mp:
        try:
            date1 = dict_date1[mp][0]
        except KeyError:
            date1 = None
        try:
            date4 = dict_date4[mp][0]
        except KeyError:
            date4 = None
        try:
            date6 = dict_date6[mp][0]
        except KeyError:
            date6 = None
        try:
            date7 = dict_date7[mp][0]
        except KeyError:
            date7 = None

        dict_date1467[mp] = [date1, date4, date6, date7]

    list_test = []
    for i in range(n):
        mp = list_mp[i]
        [R0, RN, debut_chimie, fin_chimie] = dict_date1467[mp]

        if RN == None or R0 == None:
            delta_repro = None
        else:
            delta_repro = (RN - R0).days

        if debut_chimie == None or fin_chimie == None:
            delta_chimie = None
        else:
            delta_chimie = (fin_chimie - debut_chimie).days

        try:
            boolean = delta_chimie > delta_repro
        except TypeError:
            boolean = (delta_chimie != None)

        list_test.append(boolean)

    return list_test



def temperatures_dataframe(list_mp):
    list_test = test_chimie_superieur_repro(list_mp)
    output = QueryScript(
        f"SELECT sensor2_min, sensor2_average, sensor2_max, sensor3_min, sensor3_average, sensor3_max FROM average_temperature WHERE measurepoint_fusion_id IN {tuple(list_mp)}"
    ).execute()

    matrix = []
    n = len(list_mp)
    for i in range(n):
        test = list_test[i]
        [sensor2_min, sensor2_average, sensor2_max, sensor3_min, sensor3_average, sensor3_max] = output[i]

        average = sensor3_average if test else sensor2_average
        if average == None:
            average = 'NA'
        else:
            average = round(average, 1)

        try:
            minimum = round(min(sensor2_min, sensor3_min), 1)
        except TypeError:
            if sensor3_min == None and sensor2_min == None:
                minimum = 'NA'
            else:
                minimum = round(sensor2_min, 1) if sensor3_min == None else round(sensor3_min, 1)

        try:
            maximum = round(max(sensor2_max, sensor3_max), 1)
        except TypeError:
            if sensor3_max == None and sensor2_max == None:
                maximum = 'NA'
            else:
                maximum = round(sensor2_max, 1) if sensor3_max == None else round(sensor3_max, 1)

        matrix.append(['', minimum, average, maximum])

    df = pd.DataFrame(matrix)
    df.columns = ['', 'Temperature minimum', 'Temperature moyenne', 'Temperature maximum']
    return df


def values_dataframe(list_mp):
    matrix = []

    for mp in list_mp:
        list_conductivity, list_ph, list_oxygen = conditions(mp)
        values = list_conductivity + list_ph + list_oxygen
        matrix.append(values)

    df = pd.DataFrame(matrix)
    df.columns = ['Conductivité J0', 'Conductivité J14', 'Conductivité JN', 'Conductivité J21',
                  'pH J0', 'pH J14', 'pH JN', 'pH J21',
                  'Oxygène J0', 'Oxygène J14', 'Oxygène JN', 'Oxygène J21']
    df = df.dropna(how='all', axis='columns')

    return df


def create_physicochimie_dataframe(head_dataframe, list_campaigns, dict_mp):
    list_dataframe = []
    for campaign_str in list_campaigns:
        list_mp = dict_mp[campaign_str]
        df_temperature = temperatures_dataframe(list_mp)
        df_values = values_dataframe(list_mp)
        df_temperature_values = pd.concat([df_temperature, df_values], axis=1)
        list_dataframe.append(df_temperature_values)

    df_values = pd.concat(list_dataframe)
    df_concat = pd.concat([head_dataframe, df_values], axis=1)
    df_physicochimie = df_concat.sort_values('Numéro')

    return df_physicochimie
