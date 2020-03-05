from tools import QueryScript
import env

def agency_finder(measurepoint_id):
    '''
    Permet de récupérer le code agence associé à un point de mesure
    :param measurepoint_id:
    :return: code_agence:
    '''
    try:
        agency = QueryScript(
            f"  SELECT code   FROM {env.DATABASE_RAW}.agency JOIN {env.DATABASE_RAW}.place ON agency.id = place.agency_id JOIN {env.DATABASE_RAW}.measurepoint ON place.id = measurepoint.place_id WHERE measurepoint.id = {measurepoint_id};"
        ).execute()[0]
    except IndexError:
        agency = None

    return agency


def list_agency_finder(list_mp):
    '''
    Permet de récupérer les codes agences associés à une liste de points de mesure
    :param list_mp: liste d'id de points de mesure
    :return: list_agency: liste de codes agences
    '''
    if len(list_mp) > 1:
        query_tuple_mp = tuple(list_mp)
    else:
        query_tuple_mp = f"({list_mp[0]})"
    output = QueryScript(
        f"  SELECT measurepoint.id, code   FROM {env.DATABASE_RAW}.agency JOIN {env.DATABASE_RAW}.place ON agency.id = place.agency_id JOIN {env.DATABASE_RAW}.measurepoint ON place.id = measurepoint.place_id WHERE measurepoint.id IN {query_tuple_mp};"
    ).execute()
    list_agency = []
    list_mp_output = [x[0] for x in output]
    for mp_id in list_mp:
        try:
            idx_code = list_mp_output.index(mp_id)
            list_agency.append(output[idx_code][1])
        except ValueError:
            list_agency.append(None)
    return list_agency
