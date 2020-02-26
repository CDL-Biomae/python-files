from tools import QueryScript
import env
from calcul.toxicity import *

def get_dict_pack_fusion(campaign=None):

    if campaign:
        output = QueryScript(
            f"SELECT DISTINCT pack.id, key_dates.measurepoint_fusion_id, pack.nature FROM {env.DATABASE_RAW}.pack JOIN {env.DATABASE_TREATED}.key_dates ON key_dates.measurepoint_id=pack.measurepoint_id JOIN {env.DATABASE_RAW}.measurepoint ON measurepoint.id=pack.measurepoint_id WHERE measurepoint.reference LIKE '{campaign}%' and key_dates.version={env.VERSION};"
        ).execute()
    else:
        output = QueryScript(
            f"  SELECT DISTINCT pack.id, key_dates.measurepoint_fusion_id, pack.nature FROM {env.DATABASE_RAW}.pack JOIN {env.DATABASE_TREATED}.key_dates ON key_dates.measurepoint_id=pack.measurepoint_id WHERE key_dates.version={env.VERSION};"
        ).execute()

    dict_pack_fusion = {}

    for row in output:
        [pack_id, mp, nature] = row

        try:
            dict_pack_fusion[mp][nature] = pack_id
        except KeyError:
            dict_pack_fusion[mp] = {}
            dict_pack_fusion[mp][nature] = pack_id

    return dict_pack_fusion

def run(cas):
    dict_pack_fusion = get_dict_pack_fusion()

    ### Alimentation
    # Survie 7 jours mâles: {mp_fusion: {'average': ..%, ...}}
    dict_survie_7j_males = survie_alim(dict_pack_fusion)

    # Alimentation: {mp_fusion: ..%}
    dict_alimentation = alimentation(dict_pack_fusion)

    ## Neurotoxicité
    # Neurotoxicité AChE: {mp_fusion: ..%}
    dict_neurotoxicity_AChE = neurotoxicity(dict_pack_fusion)

    ## Reproduction
    # Survie femelle: {mp_fusion: ..%}
    dict_survie_femelle = female_survivor(dict_pack_fusion)

    ## Reprotoxicité
    # Nombre jours exposition in situ: {mp_fusion: int, None or "NA"}
    dict_nombre_jours_exposition = number_days_exposition(dict_pack_fusion)

    ## Fecondité
    # Nombre de femelles concernees - fécondité
    dict_fecundity = fecundity(dict_pack_fusion)
    dict_nombre_femelles_concernees_fecondite = {mp_fusion: dict_fecundity[mp_fusion]['nbr_femelles_concernées'] for mp_fusion in dict_pack_fusion}
    dict_fecondite_moyenne = {mp_fusion: dict_fecundity[mp_fusion]['fécondité_moyenne'] for mp_fusion in dict_pack_fusion}
    dict_nombre_femelles_analysees = {mp_fusion: dict_fecundity[mp_fusion]['nbr_femelles_analysées'] for mp_fusion in dict_pack_fusion}

    ## Cycle de mue
    # vvv: {mp_fusion: {'cycle de mue': ..%, 'cycle de mue attendu': ..%, 'nb_femelles_retard': int}}
    dict_cycle_de_mue = molting_cycle(dict_pack_fusion)
    dict_cycle_de_mue_condense = {mp_fusion: '' for mp_fusion in dict_pack_fusion}
    for mp_fusion in dict_pack_fusion:
        cycle_observe = dict_cycle_de_mue[mp_fusion]['cycle de mue']
        cycle_attendu = dict_cycle_de_mue[mp_fusion]['cycle de mue attendu']
        cycle_str = f"{cycle_observe}% ({cycle_attendu}%)"
        dict_cycle_de_mue_condense[mp_fusion] = cycle_str

    ## Nombre de femelles en retard
    # dict_nombre_femelles_en_retard = {mp_fusion: nbr_femelles_en_retard}
    # dict_surface_des_retards = {pack_id: [oocyte_area_mm, ...]}
    dict_nombre_femelles_en_retard, dict_surface_des_retards = number_female_concerned_area(dict_pack_fusion)


    ## Perturbation endocrinienne
    dict_perturbation_endocrinienne = perturbation_endocrinienne(dict_pack_fusion, dict_nombre_femelles_en_retard, dict_surface_des_retards, dict_fecundity)

    ####################################################################################################################
        # CREATION VALUES #
    ####################################################################################################################

    values = []
    for mp_fusion in dict_pack_fusion:
        measurepoint_id_fusion = mp_fusion
        male_survival_7_days = dict_survie_7j_males[mp_fusion]
        alimentation = dict_alimentation[mp_fusion]
        neurotoxicity = dict_neurotoxicity_AChE[mp_fusion]
        female_survivor = dict_survie_femelle[mp_fusion]
        number_days_exposition = dict_nombre_jours_exposition[mp_fusion]
        number_female_concerned = dict_nombre_femelles_concernees_fecondite[mp_fusion]
        index_fertility_average = dict_fecondite_moyenne[mp_fusion]
        number_female_analysis = dict_nombre_femelles_analysees[mp_fusion]
        molting_cycle = dict_cycle_de_mue[mp_fusion]
        number_female_concerned_area = dict_nombre_femelles_en_retard[mp_fusion]
        endocrine_disruption = dict_perturbation_endocrinienne[mp_fusion]

        value = (measurepoint_id_fusion,
                 male_survival_7_days,
                 alimentation,
                 neurotoxicity,
                 female_survivor,
                 number_days_exposition,
                 number_female_concerned,
                 index_fertility_average,
                 number_female_analysis,
                 molting_cycle,
                 number_female_concerned_area,
                 endocrine_disruption)

        values.append(value)

    ####################################################################################################################
        # PARTIE BDD SQL #
    ####################################################################################################################

    ## On a 3 cas pour les requêtes SQL
    # Cas 1: 'première_version'
    # Cas 2: 'update_version'
    # Cas 3: 'nouvelle_version'

    ## Cas 1: Création et remplissage de la base de données
    if cas == 1:
        # Création d'un table vide s'il n'existe pas
        create_table = QueryScript(
            "CREATE TABLE IF NOT EXISTS toxtable (id INT AUTO_INCREMENT PRIMARY KEY, measurepoint_fusion_id INT, male_survival_7_days varchar(255), alimentation varchar(255), neurotoxicity varchar(255), female_survivor varchar(255), number_days_exposition varchar(255), number_female_concerned varchar(255),index_fertility_average varchar(255),number_female_analysis varchar(255),molting_cycle varchar(255), number_female_concerned_area varchar(255), endocrine_disruption varchar(255), version int);"
        ).execute()

        fill_table = QueryScript(
            "INSERT INTO toxtable (measurepoint_fusion_id, male_survival_7_days, alimentation, neurotoxicity, female_survivor, number_days_exposition, number_female_concerned, index_fertility_average, number_female_analysis, molting_cycle, number_female_concerned_area, endocrine_disruption, version) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s)"
        )
        fill_table.setRows(values)
        fill_table.executemany()

    ## Cas 2: Mise à jour de la dernière version connue
    if cas == 2:
