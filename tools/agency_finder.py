from tools import QueryScript


def agency_finder(measurepoint_id):
    try:
        agency = QueryScript(
            f"SELECT code FROM agency JOIN place ON agency.id = place.agency_id JOIN measurepoint ON place.id = measurepoint.place_id WHERE measurepoint.id = {measurepoint_id};"
        ).execute()[0]
    except IndexError:
        agency = None

    return agency


def list_agency_finder(list_mp):
    output = QueryScript(
        f"SELECT measurepoint.id, code FROM agency JOIN place ON agency.id = place.agency_id JOIN measurepoint ON place.id = measurepoint.place_id WHERE measurepoint.id IN {tuple(list_mp)};"
    ).execute()
    print(output)
    if len(output) == len(list_mp):
        list_agency = [x[1] for x in output]
        return list_agency

    else:
        list_agency = []
        list_mp_output = [x[0] for x in output]
        for mp_id in list_mp:
            try:
                idx_code = list_mp_output.index(mp_id)
                list_agency.append(output[idx_code][1])
            except ValueError:
                list_agency.append(None)

        print(list_agency)
        return list_agency
