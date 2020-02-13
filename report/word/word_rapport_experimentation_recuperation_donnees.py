from tools import QueryScript
from report import measure_points

# %% Fonction principale pour tout appeler


def recuperation_donnee(campaign):
    measurepoints_fusion_id_list = measure_points(campaign)
    dico_exposure_condition = {}
    dico_type_biotest = {}
    for measurepoint in measurepoints_fusion_id_list:
        data = data_exposure_condition(measurepoint)
        biotest = type_biotest(measurepoint)
        dico_exposure_condition[int(data[0])] = data[1]
        dico_type_biotest[int(data[0])] = biotest
    dico_avg_tempe, dico_geo_mp = average_temperature__geographic_data_measurepoint(
        measurepoints_fusion_id_list)
    dico_geo_agency = geographic_data_agency(campaign)
    return dico_exposure_condition, dico_avg_tempe, dico_geo_mp, dico_geo_agency, dico_type_biotest

# %% Données exposure condition


def data_exposure_condition(measurepoint_fusion_id):
    query = QueryScript(
        f"SELECT DISTINCT substring(reference, -5,2), measurepoint_id FROM key_dates JOIN measurepoint ON measurepoint.id = key_dates.measurepoint_fusion_id WHERE measurepoint_fusion_id = {measurepoint_fusion_id}").execute()
    measurepoints = [elt[1] for elt in query]
    if len(measurepoints) < 2:
        return query[0][0], data_exposure_condition_simple(measurepoint_fusion_id)
    else:
        return query[0][0], data_exposure_condition_fusion(measurepoints)


def data_exposure_condition_fusion(measurepoints):
    [id_mp_1, id_mp_2] = measurepoints
    dico = {}
    days = ["J+0", "J+14", "J+N", "J+21"]
    steps_barrel = [(50, "\'R0\'"), (50, "\'R0\'"),
                    (140, "\'RN\'"), (60, "\'R7\'")]

    for i in range(4):
        step, barrel = steps_barrel[i]
        if i in [0, 2]:
            measurepoint = id_mp_2
        else:
            measurepoint = id_mp_1

        output = QueryScript(
            f"SELECT recordedAt, temperature, conductivity, oxygen, ph, type FROM measureexposurecondition WHERE measurepoint_id = {measurepoint} and step = {step} and barrel = {barrel}").execute()
        if len(output) != 0:
            output = output[0]
            dico_temp = {'date': parser(output[0]), 'temperature': output[1],
                         'conductivity': output[2], 'oxygen': output[3], 'ph': output[4], 'type': output[5]}
        else:
            dico_temp = {'date': None, 'temperature': None,
                         'conductivity': None, 'oxygen': None, 'ph': None, 'type': None}
        dico[days[i]] = dico_temp

    return dico


def data_exposure_condition_simple(measurepoint_id):
    dico = {}
    days = ["J+0", "J+14", "J+N", "J+21"]
    steps_barrel = [(50, "\'R0\'"), (60, "\'R7\'"),
                    (140, "\'RN\'"), (100, "\'R21\'")]
    for i in range(4):
        step, barrel = steps_barrel[i]
        output = QueryScript(
            f"SELECT recordedAt, temperature, conductivity, oxygen, ph, type FROM measureexposurecondition WHERE measurepoint_id = {measurepoint_id} and step = {step} and barrel = {barrel}").execute()
        if len(output) != 0:
            output = output[0]
            dico_temp = {'date': parser(output[0]), 'temperature': output[1],
                         'conductivity': output[2], 'oxygen': output[3], 'ph': output[4], 'type': output[5]}
        else:
            dico_temp = {'date': None, 'temperature': None,
                         'conductivity': None, 'oxygen': None, 'ph': None, 'type': None}
        dico[days[i]] = dico_temp

    return dico


def parser(date):
    if date == None:
        return None
    year = date.year
    month = date.month
    if month < 10:
        month = "0"+str(month)
    day = date.day
    if day < 10:
        day = "0"+str(day)
    hour = date.hour
    if hour < 10:
        hour = "0"+str(hour)
    minute = date.minute
    if minute < 10:
        minute = "0"+str(minute)
    return f"{day}/{month}/{year} {hour}:{minute}"

# %% Données températures moyenne et données géographiques récupérées dans l'onglet measurepoint


def average_temperature__geographic_data_measurepoint(measurepoint_fusion_id_list):
    measurepoint_fusion_id_list = tuple(measurepoint_fusion_id_list)
    dico_temperature = {}
    dico_geo_data = {}
    tempe = QueryScript(
        f"SELECT substring(reference, -5,2), sensor3_average, sensor3_min, sensor3_max, latitudeSpotted, longitudeSpotted, lambertXSpotted, lambertYSpotted FROM average_temperature JOIN measurepoint ON average_temperature.measurepoint_fusion_id = measurepoint.id WHERE average_temperature.measurepoint_fusion_id IN {measurepoint_fusion_id_list}").execute()
    for elt in tempe:
        dico_temp_temperature = {
            'min': elt[2], 'average': elt[1], 'max': elt[3]}
        dico_temp_geo = {'latitudeSpotted': elt[4],
                         'longitudeSpotted': elt[5], 'lambertXSpotted': elt[6], 'lambertYSpotted': elt[7]}
        dico_temperature[int(elt[0])] = dico_temp_temperature
        dico_geo_data[int(elt[0])] = dico_temp_geo
    return dico_temperature, dico_geo_data

# %% Récupération des données géographiques de l'onglet agency


# on entre le nom de la campagne, cela nous ressort les informations géographiques
def geographic_data_agency(campaign):
    query = QueryScript(
        f"SELECT substring(place.reference, -2,2), agency.code, agency.name, agency.zipcode, agency.city, agency.stream, agency.lambertX, agency.lambertY, agency.network, agency.hydroecoregion FROM agency JOIN place ON agency.id = place.agency_id JOIN campaign ON place.campaign_id = campaign.id WHERE campaign.reference = '{campaign}';").execute()
    # query = QueryScript(
    #     f"SELECT DISTINCT measurepoint.reference, agency.code, agency.name, agency.zipcode, agency.city, agency.stream, agency.lambertX, agency.lambertY, agency.network, agency.hydroecoregion FROM agency JOIN place ON agency.id=place.agency_id JOIN campaign ON place.campaign_id=campaign.id JOIN measurepoint ON measurepoint.place_id=place.id JOIN key_dates ON measurepoint.id=key_dates.measurepoint_fusion_id WHERE campaign.reference='{campaign}'")
    dico = {}
    for elt in query:
        dico_temp = {'code': elt[1], 'name': elt[2], 'zipcode': elt[3], 'city': elt[4], 'stream': elt[5],
                     'lambertX': elt[6], 'lambertY': elt[7], 'network': elt[8], 'hydroecoregion': elt[9]}
        dico[int(elt[0])] = dico_temp
    return dico

# %% Récupération type de biotest


def type_biotest(measurepoint_fusion_id):
    query = QueryScript(
        f"SELECT DISTINCT pack.nature FROM pack JOIN key_dates ON pack.measurepoint_id = key_dates.measurepoint_id WHERE key_dates.measurepoint_fusion_id = {measurepoint_fusion_id}").execute()
    return query
