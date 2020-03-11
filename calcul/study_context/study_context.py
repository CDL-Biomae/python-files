'''
Permet de récupérer les dates clés d'un point de mesure

[+] prend en entrée un 'measurepoint_id'
--> renvoie 1 liste: [J0, J14, JN, N, J21] avec N = (JN-J14)
'''
import env
from tools import QueryScript
from datetime import date


def contexte(measurepoint_id):

    measurepoints = QueryScript(
        f" SELECT DISTINCT measurepoint_id   FROM {env.DATABASE_TREATED}.key_dates WHERE measurepoint_fusion_id = {measurepoint_id} AND version =   {env.CHOSEN_VERSION()}").execute()

    if len(measurepoints) < 2:
        return contexte_simple(measurepoint_id)
    else:
        return contexte_fusion(measurepoints)


def contexte_fusion(measurepoints):
    [id_mp_1, id_mp_2] = measurepoints
    if id_mp_1 < id_mp_2:
        id_mp_premier = id_mp_1
        id_mp_second = id_mp_2
    else:
        id_mp_premier = id_mp_2
        id_mp_second = id_mp_1

    dates = []

    steps_barrel = [(50, "\'R0\'"), (50, "\'R0\'"),
                    (140, "\'RN\'"), (60, "\'R7\'")]

    for i in range(4):
        step, barrel = steps_barrel[i]
        if i in [0, 2]:
            measurepoint = id_mp_premier
        else:
            measurepoint = id_mp_second

        output = QueryScript(
            f"  SELECT recordedAt   FROM {env.DATABASE_RAW}.MeasureExposureCondition WHERE measurepoint_id = {measurepoint} and step = {step} and barrel = {barrel}").execute()
        if len(output) == 0:
            dates.append(None)
        else:
            dates.append(output[0])

    if (dates[2] != None) & (dates[0] != None):
        N = calcul_N(dates[0], dates[2])
    else:
        N = None
    # try:
    #     N = str((dates[2] - dates[0]).days)
    # except TypeError:
    #     N = None

    cleaned_dates = [parser(dates[0]),
                     parser(dates[1]),
                     parser(dates[2]),
                     str(N),
                     parser(dates[3])]

    return cleaned_dates


def contexte_simple(measurepoint_id):
    dates = []

    steps_barrel = [(50, "\'R0\'"), (60, "\'R7\'"),
                    (140, "\'RN\'"), (100, "\'R21\'")]

    for i in range(4):
        step, barrel = steps_barrel[i]

        output = QueryScript(
            f"  SELECT recordedAt   FROM {env.DATABASE_RAW}.MeasureExposureCondition WHERE measurepoint_id = {measurepoint_id} and step = {step} and barrel = {barrel}").execute()
        if len(output) == 0:
            dates.append(None)
        else:
            dates.append(output[0])

    if (dates[2] != None) & (dates[0] != None):
        N = calcul_N(dates[0], dates[2])
    else:
        N = None
    # try:
    #     N = str((dates[2] - dates[0]).days)
    # except TypeError:
    #     N = None

    cleaned_dates = [parser(dates[0]),
                     parser(dates[1]),
                     parser(dates[2]),
                     N,
                     parser(dates[3])]

    return cleaned_dates


def parser(date):
    if date is None:
        return None
    year = date.year
    month = date.month
    day = date.day

    day = '0' + str(day) if day < 10 else str(day)
    month = '0' + str(month) if month < 10 else str(month)

    return f"{day}/{month}/{year}"


def calcul_N(date1, date2):  # date de type datetime
    date1_without_time = date(date1.year, date1.month, date1.day)
    date2_without_time = date(date2.year, date2.month, date2.day)
    delta_days = (date2_without_time - date1_without_time).days
    return delta_days
