from query import QueryScript
from tools import list_to_dict, pack_finder, QueryScript
import numpy as np


def run():
    average_temperature_table = QueryScript(
        "DROP TABLE IF EXISTS average_temperature_table; CREATE TABLE reference_date (id INT AUTO_INCREMENT PRIMARY KEY, measurepoint_fusion_id INT(11), sonde1_moy DOUBLE, sonde1_min DOUBLE, sonde1_max DOUBLE, sonde2_moy DOUBLE, sonde2_min DOUBLE, sonde2_max DOUBLE, sonde3_moy DOUBLE, sonde3_min DOUBLE, sonde3_max DOUBLE, sonde2_moy_labo DOUBLE );")
    average_temperature_table.execute()
    SQL_request = "INSERT INTO average_temperature_table (measurepoint_fusion_id, sonde1_moy, sonde1_min, sonde1_max, sonde2_moy, sonde2_min, sonde2_max, sonde3_moy, sonde3_min, sonde3_max, sonde2_moy_labo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = []

    liste_fusion_id = QueryScript(
        "SELECT DISTINCT measurepoint_fusion_id FROM datesclees").execute()

    # for elt_mp_id in liste_fusion_id:

    #     dates_clees = QueryScript(
    #         "SELECT date_id, date FROM datesclees WHERE measurepoint_fusion_id = {}".format(elt)).execute()
    #     measurepoint_id = QueryScript(
    #         "SELECT DISTINCT measurepoint_id FROM datesclees WHERE measurepoint_fusion_id = {}".format(elt)).execute()
    #     dico_dates_clees = list_to_dict(dates_clees)
    #     pack_id = []
    #     SQL_request_temperature_sonde1 = "SELECT value FROM measuretemperature WHERE ( (recordedAt>= {}) AND (recordedAt<= {})".format(
    #         dico_dates_clees[1], dico_dates_clees[2])
    #     SQL_request_temperature_sonde1 += " AND ( measurepoint_id IN("
    #     for mp_id in measurepoint_id:
    #         SQL_request_temperature_sonde1 += "{},".format(mp_id)
    #         pack_id += pack_finder(mp_id)

    #     SQL_request_temperature_sonde1 += ") OR pack_id IN("
    #     for pck_id in pack_id:
    #         SQL_request_temperature_sonde1 += "{},".format(pck_id)
    #     SQL_request_temperature_sonde1 += ") )"

    #     SQL_request_temperature_sonde1 += " AND ( nature = 'sensor1') )"

    # average_temperature_table.setScript(SQL_request)
    # average_temperature_table.setRows(values)
    # average_temperature_table.executemany()

    # prend en argument un measurepoint_id et le numero de la sonde (1, 2 ou 3)
    return None


def liste_temperature(measurepoint_id, num_sensor):
    dates_clees = QueryScript(
        "SELECT date_id, date FROM datesclees WHERE measurepoint_fusion_id = {}".format(measurepoint_id)).execute()
    measurepoint_id = QueryScript(
        "SELECT DISTINCT measurepoint_id FROM datesclees WHERE measurepoint_fusion_id = {}".format(measurepoint_id)).execute()
    dico_dates_clees = list_to_dict(dates_clees)
    pack_id = []
    SQL_request_temperature_sonde = "SELECT value FROM measuretemperature WHERE ( (recordedAt>= '{}') AND (recordedAt<= '{}')".format(
        dico_dates_clees[1], dico_dates_clees[2])
    SQL_request_temperature_sonde += " AND ( measurepoint_id IN("
    for mp_id in measurepoint_id:
        SQL_request_temperature_sonde += "{},".format(mp_id)
        pack_id += pack_finder(mp_id)
    SQL_request_temperature_sonde = SQL_request_temperature_sonde[:-1]

    SQL_request_temperature_sonde += ") OR pack_id IN("
    for pck_id in pack_id:
        SQL_request_temperature_sonde += "{},".format(pck_id)
    SQL_request_temperature_sonde = SQL_request_temperature_sonde[:-1]
    SQL_request_temperature_sonde += ") )"

    SQL_request_temperature_sonde += " AND ( nature = 'sensor{}') )".format(
        num_sensor)
    return QueryScript(SQL_request_temperature_sonde)


test = print(np.mean(liste_temperature(2944, 1).execute()))

# if __name__ == '__main__':
#     run()
