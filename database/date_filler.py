'''
Il y a 2 scripts dans ce fichier:
--> create_empty_date_table(): vide la table key_dates si elle existe, ou la crée si elle n'existe pas
--> fill_date_table(): remplie la table key_dates avec 7 dates clées par point de mesure

Les 7 dates clées sont détaillées dans le fichier reference_date_filler.py

/!\ C'est quoi une fusion?
--> Dans certains cas on regroupe 2 points de mesure sous un seul point de mesure. C'est le cas si la 'place' est de
type 'point_monitoring', qu'il y a exactement 2 points à cette 'place' et que les expériences associées à ces points
sont compatibles (pas 2 expériences du même type)
--> Exemple: Il y a de la fusion pour la campagne 'AG-003-01'

'''



#%% ## IMPORT ##
from tools import QueryScript
import env
#%% ## TOOLS ##


def create_empty_date_table():
    key_dates_table = QueryScript(
        f"DROP TABLE IF EXISTS key_dates; CREATE TABLE key_dates (id INT AUTO_INCREMENT PRIMARY KEY, measurepoint_id INT, date_id INT, date DATETIME, measurepoint_fusion_id INT, version INT);")
    key_dates_table.execute(True)
    print('Une table key_dates vide a été créée')


def key_dates(id_mp):
    exposureconditions = QueryScript(
        script=f'  SELECT step, recordedAt, barrel   FROM {env.DATABASE_RAW}.measureexposurecondition WHERE measurepoint_id=' + str(
            id_mp)).execute()
    natures = QueryScript(
        f"  SELECT nature   FROM {env.DATABASE_RAW}.pack WHERE measurepoint_id = {id_mp}").execute()
    steps_barrels = [(x[0], x[2]) for x in exposureconditions]

    # Dictionnaire de dates cles à remplir
    key_dates_list = {}

    # (step 50, R0) Transplantation Alimentation
    try:
        idx = steps_barrels.index((50, 'R0'))
        temp_date = exposureconditions[idx][1]
    except ValueError:
        temp_date = None

    key_dates_list['Transplantation Alimentation'] = {
        'date': temp_date, 'step': 50, 'barrel': 'R0'}

    # (step 60, R7) Recuperation Alimentation
    try:
        idx = steps_barrels.index((60, 'R7'))
        temp_date = exposureconditions[idx][1]
    except ValueError:
        temp_date = None

    key_dates_list['Recuperation Alimentation'] = {
        'date': temp_date, 'step': 60, 'barrel': 'R7'}

    # (step 20) Lancement Alimentation
    try:
        idx = steps_barrels.index((20, None))
        temp_date = exposureconditions[idx][1]
    except ValueError:
        temp_date = None

    key_dates_list['Lancement Alimentation'] = {
        'date': temp_date, 'step': 20, 'barrel': None}

    # (step 140, RN) Recuperation Reprotoxicité
    try:
        idx = steps_barrels.index((140, 'RN'))
        temp_date = exposureconditions[idx][1]
    except ValueError:
        temp_date = None

    key_dates_list['Recuperation Reprotoxicite'] = {
        'date': temp_date, 'step': 140, 'barrel': 'RN'}

    # (step 170) Arrêt Reprotoxicité
    try:
        idx = steps_barrels.index((170, None))
        temp_date = exposureconditions[idx][1]
    except ValueError:
        temp_date = None

    key_dates_list['Arret Reprotoxicite'] = {
        'date': temp_date, 'step': 170, 'barrel': None}

    # (step 50, R0) Lancement Chimie (=Lancement reprotoxicité)
    try:
        idx = steps_barrels.index((50, 'R0'))
        temp_date = exposureconditions[idx][1]
    except ValueError:
        temp_date = None

    key_dates_list['Lancement Chimie'] = {
        'date': temp_date, 'step': 50, 'barrel': 'R0'}

    # (step 100, R21) Récupération Chimie
    try:
        idx = steps_barrels.index((100, 'R21'))
        temp_date = exposureconditions[idx][1]
    except ValueError:
        if 'chemistry' in natures:
            try:
                idx = steps_barrels.index((60, 'R7'))
                temp_date = exposureconditions[idx][1]
            except ValueError:
                try:
                    idx = steps_barrels.index((140, 'RN'))
                    temp_date = exposureconditions[idx][1]
                except ValueError:
                    temp_date = None
        else:
            temp_date = None

    key_dates_list['Recuperation Chimie'] = {
        'date': temp_date, 'step': 100, 'barrel': 'R21'}

    return key_dates_list


