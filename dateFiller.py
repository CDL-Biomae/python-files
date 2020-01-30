#%% ## IMPORT ##
from query import QueryScript

#%% ## FONCTIONS ##

def createEmptyDateTable():
    datesclees_table = QueryScript(
        "DROP TABLE IF EXISTS datesclees; CREATE TABLE datesclees (id INT AUTO_INCREMENT PRIMARY KEY, measurepoint_id INT, date_id INT, date DATETIME, measurepoint_fusion_id INT);")
    datesclees_table.execute()
    print('La table datesclees a été créée')

def datesClees(id_mp):
    exposureconditions = QueryScript(
        script='SELECT step, recordedAt, barrel FROM measureexposurecondition WHERE measurepoint_id=' + str(
            id_mp)).execute()
    steps_barrels = [(x[0], x[2]) for x in exposureconditions]
    # print(steps_barrels)
    # print(exposureconditions[0])

    # Dictionnaire de dates cles à remplir
    dates_cles = {}

    # (step 50, R0) Transplantation Alimentation
    try:
        idx = steps_barrels.index((50, 'R0'))
        temp_date = exposureconditions[idx][1]
    except ValueError:
        temp_date = None

    dates_cles['Transplantation Alimentation'] = {'date': temp_date, 'step': 50, 'barrel': 'R0'}

    # (step 60, R7) Recuperation Alimentation
    try:
        idx = steps_barrels.index((60, 'R7'))
        temp_date = exposureconditions[idx][1]
    except ValueError:
        temp_date = None

    dates_cles['Recuperation Alimentation'] = {'date': temp_date, 'step': 60, 'barrel': 'R7'}

    # (step 20) Lancement Alimentation
    try:
        idx = steps_barrels.index((20, None))
        temp_date = exposureconditions[idx][1]
    except ValueError:
        temp_date = None

    dates_cles['Lancement Alimentation'] = {'date': temp_date, 'step': 20, 'barrel': None}

    # (step 140, RN) Recuperation Reprotoxicité
    try:
        idx = steps_barrels.index((140, 'RN'))
        temp_date = exposureconditions[idx][1]
    except ValueError:
        temp_date = None

    dates_cles['Recuperation Reprotoxicite'] = {'date': temp_date, 'step': 140, 'barrel': 'RN'}

    # (step 170) Arrêt Reprotoxicité
    try:
        idx = steps_barrels.index((170, None))
        temp_date = exposureconditions[idx][1]
    except ValueError:
        temp_date = None

    dates_cles['Arret Reprotoxicite'] = {'date': temp_date, 'step': 170, 'barrel': None}

    # (step 50, C0) Lancement Chimie (=Lancement reprotoxicité)
    try:
        idx = steps_barrels.index((50, 'C0'))
        temp_date = exposureconditions[idx][1]
    except ValueError:
        temp_date = None

    dates_cles['Lancement Chimie'] = {'date': temp_date, 'step': 50, 'barrel': 'C0'}

    # (step 100, R21) Récupération Chimie
    try:
        idx = steps_barrels.index((100, 'R21'))
        temp_date = exposureconditions[idx][1]
    except ValueError:
        temp_date = None

    dates_cles['Recuperation Chimie'] = {'date': temp_date, 'step': 100, 'barrel': 'R21'}

    return dates_cles

