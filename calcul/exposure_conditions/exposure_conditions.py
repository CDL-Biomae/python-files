from tools import QueryScript

def conditions(measurepoint_id):
    measurepoints = QueryScript(f"SELECT DISTINCT measurepoint_id FROM key_dates WHERE measurepoint_fusion_id = {measurepoint_id}").execute()

    if len(measurepoints) < 2:
        return conditions_simple(measurepoint_id)
    else:
        return conditions_fusion(measurepoints)

def conditions_fusion(measurepoints):
    [id_mp_1, id_mp_2] = measurepoints
    conductivity = []
    ph = []
    oxygen = []

    steps_barrel = [(50, "\'R0\'"), (50, "\'R0\'"), (140, "\'RN\'"), (60, "\'R7\'")]

    for i in range(4):
        step, barrel = steps_barrel[i]
        if i in [0, 2]:
            measurepoint = id_mp_2
        else:
            measurepoint = id_mp_1

        print(step, barrel, measurepoint)
        try:
            output = QueryScript(f"SELECT conductivity, ph, oxygen FROM measureexposurecondition WHERE measurepoint_id = {measurepoint} and step = {step} and barrel = {barrel}").execute()
            output = output[0]
        except IndexError:
            output = [None, None, None]
        print(output)
        conductivity.append(output[0])
        ph.append(output[1])
        oxygen.append(output[2])

    return (conductivity, ph, oxygen)

def conditions_simple(measurepoint_id):
    conductivity = []
    ph = []
    oxygen = []

    steps_barrel = [(50, "\'R0\'"), (60, "\'R7\'"), (140, "\'RN\'"), (100, "\'R21\'")]

    for i in range(3):
        step, barrel = steps_barrel[i]

        try:
            output = QueryScript(
                f"SELECT conductivity, ph, oxygen FROM measureexposurecondition WHERE measurepoint_id = {measurepoint_id} and step = {step} and barrel = {barrel}").execute()
            output = output[0]
        except IndexError:
            output = [None, None, None]

        conductivity.append(output[0])
        ph.append(output[1])
        oxygen.append(output[2])
    return conductivity, ph, oxygen