def key_datesFusion(id_mp_alim, id_mp_chimie, id_mp_repro):
    if id_mp_alim != None:
        exposureconditions_alim = QueryScript(
            script=f'  SELECT step, recordedAt, barrel   FROM {env.DATABASE_RAW}.measureexposurecondition WHERE measurepoint_id=' + str(id_mp_alim)).execute()
    else:
        exposureconditions_alim = []

    if id_mp_chimie != None:
        exposureconditions_chimie = QueryScript(
            script=f'  SELECT step, recordedAt, barrel   FROM {env.DATABASE_RAW}.measureexposurecondition WHERE measurepoint_id=' + str(id_mp_chimie)).execute()
    else:
        exposureconditions_chimie = []

    if id_mp_repro != None:
        exposureconditions_repro = QueryScript(
            script=f'  SELECT step, recordedAt, barrel   FROM {env.DATABASE_RAW}.measureexposurecondition WHERE measurepoint_id=' + str(id_mp_repro)).execute()
    else:
        exposureconditions_repro = []

    steps_barrels_alim = [(x[0], x[2]) for x in exposureconditions_alim] if len(
        exposureconditions_alim) else []
    steps_barrels_chimie = [(x[0], x[2]) for x in exposureconditions_chimie] if len(
        exposureconditions_chimie) else []
    steps_barrels_repro = [(x[0], x[2]) for x in exposureconditions_repro] if len(
        exposureconditions_repro) else []

    # Dictionnaire de dates cles à remplir
    key_dates_list = {}

    # (step 50, R0) Transplantation Alimentation
    try:
        idx = steps_barrels_alim.index((50, 'R0'))
        temp_date = exposureconditions_alim[idx][1]
    except ValueError:
        temp_date = None

    key_dates_list['Transplantation Alimentation'] = {
        'date': temp_date, 'step': 50, 'barrel': 'R0'}

    # (step 60, R7) Recuperation Alimentation
    try:
        idx = steps_barrels_alim.index((60, 'R7'))
        temp_date = exposureconditions_alim[idx][1]
    except ValueError:
        temp_date = None

    key_dates_list['Recuperation Alimentation'] = {
        'date': temp_date, 'step': 60, 'barrel': 'R7'}

    # (step 20) Lancement Alimentation
    try:
        idx = steps_barrels_alim.index((20, None))
        temp_date = exposureconditions_alim[idx][1]
    except ValueError:
        temp_date = None

    key_dates_list['Lancement Alimentation'] = {
        'date': temp_date, 'step': 20, 'barrel': None}

    # (step 140, RN) Recuperation Reprotoxicité
    try:
        idx = steps_barrels_repro.index((140, 'RN'))
        temp_date = exposureconditions_repro[idx][1]
    except ValueError:
        temp_date = None

    key_dates_list['Recuperation Reprotoxicite'] = {
        'date': temp_date, 'step': 140, 'barrel': 'RN'}

    # (step 170) Arrêt Reprotoxicité
    try:
        idx = steps_barrels_repro.index((170, None))
        temp_date = exposureconditions_repro[idx][1]
    except ValueError:
        temp_date = None

    key_dates_list['Arret Reprotoxicite'] = {
        'date': temp_date, 'step': 170, 'barrel': None}

    # (step 50, C0 ou T0) Lancement Chimie (=Lancement reprotoxicité)
    try:
        idx = steps_barrels_chimie.index((50, 'R0'))
        temp_date = exposureconditions_chimie[idx][1]
    except ValueError:
        temp_date = None

    key_dates_list['Lancement Chimie'] = {
        'date': temp_date, 'step': 50, 'barrel': 'R0'}

    # (step 100, R21) Récupération Chimie
    try:
        idx = steps_barrels_chimie.index((100, 'R21'))
        temp_date = exposureconditions_chimie[idx][1]
    except ValueError:
        try:
            idx = steps_barrels_chimie.index((60, 'R7'))
            temp_date = exposureconditions_chimie[idx][1]
        except ValueError:
            try:
                idx = steps_barrels_chimie.index((140, 'RN'))
                temp_date = exposureconditions_chimie[idx][1]
            except ValueError:
                temp_date = None

    key_dates_list['Recuperation Chimie'] = {
        'date': temp_date, 'step': 100, 'barrel': 'R21'}

    # Trouver id_mp_fusion
    debuts = {}

    try:
        idx_alim = steps_barrels_alim.index((20, None))
        debuts[id_mp_alim] = exposureconditions_alim[idx_alim][1]
    except ValueError:
        debuts[id_mp_alim] = None

    try:
        idx_repro = steps_barrels_repro.index((20, None))
        debuts[id_mp_repro] = steps_barrels_repro[idx_repro][1]
    except ValueError:
        debuts[id_mp_repro] = None

    try:
        idx_chimie = steps_barrels_chimie.index((20, None))
        debuts[id_mp_chimie] = exposureconditions_chimie[idx_chimie][1]
    except ValueError:
        debuts[id_mp_chimie] = None

    date_debut = min([value for value in debuts.values() if value])
    id_mp_fusion = list(debuts.keys())[list(debuts.values()).index(date_debut)]

    return key_dates_list, id_mp_fusion


