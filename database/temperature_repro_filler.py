from tools import QueryScript, list_to_dict
from math import exp
import env

def fill_temperature_repro(cas, temperatures):
    ## Cas 1: Création et remplissage de la base de données
    if cas == 1:
        QueryScript(f'DROP TABLE IF EXISTS {env.DATABASE_TREATED}.temperature_repro').execute()
        temperature_repro_table = QueryScript(
            f"CREATE TABLE {env.DATABASE_TREATED}.temperature_repro (id INT AUTO_INCREMENT PRIMARY KEY, measurepoint_id INT(11), av_cycle_BCD1 DOUBLE, expected_C2 DOUBLE, expected_D1 DOUBLE, expected_D2 DOUBLE, av_cycle_1234 DOUBLE, expected_st3 DOUBLE, expected_st4 DOUBLE, expected_st5 DOUBLE, version INT );")
        temperature_repro_table.execute(admin=True)
    ## Cas 2: Mise à jour de la dernière version connue
    if cas == 2:
        QueryScript(f"DELETE FROM {env.DATABASE_TREATED}.temperature_repro WHERE version = {env.LATEST_VERSION()} and measurepoint_id in {tuple(temperatures['need_update']) if len(temperatures['need_update']) else '(0)'};").execute(admin=True)

    SQL_request = QueryScript(f" INSERT INTO {env.DATABASE_TREATED}.temperature_repro (measurepoint_id, av_cycle_BCD1, expected_C2, expected_D1, expected_D2, av_cycle_1234, expected_st3, expected_st4, expected_st5, version) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
    values = []

    liste_id = QueryScript(
        f" SELECT measurepoint_id FROM {env.DATABASE_TREATED}.average_temperature WHERE version=  {env.LATEST_VERSION()}").execute()

    constantes = QueryScript(
        f" SELECT name,value FROM {env.DATABASE_TREATED}.r2_constant WHERE nature='Temperature repro' and version=  {env.LATEST_VERSION()}").execute()
    constantes = list_to_dict(constantes)

    
    constante_duree_femelle = int(QueryScript(
        f" SELECT value   FROM {env.DATABASE_TREATED}.r2_constant WHERE name='FEMELLES'").execute()[0])
    for elt_mp_id in liste_id:
        if elt_mp_id in temperatures['need_update']:
            elt_insert = [elt_mp_id]
            if "sensor2lab" in temperatures["data"][elt_mp_id]:
                liste_tempe = temperatures["data"][elt_mp_id]["sensor2lab"]
            else :
                liste_tempe = []
            if len(liste_tempe) > 0:
                # Valeurs associées à %BCD1
                av_cycle_BCD1 = calcul_av_cycle(constante_duree_femelle,constantes['Constante %BCD1-1'], constantes['Constante %BCD1-2'],
                                                constantes['Constante %BCD1-3'], constantes['Constante %BCD1-4'], liste_tempe)
                expected_C2 = fct_aux_expected_percent(
                    constantes["Constante %attendu C2-1"], constantes["Constante %attendu C2-2"], av_cycle_BCD1)
                expected_D1 = fct_aux_expected_percent(
                    constantes["Constante %attendu D1-1"], constantes["Constante %attendu D1-2"], av_cycle_BCD1)
                expected_D2 = fct_aux_expected_percent(
                    constantes["Constante %attendu D2-1"], constantes["Constante %attendu D2-2"], av_cycle_BCD1)
                # Valeurs associées à %1234
                av_cycle_1234 = calcul_av_cycle(constante_duree_femelle,constantes['Constante %1234-1'], constantes['Constante %1234-2'],
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
    if len(values):
        SQL_request.setRows(values)
        SQL_request.executemany()


def calcul_av_cycle(constante_duree_femelle, alpha, beta, gamme, delta, liste_tempe):
    somme = constante_duree_femelle * \
        fct_aux_av_cycle(alpha, beta, gamme, delta, liste_tempe[0])
    for temperature in liste_tempe:
        somme += fct_aux_av_cycle(alpha, beta, gamme, delta, temperature)
    return somme


def fct_aux_expected_percent(alpha, beta, x):
    expo = exp(-(alpha + beta*x))
    return 100/(1+expo)


def fct_aux_av_cycle(alpha, beta, gamma, delta, temp):
    numerateur = alpha + beta*temp
    denominateur = gamma + delta*temp
    return (100*numerateur) / (24*denominateur)


def run(cas, temperatures):
    ## On a 3 cas pour les requêtes SQL
    # Cas 1: 'première_version'
    # Cas 2: 'update_version'
    # Cas 3: 'nouvelle_version'
    
    print("--> temperature_repro table")
    fill_temperature_repro(cas, temperatures)
    print("--> temperature_repro table ready")