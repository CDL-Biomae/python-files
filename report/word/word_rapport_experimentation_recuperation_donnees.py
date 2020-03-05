from tools import QueryScript, clean_dict, translate
from report import measure_points, list_of_list_to_dict
import env
import math
# %% Fonction principale pour tout appeler


def recuperation_donnee(campaign):
    '''Fonction principale appelant toutes les autres du fichier, pour regrouper la récupération de toutes les donnés
    Retourne plusieurs dictionnaires regroupant les différentes données, avec à chaque fois en clé la référence du point de mesure'''
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
    dico_geo_mp = geographic_data_measurepoint(measurepoints_fusion_id_list)
    dico_avg_tempe = average_temperature(measurepoints_fusion_id_list)
    dico_geo_agency = geographic_data_agency(campaign)
    clean_dict(dico_geo_mp)
    return dico_exposure_condition, dico_avg_tempe, dico_geo_mp, dico_geo_agency, dico_type_biotest

# %% Données exposure condition


def data_exposure_condition(measurepoint_fusion_id):
    '''Récupération des données de conditions d'exposition, calculée à partir d'un measurepoint (fusion), retourne la référence du point de mesure,
    le dictionnaire de données et si c'était une fusion ou non (ces informations sont restockées dans un autre dictionnaire dans recuperation_donnee) '''
    query = QueryScript(
        f"SELECT DISTINCT reference, measurepoint_id FROM {env.DATABASE_TREATED}.key_dates JOIN {env.DATABASE_RAW}.measurepoint ON measurepoint.id = key_dates.measurepoint_fusion_id WHERE measurepoint_fusion_id = {measurepoint_fusion_id} and version=  {env.CHOSEN_VERSION()}").execute()
    measurepoints = [elt[1] for elt in query]
    if len(measurepoints) < 2:
        return query[0][0], data_exposure_condition_simple(measurepoint_fusion_id), False
    else:
        return query[0][0], data_exposure_condition_fusion(measurepoints), True


def data_exposure_condition_fusion(measurepoints):
    ''' Récupération des données de conditions d'exposition dans le cas d'un measurepoint fusion, prend en entrée une liste avec les deux id des points de mesures
    et retourne un dictionnaire des données'''
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
            f"  SELECT recordedAt, temperature, conductivity, oxygen, ph, type, comment   FROM {env.DATABASE_RAW}.measureexposurecondition WHERE measurepoint_id = {measurepoint} and step = {step} and barrel = {barrel}").execute()
        if len(output) != 0:
            output = output[0]
            dico_temp = {'date': parser(output[0]), 'temperature': output[1],
                         'conductivity': output[2], 'oxygen': output[3], 'ph': output[4], 'type': output[5], 'comment': translate(output[6])}
        else:
            dico_temp = {'date': None, 'temperature': None,
                         'conductivity': None, 'oxygen': None, 'ph': None, 'type': None, 'comment': None}
        dico[days[i]] = dico_temp

    return dico


def data_exposure_condition_simple(measurepoint_id):
    ''' Récupération des données de conditions d'exposition dans le cas d'un measurepoint simple, prend en entrée un id de point de mesure
    et retourne un dictionnaire des données'''
    dico = {}
    days = ["J+0", "J+7", "J+N", "J+21"]
    steps_barrel = [(50, "\'R0\'"), (60, "\'R7\'"),
                    (140, "\'RN\'"), (100, "\'R21\'")]
    for i in range(4):
        step, barrel = steps_barrel[i]
        output = QueryScript(
            f"  SELECT recordedAt, temperature, conductivity, oxygen, ph, type, comment   FROM {env.DATABASE_RAW}.measureexposurecondition WHERE measurepoint_id = {measurepoint_id} and step = {step} and barrel = {barrel}").execute()
        if len(output) != 0:
            output = output[0]
            dico_temp = {'date': parser(output[0]), 'temperature': output[1],
                         'conductivity': output[2], 'oxygen': output[3], 'ph': output[4], 'type': output[5], 'comment': translate(output[6])}
        else:
            dico_temp = {'date': None, 'temperature': None,
                         'conductivity': None, 'oxygen': None, 'ph': None, 'type': None, 'comment': None}
        dico[days[i]] = dico_temp

    return dico


def parser(date):
    '''Permet d'écrire sous forme de string les dates au bon format, en gardant un 0 s'il n'y qu'un chiffre (pour les minutes, heures, jours et moi)
    Prend en entrée un datetime et retourne un string '''
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