def intersection(liste1, liste2):
    liste3 = [x for x in liste1 if x in liste2]
    return liste3


def independance(id_mp1, id_mp2):
    natures_mp1 = QueryScript(
        script=f'  SELECT nature   FROM {env.DATABASE_RAW}.pack WHERE measurepoint_id = ' + str(id_mp1)).execute()
    natures_mp2 = QueryScript(
        script=f'  SELECT nature   FROM {env.DATABASE_RAW}.pack WHERE measurepoint_id = ' + str(id_mp2)).execute()

    inter_natures = intersection(natures_mp1, natures_mp2)
    natures = {}

    if len(inter_natures) != 0:
        return True, natures

    else:
        for nature in natures_mp1:
            natures[nature] = id_mp1
        for nature in natures_mp2:
            natures[nature] = id_mp2

        return False, natures


def dates_insert(id_mp, dates):
    SQL_request = f" INSERT INTO key_dates (measurepoint_id, date_id, date, measurepoint_fusion_id, version) VALUES (%s, %s, %s, %s, %s)"
    values = []

    for i, date in enumerate(dates):
        key = date
        measurepoint_id = id_mp
        date_id = i+1
        date = dates[key]['date']
        measurepoint_fusion_id = id_mp

        values.append((measurepoint_id, date_id, date, measurepoint_fusion_id))


    QueryScript(SQL_request, values).executemany()
    print(' --> dates insérées')


def fusion_dates_insert(id_mp_list, dates):
    [id_mp_alim, id_mp_chimie, id_mp_repro, id_mp_fusion] = id_mp_list
    SQL_request = "INSERT INTO key_dates (measurepoint_id, date_id, date, measurepoint_fusion_id, version) VALUES (%s, %s, %s, %s,%s)"
    values = []

    for i, date in enumerate(dates):
        key = date

        if i in [0, 1, 2]:
            measurepoint_id = id_mp_alim
        elif i in [3, 4]:
            measurepoint_id = id_mp_repro
        else:
            measurepoint_id = id_mp_chimie

        date_id = i+1
        date = dates[key]['date']
        measurepoint_fusion_id = id_mp_fusion

        values.append((measurepoint_id, date_id, date, measurepoint_fusion_id))
    # print(f"id_mp_list = {id_mp_list}")
    # print(SQL_request)
    # print(values)

    QueryScript(SQL_request, values).executemany()
    print(' --> dates insérées (mode fusion)')

