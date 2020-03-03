from tools import QueryScript
from . import elements_fish, elements_crustacean
import env

# PAS optimisé


def lyophilisation_pourcent(pack_id):
    output = QueryScript(
        f"  SELECT prefix, value, unit   FROM {env.DATABASE_RAW}.analysis WHERE sandre='/' AND pack_id={pack_id}").execute()
    if len(output):
        return f"{output[0][0]}{output[0][1]}{output[0][2]}"
    else:
        return None


def fat(pack_id):
    output = QueryScript(
        f"  SELECT prefix, value, unit   FROM {env.DATABASE_RAW}.analysis WHERE sandre=1358 AND pack_id={pack_id}").execute()
    if len(output):
        return f"{output[0][0] if output[0][0] else ''}{output[0][1] * 100}{output[0][2]}"
    else:
        return None


def weight(pack_id):
    output = QueryScript(
        f"  SELECT sampling_weight, metal_tare_bottle_weight, sampling_quantity, organic_tare_bottle_weight, organic_total_weight   FROM {env.DATABASE_RAW}.pack WHERE id={pack_id}").execute()
    if len(output):
        return [output[0][0]-output[0][1], (output[0][0]-output[0][1])/output[0][2], output[0][4]-output[0][3]]
    else:
        return None


def survival(pack_id):
    if pack_id is None:
        return None

    survival_list = QueryScript(
        f"  SELECT scud_quantity, scud_survivor   FROM {env.DATABASE_RAW}.cage WHERE pack_id={pack_id} AND scud_survivor IS NOT NULL").execute()
    if len(survival_list):
        quantity = survival_list[0][0]
        average = 0
        for replicate in survival_list:
            average += replicate[1]
        average = average / len(survival_list)
        return str(round(average / quantity * 100)) + '%'
    else:
        return None

############################


def convert_list(list_converted):
    for element in list_converted:
        if isinstance(element, list):
            try:
                element[0] = float(element[0])
            except:
                element[0] = f'{element[0]}'
        else:
            try:
                element = float(element)
            except:
                element = f'{element}'

    return list_converted


def get_unit_NQE(sandre_list):

    output = QueryScript(
        f" SELECT familly, sandre, NQE   FROM {env.DATABASE_TREATED}.r3 WHERE sandre IN {tuple(sandre_list)} AND version=  {env.CHOSEN_VERSION()}").execute()
    result = [[], [], []]
    if len(output):
        for sandre in sandre_list:
            for element in output:
                if sandre == int(float(element[1])):
                    if element[0] == 'Métaux':
                        result[0].append('mg/kg PF')
                        result[1].append(int(float(element[1])))
                        result[2].append(float(element[2])
                                         if element[2] != '' else '')

                    else:
                        result[0].append('µg/kg PF')
                        result[1].append(int(float(element[1])))
                        result[2].append(float(element[2])
                                         if element[2] != '' else '')
    return result


def get_unit(sandre_list):

    output = QueryScript(
        f" SELECT familly, sandre   FROM {env.DATABASE_TREATED}.r3 WHERE sandre IN {tuple(sandre_list)} AND version=  {env.CHOSEN_VERSION()}").execute()
    result = [[], []]
    if len(output):
        for sandre in sandre_list:
            for element in output:
                if sandre == int(float(element[1])):
                    if element[0] == 'Métaux':
                        result[0].append('mg/kg PF')
                        result[1].append(int(float(element[1])))

                    else:
                        result[0].append('µg/kg PF')
                        result[1].append(int(float(element[1])))
    return result


def result_by_packs_and_sandre(dict_pack_fusion, sandre_list=None):
    pack_dict = {}
    for element in dict_pack_fusion:
        try:
            pack_dict[dict_pack_fusion[element]['chemistry']] = element
        except KeyError:
            None
    result = {element: None for element in dict_pack_fusion}
    if not sandre_list:

        sandre_list = QueryScript(
            f" SELECT sandre   FROM {env.DATABASE_TREATED}.r3 WHERE version=  {env.CHOSEN_VERSION()}").execute()
        for index, sandre in enumerate(sandre_list):
            try:
                sandre_list[index] = float(sandre)
            except ValueError:
                sandre_list[index] = sandre

    list_pack = [element for element in pack_dict]
    if len(list_pack) > 1:
        query_tuple_pack = tuple(list_pack)
    else:
        query_tuple_pack = f"({list_pack[0]})"

    data = QueryScript(
        f"SELECT pack_id, prefix, value, sandre FROM {env.DATABASE_RAW}.analysis WHERE pack_id IN {query_tuple_pack} AND sandre IN {tuple(sandre_list)}").execute()
    for element in data:
        try:
            sandre = int(element[3])
        except ValueError:
            sandre = element[3]
        if result[pack_dict[element[0]]]:
            result[pack_dict[element[0]]][sandre] = element[1] + \
                str(element[2]) if element[1] else str(element[2])
        else:
            result[pack_dict[element[0]]] = {
                sandre: element[1] + str(element[2]) if element[1] else str(element[2])}

    for element in result:
        if result[element]:
            for sandre in sandre_list:
                if not sandre in result[element]:
                    try:
                        sandre = int(sandre)
                    except ValueError:
                        sandre = sandre
                    result[element][sandre] = "ND"

    return result
