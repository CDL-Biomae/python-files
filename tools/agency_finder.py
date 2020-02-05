from tools import QueryScript


def agency_finder(measurepoint_id):
    try:
        agency = QueryScript(f"SELECT code FROM agency JOIN place ON agency.id = place.agency_id JOIN measurepoint ON place.id = measurepoint.place_id WHERE measurepoint.id = {measurepoint_id};").execute()[0]
    except IndexError:
        agency = None

    return agency


def list_agency_finder(list_mp):
    list_agency = QueryScript(f"SELECT code FROM agency JOIN place ON agency.id = place.agency_id JOIN measurepoint ON place.id = measurepoint.place_id WHERE measurepoint.id IN {tuple(list_mp)};").execute()
    return list_agency
