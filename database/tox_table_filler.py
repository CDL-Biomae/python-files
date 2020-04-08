from tools import QueryScript
import env
from calcul.toxicity import Alimentation, Neurotoxicity, Reprotoxicity, Reproduction


def get_dict_pack():
    """
    Permet de récupérer l'ensemble des pack_id pour tout les points de mesures de la base de donnée
    :param campaign:
    :return dict_pack: {mp: {'nature': pack_id, ...}, ...}
    """
    output = QueryScript(
        f"SELECT DISTINCT Pack.id, Measurepoint.id, Pack.nature FROM {env.DATABASE_RAW}.Pack JOIN {env.DATABASE_RAW}.Measurepoint ON Measurepoint.id=Pack.measurepoint_id"
    ).execute()

    dict_pack = {}

    for row in output:
        [pack_id, mp, nature] = row

        try:
            dict_pack[mp][nature] = pack_id
        except KeyError:
            dict_pack[mp] = {}
            dict_pack[mp][nature] = pack_id

    return dict_pack


def run(cas):

    print("--> toxtable")
    dict_pack = get_dict_pack()

    ### Alimentation
    # Survie 7 jours mâles: {mp: {'average': ..%, ...}}
    dict_survie_7j_males = Alimentation.survie_alim(dict_pack)
    dict_survie_7j_males_average = {mp: None for mp in dict_pack}
    for mp in dict_pack:
        try:
            average = dict_survie_7j_males[mp]["average"]
        except (TypeError, KeyError):
            pass
        else:
            dict_survie_7j_males_average[mp] = average

    # Alimentation: {mp: ..%}
    dict_alimentation = Alimentation.alimentation(dict_pack)

    # Neurotoxicité
    # Neurotoxicité AChE: {mp: ..%}
    dict_neurotoxicity_AChE = Neurotoxicity.neurotoxicity(dict_pack)

    ## Reproduction
    # Survie femelle: {mp: ..%}
    dict_survie_femelle = Reproduction.female_survivor(dict_pack)

    ## Reprotoxicité
    # Nombre jours exposition in situ: {mp: int, None or "NA"}
    dict_nombre_jours_exposition = Reprotoxicity.number_days_exposition(dict_pack)

    ## Fecondité
    # Nombre de femelles concernees - fécondité
    dict_fecundity = Reprotoxicity.fecundity(dict_pack)
    dict_nombre_femelles_concernees_fecondite = {
        mp: dict_fecundity[mp]["nbr_femelles_concernées"] for mp in dict_pack
    }
    dict_fecondite_moyenne = {
        mp: dict_fecundity[mp]["fécondité_moyenne"] for mp in dict_pack
    }
    dict_nombre_femelles_analysees = {
        mp: dict_fecundity[mp]["nbr_femelles_analysées"] for mp in dict_pack
    }

    # Transformation de "indice de fecondité - moyenne" en "%Inhibition fecondité - Résultat attendu"
    ref_calcul = QueryScript(
        f"SELECT value FROM {env.DATABASE_TREATED}.r2_constant WHERE name = 'indice de fertilité attendu - moyenne' AND version = {env.LATEST_VERSION()};"
    ).execute()[0]
    dict_percent_inhibition_fecondite = {}
    for mp in dict_fecondite_moyenne:
        value = dict_fecondite_moyenne[mp]
        if isinstance(value, float):
            percent_inhibition = -100 * (ref_calcul - value) / ref_calcul
            dict_percent_inhibition_fecondite[mp] = percent_inhibition
        else:
            dict_percent_inhibition_fecondite[mp] = value

    ## Cycle de mue
    # vvv: {mp: {'cycle de mue': ..%, 'cycle de mue attendu': ..%, 'nb_femelles_retard': int}}
    dict_cycle_de_mue = Reprotoxicity.molting_cycle(dict_pack)
    dict_cycle_de_mue_condense = {mp: "" for mp in dict_pack}
    for mp in dict_pack:
        cycle_observe = dict_cycle_de_mue[mp]["cycle de mue"]
        cycle_attendu = dict_cycle_de_mue[mp]["cycle de mue attendu"]
        cycle_str = f"{cycle_observe}% ({cycle_attendu}%)"
        dict_cycle_de_mue_condense[mp] = cycle_str

    ## Nombre de femelles en retard
    # dict_nombre_femelles_en_retard = {mp: nbr_femelles_en_retard}
    # dict_surface_des_retards = {pack_id: [oocyte_area_mm, ...]}
    (
        dict_nombre_femelles_en_retard,
        dict_surface_des_retards,
    ) = Reprotoxicity.number_female_concerned_area(dict_pack)

    ## Perturbation endocrinienne
    dict_perturbation_endocrinienne = Reprotoxicity.perturbation_endocrinienne(
        dict_pack,
        dict_nombre_femelles_en_retard,
        dict_surface_des_retards,
        dict_fecundity,
    )

    ####################################################################################################################
    # CREATION VALUES #
    ####################################################################################################################
    k = 0
    values = []
    for mp in dict_pack:
        measurepoint_id = mp
        male_survival_7_days = dict_survie_7j_males_average[mp]
        alimentation = dict_alimentation[mp]
        neurotoxicity = dict_neurotoxicity_AChE[mp]
        female_survivor = dict_survie_femelle[mp]
        number_days_exposition = dict_nombre_jours_exposition[mp]
        number_female_concerned = dict_nombre_femelles_concernees_fecondite[mp]
        percent_inhibition_fecondite = dict_percent_inhibition_fecondite[mp]
        number_female_analysis = dict_nombre_femelles_analysees[mp]
        molting_cycle = dict_cycle_de_mue_condense[mp]
        number_female_concerned_area = dict_nombre_femelles_en_retard[mp]
        endocrine_disruption = dict_perturbation_endocrinienne[mp]

        value = (
            measurepoint_id,
            male_survival_7_days,
            alimentation,
            neurotoxicity,
            female_survivor,
            number_days_exposition,
            number_female_concerned,
            percent_inhibition_fecondite,
            number_female_analysis,
            molting_cycle,
            number_female_concerned_area,
            endocrine_disruption,
        )

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
        # Création d'un table vide si elle n'existe pas
        QueryScript(f'DROP TABLE IF EXISTS {env.DATABASE_TREATED}.toxtable').execute(admin=True)
        create_table = QueryScript(
            f"CREATE TABLE IF NOT EXISTS {env.DATABASE_TREATED}.toxtable (id INT AUTO_INCREMENT PRIMARY KEY, measurepoint_id INT, male_survival_7_days varchar(255), alimentation varchar(255), neurotoxicity varchar(255), female_survivor varchar(255), number_days_exposition varchar(255), number_female_concerned varchar(255),percent_inhibition_fecondite varchar(255),number_female_analysis varchar(255),molting_cycle varchar(255), number_female_concerned_area varchar(255), endocrine_disruption varchar(255), version int);"
        ).execute(admin=True)

        fill_table = QueryScript(
            f"INSERT INTO {env.DATABASE_TREATED}.toxtable (measurepoint_id, male_survival_7_days, alimentation, neurotoxicity, female_survivor, number_days_exposition, number_female_concerned, percent_inhibition_fecondite, number_female_analysis, molting_cycle, number_female_concerned_area, endocrine_disruption, version) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s)"
        )
        fill_table.setRows(values)
        fill_table.executemany()

    ## Cas 2: Mise à jour de la dernière version connue
    if cas == 2:
        QueryScript(f"DELETE FROM {env.DATABASE_TREATED}.toxtable WHERE version = {env.LATEST_VERSION()};").execute(admin=True)
        fill_table = QueryScript(
            f"INSERT INTO {env.DATABASE_TREATED}.toxtable (measurepoint_id, male_survival_7_days, alimentation, neurotoxicity, female_survivor, number_days_exposition, number_female_concerned, percent_inhibition_fecondite, number_female_analysis, molting_cycle, number_female_concerned_area, endocrine_disruption, version) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s)"
        )
        fill_table.setRows(values)
        fill_table.executemany()

    ## Cas 3: Ajout d'une nouvelle version
    if cas == 3:
        fill_table = QueryScript(
            f"INSERT INTO {env.DATABASE_TREATED}.toxtable (measurepoint_id, male_survival_7_days, alimentation, neurotoxicity, female_survivor, number_days_exposition, number_female_concerned, percent_inhibition_fecondite, number_female_analysis, molting_cycle, number_female_concerned_area, endocrine_disruption, version) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s)"
        )
        fill_table.setRows(values)
        fill_table.executemany()

    print("--> toxtable ready")