def datesCleesFusion(id_mp_alim, id_mp_chimie, id_mp_repro):
    if id_mp_alim != None:
        exposureconditions_alim = QueryScript(script='SELECT step, recordedAt, barrel FROM measureexposurecondition WHERE measurepoint_id=' + str(id_mp_alim)).execute()
    else:
        exposureconditions_alim = []

    if id_mp_chimie != None:
        exposureconditions_chimie = QueryScript(script='SELECT step, recordedAt, barrel FROM measureexposurecondition WHERE measurepoint_id=' + str(id_mp_chimie)).execute()
    else:
        exposureconditions_chimie = []

    if id_mp_repro != None:
        exposureconditions_repro = QueryScript(script='SELECT step, recordedAt, barrel FROM measureexposurecondition WHERE measurepoint_id=' + str(id_mp_repro)).execute()
    else:
        exposureconditions_repro = []

    steps_barrels_alim = [(x[0], x[2]) for x in exposureconditions_alim] if len(exposureconditions_alim) else []
    steps_barrels_chimie = [(x[0], x[2]) for x in exposureconditions_chimie] if len(exposureconditions_chimie) else []
    steps_barrels_repro = [(x[0], x[2]) for x in exposureconditions_repro] if len(exposureconditions_repro) else []

    # print(steps_barrels_alim)
    # print(steps_barrels_chimie)
    # print(steps_barrels_repro)

    # Dictionnaire de dates cles à remplir
    dates_cles = {}

    # (step 50, R0) Transplantation Alimentation
    try:
        idx = steps_barrels_alim.index((50, 'R0'))
        temp_date = exposureconditions_alim[idx][1]
    except ValueError:
        temp_date = None

    dates_cles['Transplantation Alimentation'] = {'date': temp_date, 'step': 50, 'barrel': 'R0'}

    # (step 60, R7) Recuperation Alimentation
    try:
        idx = steps_barrels_alim.index((60, 'R7'))
        temp_date = exposureconditions_alim[idx][1]
    except ValueError:
        temp_date = None

    dates_cles['Recuperation Alimentation'] = {'date': temp_date, 'step': 60, 'barrel': 'R7'}

    # (step 20) Lancement Alimentation
    try:
        idx = steps_barrels_alim.index((20, None))
        temp_date = exposureconditions_alim[idx][1]
    except ValueError:
        temp_date = None

    dates_cles['Lancement Alimentation'] = {'date': temp_date, 'step': 20, 'barrel': None}

    # (step 140, RN) Recuperation Reprotoxicité
    try:
        idx = steps_barrels_repro.index((140, 'RN'))
        temp_date = exposureconditions_repro[idx][1]
    except ValueError:
        temp_date = None

    dates_cles['Recuperation Reprotoxicite'] = {'date': temp_date, 'step': 140, 'barrel': 'RN'}

    # (step 170) Arrêt Reprotoxicité
    try:
        idx = steps_barrels_repro.index((170, None))
        temp_date = exposureconditions_repro[idx][1]
    except ValueError:
        temp_date = None

    dates_cles['Arret Reprotoxicite'] = {'date': temp_date, 'step': 170, 'barrel': None}

    # (step 50, C0) Lancement Chimie (=Lancement reprotoxicité)
    try:
        idx = steps_barrels_chimie.index((50, 'C0'))
        temp_date = exposureconditions_chimie[idx][1]
    except ValueError:
        temp_date = None

    dates_cles['Lancement Chimie'] = {'date': temp_date, 'step': 50, 'barrel': 'C0'}

    # (step 100, R21) Récupération Chimie
    try:
        idx = steps_barrels_chimie.index((100, 'R21'))
        temp_date = exposureconditions_chimie[idx][1]
    except ValueError:
        temp_date = None

    dates_cles['Recuperation Chimie'] = {'date': temp_date, 'step': 100, 'barrel': 'R21'}

    return dates_cles

def intersection(liste1, liste2):
    liste3 = [x for x in liste1 if x in liste2]
    return liste3

def independance(id_mp1, id_mp2):
    natures_mp1 = QueryScript(script='SELECT nature FROM pack WHERE measurepoint_id = ' + str(id_mp1)).execute()
    natures_mp2 = QueryScript(script='SELECT nature FROM pack WHERE measurepoint_id = ' + str(id_mp2)).execute()

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

def insererDates(id_mp, dates):
    SQL_request = f"INSERT INTO datesclees (measurepoint_id, date_id, date, measurepoint_fusion_id) VALUES (%s, %s, %s, %s)"
    values = []

    for i in range(len(dates)):
        key = list(dates.keys())[i]
        measurepoint_id = id_mp
        date_id = i+1
        date = dates[key]['date']
        measurepoint_fusion_id = id_mp

        values.append((measurepoint_id, date_id, date, measurepoint_fusion_id))

    # print(SQL_request)
    # print(values)

    QueryScript(SQL_request, values).executemany()
    print(' --> dates insérées')