# %% Données géographiques récupérées dans l'onglet measurepoint


def geographic_data_measurepoint(measurepoint_fusion_id_list):
    '''Prend en entrée la liste des id des points de mesures fusion dont l'on souhaite les données
    Retourne un dictionnaire contenant les données géographiques récupérées dans la table measurepoint, sous forme de dictionnaire de dictionnaire,
    avec comme première clé la référence du point de mesure, et en deuxième le type de donnée (longitude, latitude, lambert, etc)
    Les données sont déjà formatées comme elles doivent apparaitre dans le word (virgule comme séparateur de chiffre comme en français, caractère spéciaux corrigés) '''
    if len(measurepoint_fusion_id_list) == 1:
        measurepoint_fusion_id_list = "(" + \
            str(measurepoint_fusion_id_list[0]) + ")"
    else:
        measurepoint_fusion_id_list = tuple(measurepoint_fusion_id_list)
    dico_geo_data = {}

    tempe = QueryScript(
        f"SELECT reference, latitudeSpotted, longitudeSpotted, lambertXSpotted, lambertYSpotted, measurepoint.name, measurepoint.city, measurepoint.zipcode, measurepoint.stream, measurepoint.latitude, measurepoint.longitude FROM {env.DATABASE_TREATED}.average_temperature JOIN {env.DATABASE_RAW}.measurepoint ON average_temperature.measurepoint_fusion_id = measurepoint.id WHERE average_temperature.measurepoint_fusion_id IN {measurepoint_fusion_id_list} and average_temperature.version=  {env.CHOSEN_VERSION()}").execute()
    for elt in tempe:
        dico_temp_geo = {'latitudeSpotted': f"{elt[1]}".replace(',', '.'),
                         'longitudeSpotted': f"{elt[2]}".replace(',', '.'), 'lambertXSpotted': f"{elt[3]}".replace(',', '.'), 'lambertYSpotted': f"{elt[4]}".replace(',', '.'), 'name_mp': translate(elt[5]), 'city': translate(elt[6]), 'zipcode': translate(elt[7]), 'stream': translate(elt[8]), 'latitudeTh': elt[9], 'longitudeTh': elt[10]}
        dico_geo_data[elt[0]] = dico_temp_geo
    return dico_geo_data

# %% Données températures moyennes


