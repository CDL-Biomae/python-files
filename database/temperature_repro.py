from tools import QueryScript, list_to_dict
from database import liste_temperature
from math import exp
import env

def run():
     
    temperature_repro_table = QueryScript(
        f" DROP TABLE IF EXISTS {env.DATABASE_TREATED}.temperature_repro; CREATE TABLE {env.DATABASE_TREATED}.temperature_repro (id INT AUTO_INCREMENT PRIMARY KEY, measurepoint_fusion_id INT(11), av_cycle_BCD1 DOUBLE, expected_C2 DOUBLE, expected_D1 DOUBLE, expected_D2 DOUBLE, av_cycle_1234 DOUBLE, expected_st3 DOUBLE, expected_st4 DOUBLE, expected_st5 DOUBLE, version INT );")
    temperature_repro_table.execute(True)
    SQL_request = f" INSERT INTO {env.DATABASE_TREATED}.temperature_repro (measurepoint_fusion_id, av_cycle_BCD1, expected_C2, expected_D1, expected_D2, av_cycle_1234, expected_st3, expected_st4, expected_st5, version) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = []

    liste_fusion_id = QueryScript(
        f" SELECT measurepoint_fusion_id FROM {env.DATABASE_TREATED}.average_temperature WHERE version={env.VERSION}").execute()

    constantes = QueryScript(
        f" SELECT name,value FROM {env.DATABASE_TREATED}.r2_constant WHERE nature='Temperature repro' and version={env.VERSION}").execute()
    constantes = list_to_dict(constantes)
    print(env.VERSION)
    print(constantes)

    count = 1
    for elt_mp_id in liste_fusion_id:
        #elt_mp_id = 2895
        print(elt_mp_id, count)
        elt_insert = [elt_mp_id]
        liste_tempe = liste_temperature(elt_mp_id, "2lab")
        if len(liste_tempe) > 0:
            # Valeurs associées à %BCD1
            av_cycle_BCD1 = calcul_av_cycle(constantes['Constante %BCD1-1'], constantes['Constante %BCD1-2'],
                                            constantes['Constante %BCD1-3'], constantes['Constante %BCD1-4'], liste_tempe)
            expected_C2 = fct_aux_expected_percent(
                constantes["Constante %attendu C2-1"], constantes["Constante %attendu C2-2"], av_cycle_BCD1)
            expected_D1 = fct_aux_expected_percent(
                constantes["Constante %attendu D1-1"], constantes["Constante %attendu D1-2"], av_cycle_BCD1)
            expected_D2 = fct_aux_expected_percent(
                constantes["Constante %attendu D2-1"], constantes["Constante %attendu D2-2"], av_cycle_BCD1)
            # Valeurs associées à %1234
            av_cycle_1234 = calcul_av_cycle(constantes['Constante %1234-1'], constantes['Constante %1234-2'],
                                            constantes['Constante %1234-3'], constantes['Constante %1234-4'], liste_tempe)
            expected_st3 = fct_aux_expected_percent(
                constantes["Constante %attendu st3-1"], constantes["Constante %attendu st3-2"], av_cycle_1234)
            expected_st4 = fct_aux_expected_percent(
                constantes["Constante %attendu st4-1"], constantes["Constante %attendu st4-2"], av_cycle_1234)
            expected_st5 = fct_aux_expected_percent(
                constantes["Constante %attendu st5-1"], constantes["Constante %attendu st5-2"], av_cycle_1234)

            elt_insert += [av_cycle_BCD1, expected_C2, expected_D1,
                           expected_D2, av_cycle_1234, expected_st3, expected_st4, expected_st5]
            values.append(tuple(elt_insert))
        count += 1

    temperature_repro_table.setScript(SQL_request)
    temperature_repro_table.setRows(values)
    temperature_repro_table.executemany()


def calcul_av_cycle(alpha, beta, gamme, delta, liste_tempe):
    constante_duree_femelle = int(QueryScript(
        f" SELECT value   FROM {env.DATABASE_TREATED}.r2_constant WHERE name='FEMELLES'").execute()[0])
    somme = constante_duree_femelle * \
        fct_aux_av_cycle(alpha, beta, gamme, delta, liste_tempe[0])
    for temperature in liste_tempe:
        somme += fct_aux_av_cycle(alpha, beta, gamme, delta, temperature)
    return somme


def fct_aux_expected_percent(alpha, beta, x):
    expo = exp(-(alpha + beta*x))
    return (100/(1+expo))


def fct_aux_av_cycle(alpha, beta, gamma, delta, temp):
    numerateur = alpha + beta*temp
    denominateur = gamma + delta*temp
    return((100*numerateur) / (24*denominateur))