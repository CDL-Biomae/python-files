'''
Permet de récupérer les informations physico-chimiques pour les dates clés d'un point de mesure

[+] prend en entrée un 'measurepoint_id'
--> renvoie 3 listes:
        conductivité = [cond_J0, cond_J14, cond_JN, cond_J21]
        pH = [pH_J0, pH_J14, pH_JN, pH_J21]
        oxygene = [oxygen_J0, oxygen_J14, oxygen_JN, oxygen_J21]
'''


from tools import QueryScript
import env

def conditions(measurepoint_id):
     
    measurepoints = QueryScript(
        f" SELECT DISTINCT measurepoint_id   FROM {env.DATABASE_TREATED}.key_dates WHERE measurepoint_fusion_id = {measurepoint_id} AND version={env.VERSION}").execute()

    if len(measurepoints) < 2:
        # Si jamais il n'y a qu'un seul point de mesure
        return conditions_simple(measurepoint_id)
    else:
        # Si jamais on a 2 points de mesure on est dans un cas de fusion de point de mesure
        return conditions_fusion(measurepoints)


def conditions_fusion(measurepoints):
    [id_mp_1, id_mp_2] = measurepoints
    if id_mp_1 < id_mp_2:
        id_mp_premier = id_mp_1
        id_mp_second = id_mp_2
    else:
        id_mp_premier = id_mp_2
        id_mp_second = id_mp_1
    conductivity = []
    ph = []
    oxygen = []

    steps_barrel = [(50, "\'R0\'"), (50, "\'R0\'"),
                    (140, "\'RN\'"), (60, "\'R7\'")]

    for i in range(4):
        step, barrel = steps_barrel[i]
        if i in [0, 2]:
            measurepoint = id_mp_premier
        else:
            measurepoint = id_mp_second

        try:
            output = QueryScript(
                f"  SELECT conductivity, ph, oxygen   FROM {env.DATABASE_RAW}.measureexposurecondition WHERE measurepoint_id = {measurepoint} and step = {step} and barrel = {barrel}").execute()
            output = output[0]
        except IndexError:
            output = [None, None, None]
        conductivity.append(output[0])
        ph.append(output[1])
        oxygen.append(output[2])

    return (conductivity, ph, oxygen)


def conditions_simple(measurepoint_id):
    conductivity = []
    ph = []
    oxygen = []

    steps_barrel = [(50, "\'R0\'"), (60, "\'R7\'"),
                    (140, "\'RN\'"), (100, "\'R21\'")]

    for i in range(4):
        step, barrel = steps_barrel[i]

        try:
            output = QueryScript(
                f"  SELECT conductivity, ph, oxygen   FROM {env.DATABASE_RAW}.measureexposurecondition WHERE measurepoint_id = {measurepoint_id} and step = {step} and barrel = {barrel}").execute()
            output = output[0]
        except IndexError:
            output = [None, None, None]
        conductivity.append(output[0])
        ph.append(output[1])
        oxygen.append(output[2])

    return conductivity, ph, oxygen
