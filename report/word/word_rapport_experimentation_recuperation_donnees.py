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
        dico_exposure_condition[data[0]] = data[1]
        dico_exposure_condition[data[0]]['fusion?'] = data[2]
        dico_type_biotest[data[0]] = {}
        dico_type_biotest[data[0]]['biotest'] = biotest
        if "chemistry" in biotest:
            scud_survivor = scud_survivor_chemistry(measurepoint)
            dico_type_biotest[data[0]]['survivor_chemistry'] = scud_survivor
    dico_avg_tempe, dico_geo_mp = average_temperature__geographic_data_measurepoint(
        measurepoints_fusion_id_list)
    dico_geo_agency = geographic_data_agency(campaign)
    return dico_exposure_condition, dico_avg_tempe, dico_geo_mp, dico_geo_agency, dico_type_biotest

# %% Données exposure condition


def data_exposure_condition(measurepoint_fusion_id):
    query = QueryScript(
        f"SELECT DISTINCT reference, measurepoint_id FROM key_dates JOIN measurepoint ON measurepoint.id = key_dates.measurepoint_fusion_id WHERE measurepoint_fusion_id = {measurepoint_fusion_id}").execute()
    measurepoints = [elt[1] for elt in query]
    if len(measurepoints) < 2:
        return query[0][0], data_exposure_condition_simple(measurepoint_fusion_id), False
    else:
        return query[0][0], data_exposure_condition_fusion(measurepoints), True


def data_exposure_condition_fusion(measurepoints):
    [id_mp_1, id_mp_2] = measurepoints
    if id_mp_1 < id_mp_2:
        id_mp_premier = id_mp_1
        id_mp_second = id_mp_2
    else:
        id_mp_premier = id_mp_2
        id_mp_second = id_mp_1
    dico = {}
    days = ["J+0", "J+14", "J+N", "J+21"]
    steps_barrel = [(50, "\'R0\'"), (50, "\'R0\'"),
                    (140, "\'RN\'"), (60, "\'R7\'")]

    for i in range(4):
        step, barrel = steps_barrel[i]
        if i in [0, 2]:
            measurepoint = id_mp_premier
        else:
            measurepoint = id_mp_second

        output = QueryScript(
            f"SELECT recordedAt, temperature, conductivity, oxygen, ph, type, comment FROM measureexposurecondition WHERE measurepoint_id = {measurepoint} and step = {step} and barrel = {barrel}").execute()
        if len(output) != 0:
            output = output[0]
            dico_temp = {'date': parser(output[0]), 'temperature': output[1],
                         'conductivity': output[2], 'oxygen': output[3], 'ph': output[4], 'type': output[5], 'comment': output[6]}
        else:
            dico_temp = {'date': None, 'temperature': None,
                         'conductivity': None, 'oxygen': None, 'ph': None, 'type': None, 'comment': None}
        dico[days[i]] = dico_temp

    return dico


def data_exposure_condition_simple(measurepoint_id):
    dico = {}
    days = ["J+0", "J+7", "J+N", "J+21"]
    steps_barrel = [(50, "\'R0\'"), (60, "\'R7\'"),
                    (140, "\'RN\'"), (100, "\'R21\'")]
    for i in range(4):
        step, barrel = steps_barrel[i]
        output = QueryScript(
            f"SELECT recordedAt, temperature, conductivity, oxygen, ph, type, comment FROM measureexposurecondition WHERE measurepoint_id = {measurepoint_id} and step = {step} and barrel = {barrel}").execute()
        if len(output) != 0:
            output = output[0]
            dico_temp = {'date': parser(output[0]), 'temperature': output[1],
                         'conductivity': output[2], 'oxygen': output[3], 'ph': output[4], 'type': output[5], 'comment': output[6]}
        else:
            dico_temp = {'date': None, 'temperature': None,
                         'conductivity': None, 'oxygen': None, 'ph': None, 'type': None, 'comment': None}
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
    if len(measurepoint_fusion_id_list) == 1:
        measurepoint_fusion_id_list = "(" + \
            measurepoint_fusion_id_list[0] + ")"
    else:
        measurepoint_fusion_id_list = tuple(measurepoint_fusion_id_list)
    dico_temperature = {}
    dico_geo_data = {}
    tempe = QueryScript(
        f"SELECT reference, sensor3_average, sensor3_min, sensor3_max, latitudeSpotted, longitudeSpotted, lambertXSpotted, lambertYSpotted FROM average_temperature JOIN measurepoint ON average_temperature.measurepoint_fusion_id = measurepoint.id WHERE average_temperature.measurepoint_fusion_id IN {measurepoint_fusion_id_list}").execute()
    for elt in tempe:
        dico_temp_temperature = {
            'min': elt[2], 'average': elt[1], 'max': elt[3]}
        dico_temp_geo = {'latitudeSpotted': f"{elt[4]}".replace(',', '.'),
                         'longitudeSpotted': f"{elt[5]}".replace(',', '.'), 'lambertXSpotted': f"{elt[6]}".replace(',', '.'), 'lambertYSpotted': f"{elt[7]}".replace(',', '.')}
        dico_temperature[elt[0]] = dico_temp_temperature
        dico_geo_data[elt[0]] = dico_temp_geo
    return dico_temperature, dico_geo_data

# %% Récupération des données géographiques de l'onglet agency


# on entre le nom de la campagne, cela nous ressort les informations géographiques
def geographic_data_agency(campaign):
    query = QueryScript(
        f"SELECT DISTINCT measurepoint.reference, agency.code, agency.name, agency.zipcode, agency.city, agency.stream, agency.lambertX, agency.lambertY, agency.network, agency.hydroecoregion FROM agency JOIN place ON agency.id=place.agency_id JOIN campaign ON place.campaign_id=campaign.id JOIN measurepoint ON measurepoint.place_id=place.id JOIN key_dates ON measurepoint.id=key_dates.measurepoint_fusion_id WHERE campaign.reference='{campaign}'").execute()
    dico = {}
    for elt in query:
        dico_temp = {'code': elt[1], 'name': elt[2], 'zipcode': elt[3], 'city': elt[4], 'stream': elt[5],
                     'lambertX': elt[6], 'lambertY': elt[7], 'network': elt[8], 'hydroecoregion': elt[9]}
        dico[elt[0]] = dico_temp
    return dico

# %% Récupération type de biotest


def type_biotest(measurepoint_fusion_id):
    query = QueryScript(
        f"SELECT DISTINCT pack.nature FROM pack JOIN key_dates ON pack.measurepoint_id = key_dates.measurepoint_id JOIN cage ON pack.id = cage.pack_id WHERE key_dates.measurepoint_fusion_id = {measurepoint_fusion_id}").execute()
    return query

# %% Récupération Survie Chimie


def scud_survivor_chemistry(measurepoint_fusion_id):
    query = QueryScript(
        f"SELECT Distinct cage.scud_survivor, pack.scud_quantity, pack.id FROM cage JOIN pack ON cage.pack_id = pack.id JOIN key_dates ON pack.measurepoint_id = key_dates.measurepoint_id WHERE pack.nature = 'chemistry' AND cage.scud_survivor IS not null AND key_dates.measurepoint_fusion_id = {measurepoint_fusion_id}").execute()
    total = 0
    for elt in query:
        total += elt[0]/elt[1]
    if len(query) == 0:
        average = 0
    else:
        average = total/len(query)*100
    return average
