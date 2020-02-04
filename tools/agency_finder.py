from tools import QueryScript

def agency_finder(measurepoint_id) :
    try:
        agency = QueryScript(f"SELECT code FROM agency WHERE id IN (SELECT agency_id FROM place WHERE id IN (SELECT place_id FROM measurepoint WHERE id = {measurepoint_id}))").execute()[0]
    except IndexError:
        agency = None

    return agency
