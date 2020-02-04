from tools import QueryScript
from database import liste_temperature
from math import exp


def run():
    temperature_repro_table = QueryScript(
        "DROP TABLE IF EXISTS temperature_repro; CREATE TABLE temperature_repro (id INT AUTO_INCREMENT PRIMARY KEY, measurepoint_fusion_id INT(11), av_cycle_%_BCD1 DOUBLE, expected_%C2 DOUBLE, expected_%D1 DOUBLE, expected_%D2 DOUBLE, av_cycle_%_1234 DOUBLE, expected_%_st3 DOUBLE, expected_%_st4 DOUBLE, expected_%_st5 DOUBLE );")
    temperature_repro_table.execute()
    SQL_request = "INSERT INTO temperature_repro (measurepoint_fusion_id, av_cycle_%_BCD1, expected_%C2, expected_%D1, expected_%D2, av_cycle_%_1234, expected_%_st3, expected_%_st4, expected_%_st5) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = []

    liste_fusion_id = QueryScript(
        "SELECT measurepoint_fusion_id FROM average_temperature").execute()

    compteur = 1
    for elt_mp_id in liste_fusion_id:
        print(elt_mp_id, compteur)
        elt_insert = []
        values.append(tuple(elt_insert))
        compteur += 1

    temperature_repro_table.setScript(SQL_request)
    temperature_repro_table.setRows(values)
    temperature_repro_table.executemany()


def fct_aux_expected_percent(alpha, beta, x):
    expo = exp(-(alpha + beta*x))
    return (100/(1+expo))


def fct_aux_av_cylce(alpha, beta, gamma, delta, temp):
    numerateur = alpha + beta*temp
    denominateur = gamme + delta*temp
    return((100*numerateur) / (24*denominateur))