def average_temperature(measurepoint_fusion_id_list):
    '''Prend en entrée la liste des id des points de mesures fusion que l'on souhaite
    Retourne un dictionnaire contenant les données de température (min, max, moyenne) de la table average_temperature, sous forme de dictionnaire de dictionnaire,
    avec comme première clé la référence du point de mesure, et en deuxième le type de donnée (min, max, average)
    Puisqu'il y a (potentiellement) trois sondes, on prend le minimum de tous les minimums (sachant que celui ci est déjà calculé), le maximum des maximum,
    et la température moyenne de la sonde qui est restée le plus longtemps
    Cette étape est longue, puisqu'il faut récupérer les données de dates correspondantes et trouver la période la plus longue '''
    if len(measurepoint_fusion_id_list) == 1:
        measurepoint_fusion_id_list = "(" + \
            str(measurepoint_fusion_id_list[0]) + ")"
    else:
        measurepoint_fusion_id_list = tuple(measurepoint_fusion_id_list)
    dico_avg_tempe_result = {}
    dico_avg_all_tempe = {}
    dico_date = {}  # {reference: [date1, date4, date6, date7]}
    tempe = QueryScript(
        f"SELECT reference, sensor1_min, sensor1_average, sensor1_max, sensor2_min, sensor2_average, sensor2_max, sensor3_min, sensor3_average, sensor3_max, average_temperature.measurepoint_fusion_id FROM {env.DATABASE_TREATED}.average_temperature JOIN {env.DATABASE_RAW}.measurepoint ON average_temperature.measurepoint_fusion_id = measurepoint.id WHERE average_temperature.measurepoint_fusion_id IN {measurepoint_fusion_id_list} AND average_temperature.version=  {env.CHOSEN_VERSION()}").execute()

    output_date1 = QueryScript(
        f"SELECT measurepoint_id, date FROM {env.DATABASE_TREATED}.key_dates WHERE date_id = 1 and measurepoint_fusion_id IN {measurepoint_fusion_id_list} AND key_dates.version=  {env.CHOSEN_VERSION()}"
    ).execute()
    output_date2 = QueryScript(
        f"SELECT measurepoint_id, date FROM {env.DATABASE_TREATED}.key_dates WHERE date_id = 2 and measurepoint_fusion_id IN {measurepoint_fusion_id_list} AND key_dates.version=  {env.CHOSEN_VERSION()}"
    ).execute()
    output_date4 = QueryScript(
        f"SELECT measurepoint_id, date FROM {env.DATABASE_TREATED}.key_dates WHERE date_id = 4 and measurepoint_fusion_id IN {measurepoint_fusion_id_list} AND key_dates.version=  {env.CHOSEN_VERSION()}"
    ).execute()
    output_date6 = QueryScript(
        f"SELECT measurepoint_id, date FROM {env.DATABASE_TREATED}.key_dates WHERE date_id = 6 and measurepoint_fusion_id IN {measurepoint_fusion_id_list} AND key_dates.version=  {env.CHOSEN_VERSION()}"
    ).execute()
    output_date7 = QueryScript(
        f"SELECT measurepoint_id, date FROM {env.DATABASE_TREATED}.key_dates WHERE date_id = 7 and measurepoint_fusion_id IN {measurepoint_fusion_id_list} AND key_dates.version=  {env.CHOSEN_VERSION()}"
    ).execute()

    dict_date1 = list_of_list_to_dict(output_date1)  # {mp: [date]}
    dict_date2 = list_of_list_to_dict(output_date2)
    dict_date4 = list_of_list_to_dict(output_date4)
    dict_date6 = list_of_list_to_dict(output_date6)
    dict_date7 = list_of_list_to_dict(output_date7)

    for elt in tempe:
        mp = elt[10]
        dico_temp_tempe = {'sensor1': {'min': elt[1], 'average': elt[2], 'max': elt[3]}, 'sensor2': {
            'min': elt[4], 'average': elt[5], 'max': elt[6]}, 'sensor3': {'min': elt[7], 'average': elt[8], 'max': elt[9]}}
        dico_avg_all_tempe[elt[0]] = dico_temp_tempe

        try:
            date1 = dict_date1[mp][0]
        except KeyError:
            date1 = None
        try:
            date2 = dict_date2[mp][0]
        except KeyError:
            date2 = None
        try:
            date4 = dict_date4[mp][0]
        except KeyError:
            date4 = None
        try:
            date6 = dict_date6[mp][0]
        except KeyError:
            date6 = None
        try:
            date7 = dict_date7[mp][0]
        except KeyError:
            date7 = None

        dico_date[elt[0]] = {'date_1': date1, 'date_2': date2,
                             'date_4': date4, 'date_6': date6, 'date_7': date7}

    dico_test = {}
    for key in dico_date.keys():
        dates = dico_date[key]
        begin_sensor1, end_sensor1, begin_sensor2, end_sensor2, begin_sensor3, end_sensor3 = dates[
            'date_1'], dates['date_2'], dates['date_6'], dates['date_4'], dates['date_6'], dates['date_7']

        if begin_sensor1 is None or end_sensor1 is None:
            delta_sensor1 = None
        else:
            delta_sensor1 = (end_sensor1 - begin_sensor1).days

        if begin_sensor2 is None or end_sensor2 is None:
            delta_sensor2 = None
        else:
            delta_sensor2 = (end_sensor2 - begin_sensor2).days

        if begin_sensor3 is None or end_sensor3 is None:
            delta_sensor3 = None
        else:
            delta_sensor3 = (end_sensor3 - begin_sensor3).days

        sensor_delta = [('sensor1', delta_sensor1), ('sensor2',
                                                     delta_sensor2), ('sensor3', delta_sensor3)]
        sensor_delta = [elt for elt in sensor_delta if elt[1] is not None]
        if len(sensor_delta) == 0:
            dico_test[key] = None
        (max_sensor, max_value) = (None, -math.inf)
        for elt in sensor_delta:
            if (elt[1] > max_value) & (dico_avg_all_tempe[key][elt[0]]['average'] is not None):
                (max_sensor, max_value) = elt
        dico_test[key] = max_sensor

    for key in dico_test.keys():
        if dico_test[key] is None:
            dico_avg_tempe_result[key] = {
                'min': None, 'average': None, 'max': None}
        else:
            liste_mini = []
            liste_maxi = []
            for sensor in ['sensor1', 'sensor2', 'sensor3']:
                mini = dico_avg_all_tempe[key][sensor]['min']
                maxi = dico_avg_all_tempe[key][sensor]['max']
                if mini is not None:
                    liste_mini.append(mini)
                if maxi is not None:
                    liste_maxi.append(maxi)
            temp = {'min': min(
                liste_mini), 'average': dico_avg_all_tempe[key][dico_test[key]]['average'], 'max': max(liste_maxi)}
            dico_avg_tempe_result[key] = temp
    return dico_avg_tempe_result


