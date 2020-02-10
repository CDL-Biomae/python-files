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
        return output


    ################# list_mp et output ne sont pas ordonnés de la même manière donc decorrelation entrée et sortie........

    else:
        compteur = 0
        list_agency = []
        for mp_id in list_mp:
            print(mp_id)
            [mp_output, code] = output[compteur]
            if mp_id == mp_output:
                print(f'Test ok for {mp_id} and {mp_output}')
                list_agency.append(code)
                compteur += 1
            else:
                list_agency.append(None)
                print(f'No agency code for {mp_id}, none written')

        print(list_agency)
        return list_agency
