from docx import Document
from tools import QueryScript
from report import measure_points


def create_doc(campain):
    doc = Document('Page_de_garde.docx')
    style = doc.styles['Normal']
    font = style.font
    font.name = "Arial"
    return []


def recuperation_donnee(campaign):
    measurepoints_fusion_id_list = measure_points(campaign)
    return measurepoints_fusion_id_list

# %% Données exposure condition


def contexte(measurepoint_fusion_id):
    measurepoints = QueryScript(
        f"SELECT DISTINCT measurepoint_id FROM key_dates WHERE measurepoint_fusion_id = {measurepoint_fusion_id}").execute()

    if len(measurepoints) < 2:
        return data_exposure_condition_simple(measurepoint_fusion_id)
    else:
        return data_exposure_condition_fusion(measurepoints)


def data_exposure_condition_fusion(measurepoints):
    [id_mp_1, id_mp_2] = measurepoints
    dico = {}
    days = ["J+0", "J+7", "J+N", "J+21"]
    steps_barrel = [(50, "\'R0\'"), (50, "\'R0\'"),
                    (140, "\'RN\'"), (60, "\'R7\'")]

    for i in range(4):
        step, barrel = steps_barrel[i]
        dico_temp = {}
        if i in [0, 2]:
            measurepoint = id_mp_2
        else:
            measurepoint = id_mp_1

        output = QueryScript(
            f"SELECT recordedAt, temperature, conductivity, oxygen, ph FROM measureexposurecondition WHERE measurepoint_id = {measurepoint} and step = {step} and barrel = {barrel}").execute()
        output = output[0]
        if len(output) != 0:
            dico_temp["date"] = parser(output[0])
            dico_temp["temperature"] = output[1]
            dico_temp["conductivity"] = output[2]
            dico_temp["oxygen"] = output[3]
            dico_temp["ph"] = output[4]
        dico[days[i]] = dico_temp

    return dico


def data_exposure_condition_simple(measurepoint_id):
    dico = {}
    days = ["J+0", "J+7", "J+N", "J+21"]
    steps_barrel = [(50, "\'R0\'"), (60, "\'R7\'"),
                    (140, "\'RN\'"), (100, "\'R21\'")]

    for i in range(4):
        step, barrel = steps_barrel[i]
        dico_temp = {}
        output = QueryScript(
            f"SELECT recordedAt, temperature, conductivity, oxygen, ph FROM measureexposurecondition WHERE measurepoint_id = {measurepoint_id} and step = {step} and barrel = {barrel}").execute()
        if len(output) != 0:
            dico_temp["date"] = parser(output[0])
            dico_temp["temperature"] = output[1]
            dico_temp["conductivity"] = output[2]
            dico_temp["oxygen"] = output[3]
            dico_temp["ph"] = output[4]
    dico[days[i]] = dico_temp

    return dico


def parser(date):
    if date == None:
        return None
    year = date.year
    month = date.month
    day = date.day
    hour = date.hour
    minute = date.minute
    return f"{day}/{month}/{year} {hour}:{minute}"

# %% Données températures moyenne


# a changer parce que je fais measurepoint par measurepoint
def average_temperature(measurepoint_fusion_id):
    tempe = QueryScript(
        f"SELECT sensor3_average, sensor3_min, sensor3_max FROM average_temperature WHERE measurepoint_fusion_id = {measurepoint_fusion_id}").execute()
    tempe = tempe[0]
    dico = {'min': tempe[1], 'average': tempe[0], 'max': tempe[2]}
    return dico

# %% Récupération des données géographiques


# on entre le nom de la campagne, cela nous ressort les informations géographiques
def geographic_data_agency(campaign):
    query = QueryScript(
        f"SELECT substring(place.reference, -2,2), agency.code, agency.name, agency.zipcode, agency.city, agency.stream, agency.lambertX, agency.lambertY, agency.network, agency.hydroecoregion FROM agency JOIN place ON agency.id = place.agency_id JOIN campaign ON place.campaign_id = campaign.id WHERE campaign.reference = '{campaign}';")
    result = query.execute()
    return result


# a changer parce que je fais measurepoint par measurepoint
def geographic_data_measurepoint(measurepoint_id):
    query = QueryScript(
        f"SELECT latitudeSpotted, longitudeSpotted, lambertXSpotted, lambertYSpotted FROM biomae.measurepoint WHERE id={measurepoint_id}")
    return query.execute()
