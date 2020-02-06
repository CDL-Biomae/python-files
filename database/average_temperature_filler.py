from tools import list_to_dict, pack_finder, QueryScript
import numpy as np


def run():
    average_temperature_table = QueryScript(
        "DROP TABLE IF EXISTS average_temperature; CREATE TABLE average_temperature (id INT AUTO_INCREMENT PRIMARY KEY, measurepoint_fusion_id INT(11), sensor1_average DOUBLE, sensor1_min DOUBLE, sensor1_max DOUBLE, sensor2_average DOUBLE, sensor2_min DOUBLE, sensor2_max DOUBLE, sensor3_average DOUBLE, sensor3_min DOUBLE, sensor3_max DOUBLE, sensor2_average_labo DOUBLE );")
    average_temperature_table.execute()
    SQL_request = "INSERT INTO average_temperature (measurepoint_fusion_id, sensor1_average, sensor1_min, sensor1_max, sensor2_average, sensor2_min, sensor2_max, sensor3_average, sensor3_min, sensor3_max, sensor2_average_labo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = []

    liste_fusion_id = QueryScript(
        "SELECT DISTINCT measurepoint_fusion_id FROM key_dates").execute()

    count = 1
    for elt_mp_id in liste_fusion_id:
        print(elt_mp_id, count)
        elt_insert = average_temperature_list(elt_mp_id)
        values.append(tuple(elt_insert))
        count += 1

    average_temperature_table.setScript(SQL_request)
    average_temperature_table.setRows(values)
    average_temperature_table.executemany()


# prend en argument un measurepoint_fusion_id et le numero de la sensor (1, 2 ou 3 ou 2lab qui correpond a la moyenne in situ+lab)
def liste_temperature(measurepoint_fusion_id, num_sensor):
    key_date_list_measurepoint_id = QueryScript(
        "SELECT date_id, date, measurepoint_id FROM key_dates WHERE measurepoint_fusion_id = {}".format(measurepoint_fusion_id)).execute()
    # measurepoint_id = QueryScript(  # a optimiser
    #     "SELECT DISTINCT measurepoint_id FROM key_dates WHERE measurepoint_fusion_id = {}".format(measurepoint_fusion_id)).execute()
    key_date_list = [elt[:-1] for elt in key_date_list_measurepoint_id]
    measurepoint_id = [elt[-1] for elt in key_date_list_measurepoint_id]
    measurepoint_id = list(set(measurepoint_id))

    if None in measurepoint_id:
        measurepoint_id.remove(None)

    pack_id = []
    for mp_id in measurepoint_id:
        pack_id += pack_finder(mp_id)
    if len(pack_id) == 0:
        return []

    dict_key_date_list = list_to_dict(key_date_list)
    valid_output = False

    SQL_request_temperature_sensor = []
    if (num_sensor == 1) & (dict_key_date_list[1] != None) & (dict_key_date_list[2] != None):
        SQL_request_temperature_sensor = "SELECT value FROM measuretemperature WHERE ( (recordedAt>= '{}') AND (recordedAt<= '{}')".format(
            dict_key_date_list[1], dict_key_date_list[2])
        valid_output = True
    elif (num_sensor == 2) & (dict_key_date_list[6] != None) & (dict_key_date_list[4] != None):
        SQL_request_temperature_sensor = "SELECT value FROM measuretemperature WHERE ( (recordedAt>= '{}') AND (recordedAt<= '{}')".format(
            dict_key_date_list[6], dict_key_date_list[4])
        valid_output = True
    elif (num_sensor == "2lab") & (dict_key_date_list[6] != None) & (dict_key_date_list[5] != None):
        SQL_request_temperature_sensor = "SELECT value FROM measuretemperature WHERE ( (recordedAt>= '{}') AND (recordedAt<= '{}')".format(
            dict_key_date_list[6], dict_key_date_list[5])
        valid_output = True
    elif (num_sensor == 3) & (dict_key_date_list[6] != None) & (dict_key_date_list[7] != None):
        SQL_request_temperature_sensor = "SELECT value FROM measuretemperature WHERE ( (recordedAt>= '{}') AND (recordedAt<= '{}')".format(
            dict_key_date_list[6], dict_key_date_list[7])
        valid_output = True

    if len(measurepoint_id) > 1:
        SQL_request_temperature_sensor += f" AND ( measurepoint_id IN{tuple(measurepoint_id)}"
    else:
        SQL_request_temperature_sensor += f" AND ( measurepoint_id IN({measurepoint_id[0]})"

    # for mp_id in measurepoint_id:
    #     SQL_request_temperature_sensor += "{},".format(mp_id)
    #     pack_id += pack_finder(mp_id)
    # SQL_request_temperature_sensor = SQL_request_temperature_sensor[:-1]
    if len(pack_id) > 1:
        SQL_request_temperature_sensor += f" OR pack_id IN{tuple(pack_id)} )"
    else:
        SQL_request_temperature_sensor += f" OR pack_id IN({pack_id[0]}) )"

    # for pck_id in pack_id:
    #     SQL_request_temperature_sensor += "{},".format(pck_id)
    # SQL_request_temperature_sensor = SQL_request_temperature_sensor[:-1]
    # SQL_request_temperature_sensor += ") )"

    if num_sensor in [1, 2, 3]:
        SQL_request_temperature_sensor += " AND ( nature = 'sensor{}') )".format(
            num_sensor)
    else:  # cas correspondant a 2lab, qui est la moyenne in situ+lab
        SQL_request_temperature_sensor += " AND ( nature = 'sensor{}') )".format(
            2)
    if valid_output:
        return QueryScript(SQL_request_temperature_sensor).execute()
    else:
        return []


def average_temperature_list(measurepoint_fusion_id):
    elt_insert = [measurepoint_fusion_id]
    for num_sensor in [1, 2, 3]:
        list_temp = liste_temperature(
            measurepoint_fusion_id, num_sensor)
        if list_temp != []:
            elt_insert += [np.average(list_temp),
                           min(list_temp), max(list_temp)]
        else:
            elt_insert += [None, None, None]

    list_temp = liste_temperature(measurepoint_fusion_id, "2lab")
    if list_temp != []:
        elt_insert += [np.average(list_temp)]
    else:
        elt_insert += [None]
    return elt_insert