# %% Récupération des données géographiques de l'onglet agency


# on entre le nom de la campagne, cela nous ressort les informations géographiques
def geographic_data_agency(campaign):
    '''Prend en entrée la référence de campagne dont l'on souhaite les données
    Retourne un dictionnaire contenant les données géographiques récupérées dans la table agency, sous forme de dictionnaire de dictionnaire,
    avec comme première clé la référence du point de mesure, et en deuxième le type de donnée (longitude, latitude, lambert, etc)
    Les données sont déjà formatées comme elles doivent apparaitre dans le word (virgule comme séparateur de chiffre comme en français, caractère spéciaux corrigés) 
    Celles-ci ne sont utilisées que dans le cas d'une agence de l'eau'''
    query = QueryScript(
        f"  SELECT DISTINCT measurepoint.reference, agency.code, agency.name, agency.zipcode, agency.city, agency.stream, agency.lambertX, agency.lambertY, agency.network, agency.hydroecoregion, agency.latitude, agency.longitude FROM {env.DATABASE_RAW}.agency JOIN {env.DATABASE_RAW}.place ON agency.id=place.agency_id JOIN {env.DATABASE_RAW}.campaign ON place.campaign_id=campaign.id JOIN {env.DATABASE_RAW}.measurepoint ON measurepoint.place_id=place.id JOIN {env.DATABASE_TREATED}.key_dates ON measurepoint.id=key_dates.measurepoint_fusion_id WHERE campaign.reference='{campaign}' and key_dates.version=  {env.CHOSEN_VERSION()}").execute()
    dico = {}
    for elt in query:
        dico_temp = {'code': elt[1], 'name': translate(elt[2]), 'zipcode': translate(elt[3]), 'city': translate(elt[4]), 'stream': translate(elt[5]),
                     'lambertX': elt[6], 'lambertY': elt[7], 'network': translate(elt[8]), 'hydroecoregion': translate(elt[9]), 'latitudeTh': elt[10], 'longitudeTh': elt[11]}
        dico[elt[0]] = dico_temp
    return dico

# %% Récupération type de biotest


def type_biotest(measurepoint_fusion_id):
    '''Prend en argument un id de measurepoint fusion
    Retourne la liste des biotests en anglais (nom de la base de données) sous forme de liste'''
    query = QueryScript(
        f"  SELECT DISTINCT pack.nature FROM {env.DATABASE_RAW}.pack JOIN {env.DATABASE_TREATED}.key_dates ON pack.measurepoint_id = key_dates.measurepoint_id JOIN {env.DATABASE_RAW}.cage ON pack.id = cage.pack_id WHERE key_dates.version=  {env.CHOSEN_VERSION()} AND key_dates.measurepoint_fusion_id = {measurepoint_fusion_id}").execute()
    return query

# %% Récupération Survie Chimie


def scud_survivor_chemistry(measurepoint_fusion_id):
    '''Prend en argument un id de measurepoint fusion
    Retourne la valeur de la moyenne de la survie des gamares pour la chimie '''
    query = QueryScript(
        f"SELECT Distinct cage.scud_survivor, pack.scud_quantity, cage.id FROM {env.DATABASE_RAW}.cage JOIN {env.DATABASE_RAW}.pack ON cage.pack_id = pack.id JOIN {env.DATABASE_TREATED}.key_dates ON pack.measurepoint_id = key_dates.measurepoint_id WHERE key_dates.version=  {env.CHOSEN_VERSION()} AND pack.nature = 'chemistry' AND cage.scud_survivor IS not null AND key_dates.measurepoint_fusion_id = {measurepoint_fusion_id}").execute()
    total = 0
    for elt in query:
        total += elt[0]/elt[1]
    if len(query) == 0:
        average = 0
    else:
        average = total/len(query)*100
    return average