def insererDatesFusion(id_mp_list, dates):
    [id_mp_alim, id_mp_chimie, id_mp_repro] = id_mp_list
    SQL_request = f"INSERT INTO datesclees (measurepoint_id, date_id, date, measurepoint_fusion_id) VALUES (%s, %s, %s, %s)"
    values = []

    for i in range(len(dates)):
        key = list(dates.keys())[i]

        if i in [0, 1, 2]:
            measurepoint_id = id_mp_alim
        elif i in [3, 4]:
            measurepoint_id = id_mp_repro
        else:
            measurepoint_id = id_mp_chimie

        date_id = i+1
        date = dates[key]['date']
        measurepoint_fusion_id = id_mp_alim  # Pour l'instant le point de mesure de l'alimentation est considere commme le point de fusion des measurepoints

        values.append((measurepoint_id, date_id, date, measurepoint_fusion_id))
    # print(f"id_mp_list = {id_mp_list}")
    # print(SQL_request)
    # print(values)

    QueryScript(SQL_request, values).executemany()
    print(' --> dates insérées (mode fusion)')

#%% ## INITIALISATION ##

createEmptyDateTable()
campaigns = QueryScript(script='SELECT id, reference FROM campaign').execute()
id_campaigns = [x[0] for x in campaigns]

#%% ## RECUPERATION ET INSERTION DES DATES CLEES ##

for id_c in id_campaigns:
    places = QueryScript(script='SELECT id, reference, type FROM place WHERE campaign_id='+str(id_c)).execute()
    n_places = len(places)
    for i in range(n_places):
        id_p, ref_p, type_p = places[i]

        measurepoints = QueryScript(script='SELECT id, reference FROM measurepoint WHERE place_id=' + str(id_p)).execute()
        id_measurepoints = [x[0] for x in measurepoints]

        print('\n[+] id_place = ', id_p)
        # print('[+] type_place =', type_p)

        if type_p == 'work_monitoring':
            for id_mp in id_measurepoints:
                dates_clees = datesClees(id_mp)
                insererDates(id_mp, dates_clees)

        if type_p == 'point_monitoring':

            # S'il n'y a qu'un seul point de mesure à un endroit (place) il n'y a aucune fusion de dates a faire
            if len(id_measurepoints) == 1:
                id_mp = id_measurepoints[0]
                dates_clees = datesClees(id_mp)
                insererDates(id_mp, dates_clees)

            # Pas encore fait..
            # S'il y a plus de 3 points de mesure à un endroit (place) --> gérer comme si les points étaient indépendants
            elif len(id_measurepoints) > 2:
                print(f"[+] /!\ plus de 3 points de mesures /!\ id_place = {id_p}")
                print('[+] Ils sont donc considérés comme indépendants')
                # print('[+] point_monitoring --> id_measurepoints = ', id_measurepoints)
                for id_mp in id_measurepoints:
                    dates_clees = datesClees(id_mp)
                    insererDates(id_mp, dates_clees)
                    # print(steps_barrels)
                    # print(exposureconditions[0])

            # Dernier cas: S'il y a exactement 2 points de mesure à un endroit <=> possibles biotests effectués à des périodes différentes donc fusion des dates
            # sinon voir les points comme indépendants
            else:
                # print('\n[+] id_place = ', id_p)
                # print('[+] point_monitoring --> id_measurepoints = ', id_measurepoints)

                [id_mp1, id_mp2] = id_measurepoints
                resultat, natures = independance(id_mp1, id_mp2)

                if resultat:  # Si les points sont indépendants (c'est à dire qu'ils ont des types de biotests communs)
                    for id_mp in id_measurepoints:
                        dates_clees = datesClees(id_mp)
                        insererDates(id_mp, dates_clees)

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
                        print('\n /!\\ Erreur le point de mesure pour la chimie est différent du point de mesure pour la reproduction')
                    dates_clees = datesCleesFusion(id_mp_alim, id_mp_chimie, id_mp_repro)
                    id_list = [id_mp_alim, id_mp_chimie, id_mp_repro]

                    insererDatesFusion(id_list, dates_clees)

