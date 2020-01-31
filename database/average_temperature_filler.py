from tools import list_to_dict, pack_finder, QueryScript
import numpy as np


def run():
    average_temperature_table = QueryScript(
        "DROP TABLE IF EXISTS average_temperature; CREATE TABLE average_temperature (id INT AUTO_INCREMENT PRIMARY KEY, measurepoint_fusion_id INT(11), sonde1_moy DOUBLE, sonde1_min DOUBLE, sonde1_max DOUBLE, sonde2_moy DOUBLE, sonde2_min DOUBLE, sonde2_max DOUBLE, sonde3_moy DOUBLE, sonde3_min DOUBLE, sonde3_max DOUBLE, sonde2_moy_labo DOUBLE );")
    average_temperature_table.execute()
    SQL_request = "INSERT INTO average_temperature (measurepoint_fusion_id, sonde1_moy, sonde1_min, sonde1_max, sonde2_moy, sonde2_min, sonde2_max, sonde3_moy, sonde3_min, sonde3_max, sonde2_moy_labo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = []

    liste_fusion_id = QueryScript(
        "SELECT DISTINCT measurepoint_fusion_id FROM datesclees").execute()

    for elt_mp_id in liste_fusion_id:
        elt_insert = liste_temperature_moyenne(elt_mp_id)
        values.append(tuple(elt_insert))

    # elt_insert = liste_temperature_moyenne(2944)
    # values.append(tuple(elt_insert))

    average_temperature_table.setScript(SQL_request)
    average_temperature_table.setRows(values)
    average_temperature_table.executemany()


# prend en argument un measurepoint_fusion_id et le numero de la sonde (1, 2 ou 3 ou 2lab qui correpond a la moyenne in situ+lab)
def liste_temperature(measurepoint_fusion_id, num_sensor):
    dates_clees = QueryScript(
        "SELECT date_id, date FROM datesclees WHERE measurepoint_fusion_id = {}".format(measurepoint_fusion_id)).execute()
    measurepoint_id = QueryScript(  # a optimiser
        "SELECT DISTINCT measurepoint_id FROM datesclees WHERE measurepoint_fusion_id = {}".format(measurepoint_fusion_id)).execute()
    dico_dates_clees = list_to_dict(dates_clees)
    sortie_valable = False
    pack_id = []
    SQL_request_temperature_sonde = []
    if (num_sensor == 1) & (dico_dates_clees[1] != None) & (dico_dates_clees[2] != None):
        SQL_request_temperature_sonde = "SELECT value FROM measuretemperature WHERE ( (recordedAt>= '{}') AND (recordedAt<= '{}')".format(
            dico_dates_clees[1], dico_dates_clees[2])
        sortie_valable = True
    elif (num_sensor == 2) & (dico_dates_clees[6] != None) & (dico_dates_clees[4] != None):
        SQL_request_temperature_sonde = "SELECT value FROM measuretemperature WHERE ( (recordedAt>= '{}') AND (recordedAt<= '{}')".format(
            dico_dates_clees[6], dico_dates_clees[4])
        sortie_valable = True
    elif (num_sensor == "2lab") & (dico_dates_clees[6] != None) & (dico_dates_clees[5] != None):
        SQL_request_temperature_sonde = "SELECT value FROM measuretemperature WHERE ( (recordedAt>= '{}') AND (recordedAt<= '{}')".format(
            dico_dates_clees[6], dico_dates_clees[5])
        sortie_valable = True
    elif (num_sensor == 3) & (dico_dates_clees[6] != None) & (dico_dates_clees[7] != None):
        SQL_request_temperature_sonde = "SELECT value FROM measuretemperature WHERE ( (recordedAt>= '{}') AND (recordedAt<= '{}')".format(
            dico_dates_clees[6], dico_dates_clees[7])
        sortie_valable = True
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

    if num_sensor in [1, 2, 3]:
        SQL_request_temperature_sonde += " AND ( nature = 'sensor{}') )".format(
            num_sensor)
    else:  # cas correspondant a 2lab, qui est la moyenne in situ+lab
        SQL_request_temperature_sonde += " AND ( nature = 'sensor{}') )".format(
            2)
    if sortie_valable:
        return QueryScript(SQL_request_temperature_sonde).execute()
    else:
        return []


def liste_temperature_moyenne(measurepoint_fusion_id):
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


# test = print(np.mean(liste_temperature(2944, 1).execute()))

# if __name__ == '__main__':
#     run()