# %% ## RECUPERATION ET INSERTION DES DATES CLEES ##


def fill_date_table():
    id_campaigns = QueryScript(script=f'  SELECT id   FROM {env.DATABASE_RAW}.campaign').execute()
    for id_c in id_campaigns:
        places = QueryScript(
            script=f'  SELECT id, type   FROM {env.DATABASE_RAW}.place WHERE campaign_id=' + str(id_c)).execute()
        n_places = len(places)
        for i in range(n_places):
            id_p, type_p = places[i]

            id_measurepoints = QueryScript(
                script=f'  SELECT id   FROM {env.DATABASE_RAW}.measurepoint WHERE place_id=' + str(id_p)).execute()

            print('\n[+] id_place = ', id_p)

            if type_p != 'point_monitoring':  # type_p appartient ici à work_monitoring, other ou null
                for id_mp in id_measurepoints:
                    key_date_list = key_dates(id_mp)
                    dates_insert(id_mp, key_date_list)

            else:

                # S'il n'y a qu'un seul point de mesure à un endroit (place) il n'y a aucune fusion de dates a faire
                if len(id_measurepoints) == 1:
                    id_mp = id_measurepoints[0]
                    key_date_list = key_dates(id_mp)
                    dates_insert(id_mp, key_date_list)

                # S'il y a plus de 3 points de mesure à un endroit (place) --> gérer comme si les points étaient indépendants
                elif len(id_measurepoints) > 2:
                    print(
                        f"[+] /!\ plus de 3 points de mesures /!\ id_place = {id_p}")
                    print('[+] Ils sont donc considérés comme indépendants')
                    # print('[+] point_monitoring --> id_measurepoints = ', id_measurepoints)
                    for id_mp in id_measurepoints:
                        key_date_list = key_dates(id_mp)
                        dates_insert(id_mp, key_date_list)

                # Dernier cas: S'il y a exactement 2 points de mesure à un endroit <=> possibles biotests effectués à des périodes différentes donc fusion des dates
                # sinon voir les points comme indépendants
                else:
                    [id_mp1, id_mp2] = id_measurepoints
                    resultat, natures = independance(id_mp1, id_mp2)

                    # Si les points sont indépendants (c'est à dire qu'ils ont des types de biotests communs)
                    if resultat:
                        for id_mp in id_measurepoints:
                            key_date_list = key_dates(id_mp)
                            dates_insert(id_mp, key_date_list)

                    else:
                        try:
                            id_mp_alim = natures['alimentation']
                        except KeyError:
                            id_mp_alim = None

                        try:
                            id_mp_chimie = natures['chemistry']
                        except KeyError:
                            id_mp_chimie = None

                        try:
                            id_mp_repro = natures['reproduction']
                        except KeyError:
                            id_mp_repro = None

                        if id_mp_repro != id_mp_chimie:
                            print(
                                '\n /!\\ Erreur le point de mesure pour la chemistry est différent du point de mesure pour la reproduction')
                        key_date_list, id_mp_fusion = key_datesFusion(
                            id_mp_alim, id_mp_chimie, id_mp_repro)
                        id_list = [id_mp_alim, id_mp_chimie,
                                   id_mp_repro, id_mp_fusion]

                        fusion_dates_insert(id_list, key_date_list)

def run(cas):
    ## On a 3 cas pour les requêtes SQL
    # Cas 1: 'première_version'
    # Cas 2: 'update_version'
    # Cas 3: 'nouvelle_version'

    ## Cas 1: Création et remplissage de la base de données
    if cas == 1:
        create_empty_date_table()
        fill_date_table()

    ## Cas 2: Mise à jour de la dernière version connue
    if cas == 2:
        version = env.LATEST_VERSION()
        db_treated = env.DATABASE_TREATED
        delete_query = QueryScript(f"DELETE FROM {db_treated}.key_dates WHERE version = {version};")
        delete_query.execute()
        fill_date_table()

    ## Cas 3: Ajout d'une nouvelle version
    if cas == 3:
        fill_date_table()
