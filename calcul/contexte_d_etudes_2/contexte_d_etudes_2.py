from tools import QueryScript
import datetime

def contexte(measurepoint_id):
    measurepoints = QueryScript(f"SELECT DISTINCT measurepoint_id FROM datesclees WHERE measurepoint_fusion_id = {measurepoint_id}").execute()

    if len(measurepoints) < 2:
        return contexte_simple(measurepoint_id)
    else:
        return contexte_fusion(measurepoints)

def contexte_fusion(measurepoints):
    [id_mp_1, id_mp_2] = measurepoints
    dates = []

    steps_barrel = [(50, "\'R0\'"), (50, "\'R0\'"), (140, "\'RN\'"), (60, "\'R7\'")]

    for i in range(4):
        step, barrel = steps_barrel[i]
        if i in [0, 2]:
            measurepoint = id_mp_2
        else:
            measurepoint = id_mp_1

        output = QueryScript(f"SELECT recordedAt FROM measureexposurecondition WHERE measurepoint_id = {measurepoint} and step = {step} and barrel = {barrel}").execute()
        if len(output) == 0:
            output.append(None)
        else:
            dates.append(output[0])

    N = (dates[2] - dates[0]).days

    cleaned_dates = [parser(dates[0]),
                     parser(dates[1]),
                     parser(dates[2]),
                     str(N),
                     parser(dates[3])]

    return cleaned_dates

def contexte_simple(measurepoint_id):
    dates = []

    steps_barrel = [(50, "\'R0\'"), (60, "\'R7\'"), (140, "\'RN\'"), (100, "\'R21\'")]

    for i in range(4):
        step, barrel = steps_barrel[i]

        output = QueryScript(
            f"SELECT recordedAt FROM measureexposurecondition WHERE measurepoint_id = {measurepoint_id} and step = {step} and barrel = {barrel}").execute()
        if len(output) == 0:
            dates.append(None)
        else:
            dates.append(output[0])

    N = (dates[2] - dates[0]).days

    cleaned_dates = [parser(dates[0]),
                     parser(dates[1]),
                     parser(dates[2]),
                     str(N),
                     parser(dates[3])]

    return cleaned_dates

def parser(date):
    if date == None:
        return None
    year = date.year
    month = date.month
    day = date.day
    return f"{day}/{month}/{year}"

print(contexte(2895))