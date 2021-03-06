from tools import QueryScript
from math import *
from scipy.stats import binom
from collections import Counter
from datetime import date
import env

class Reprotoxicity:

    @staticmethod
    # retourne dict_nbr_days_exposition = {mp: nbrdays}
    def number_days_exposition(dict_pack):

        nature = 'reproduction'
        list_mp_repro = []
        for mp in dict_pack:
            try:
                dict_pack[mp][nature]
            except KeyError:
                pass
            else:
                list_mp_repro.append(mp)

        # Récupération des dates de début et de fin
        output_dates_debut = QueryScript(
            f" SELECT measurepoint_id, date   FROM {env.DATABASE_TREATED}.key_dates where date_id=1 and measurepoint_id IN {tuple(list_mp_repro) if len(list_mp_repro)>1 else '('+(str(list_mp_repro[0]) if len(list_mp_repro) else '0')+')'} and version=  {env.CHOSEN_VERSION()};"
        ).execute()
        output_dates_fin = QueryScript(
            f" SELECT measurepoint_id, date   FROM {env.DATABASE_TREATED}.key_dates where date_id=4 and measurepoint_id IN {tuple(list_mp_repro) if len(list_mp_repro)>1 else '('+(str(list_mp_repro[0]) if len(list_mp_repro) else '0')+')'} and version=  {env.CHOSEN_VERSION()};"
        ).execute()

        output_mp_debut = [x[0] for x in output_dates_debut]
        output_mp_fin = [x[0] for x in output_dates_fin]

        dict_dates_debut_fin = {}  # {mp: [date_debut, date_fin]}
        for mp in list_mp_repro:
            try : 
                idx_debut = output_mp_debut.index(mp)
                idx_fin = output_mp_fin.index(mp)
                dict_dates_debut_fin[mp] = [output_dates_debut[idx_debut][1], output_dates_fin[idx_fin][1]]
            except ValueError:
                dict_dates_debut_fin[mp] = [None, None]
        # Initialisation du dictionnaire de sortie
        dict_nbr_days_exposition = {mp: None for mp in dict_pack}  # {mp: nbrdays}

        # Calcul
        for mp in list_mp_repro:
            [date_debut, date_fin] = dict_dates_debut_fin[mp]
            if date_debut is not None and date_fin is not None:
                if date_debut is None and date_fin is None:
                    dict_nbr_days_exposition[mp] = "NA"
                else:
                    date_fin_sans_heure = date(date_fin.year, date_fin.month, date_fin.day)
                    date_debut_sans_heure = date(date_debut.year, date_debut.month, date_debut.day)
                    nbrdays = (date_fin_sans_heure - date_debut_sans_heure).days
                    dict_nbr_days_exposition[mp] = nbrdays
            else:
                dict_nbr_days_exposition[mp] = "NA"

        return dict_nbr_days_exposition

    @staticmethod
    # retourne dict_index_fecundity = {pack_id: {'list_molting_stage': [...], 'list_index_fecundity': [...]}
    def index_fecundity_female(list_pack_repro):
        SQL_request = f"  SELECT pack_id, female, molting_stage, embryo_stage, specimen_size_mm, specimen_size_px, embryo_total FROM {env.DATABASE_RAW}.MeasureReprotoxicity where pack_id IN {tuple(list_pack_repro) if len(list_pack_repro)>1 else '('+(str(list_pack_repro[0]) if len(list_pack_repro) else '0')+')'};"
        output = QueryScript(SQL_request).execute()

        # Initialisation du dictionnaire de la requête mise en forme
        # {pack_id: {'px_to_mm': int, 'data': [[molting_stage, embryo_stage, specimen_size_mm, specimen_size_px, embryo_total], [...]] }}
        dict_result = {pack_id: {'px_to_mm': None, 'data': []} for pack_id in list_pack_repro}

        pack_errors = []

        for row in output:
            [pack_id, female, molting_stage, embryo_stage, specimen_size_mm, specimen_size_px, embryo_total] = row

            if female == '' or female == '0bis':
                continue

            if int(female) == 0:  # Valeur étalon
                try:
                    px_to_mm = specimen_size_mm/specimen_size_px
                except (TypeError, ZeroDivisionError):
                    pack_errors.append(pack_id)
                    continue
                dict_result[pack_id]['px_to_mm'] = px_to_mm
            elif female is not None:  # Données à traiter ensuite
                data = [molting_stage, embryo_stage, specimen_size_mm, specimen_size_px, embryo_total]
                dict_result[pack_id]['data'].append(data)

        # Initialisation du dictionnaire de sortie
        dict_index_fecundity = {pack_id: {'list_molting_stage': [], 'list_index_fecundity': []} for pack_id in list_pack_repro}

        for pack_id in dict_result.keys():
            data = dict_result[pack_id]['data']
            px_to_mm = dict_result[pack_id]['px_to_mm']
            for row in data:
                [molting_stage, embryo_stage, specimen_size_mm, specimen_size_px, embryo_total] = row

                if len(row) == 0:
                    dict_index_fecundity[pack_id]['list_index_fecundity'].append(0)
                else:
                    dict_index_fecundity[pack_id]['list_molting_stage'].append(molting_stage)
                    if embryo_stage in [2, 3, 4]:
                        if embryo_total == 0:
                            dict_index_fecundity[pack_id]['list_index_fecundity'].append(0)
                        else:
                            if specimen_size_mm is None or specimen_size_mm == 0:
                                if specimen_size_px == 0:
                                    continue
                                try:
                                    specimen_size_mm = specimen_size_px * px_to_mm
                                except TypeError:
                                    pack_errors.append(pack_id)
                                    continue
                            if specimen_size_mm == 0:
                                pack_errors.append(pack_id)
                                continue
                            dict_index_fecundity[pack_id]['list_index_fecundity'].append(embryo_total/(specimen_size_mm-5))
                    else:
                        dict_index_fecundity[pack_id]['list_index_fecundity'].append(0)
        return dict_index_fecundity  # {pack_id: {'list_molting_stage': [...], 'list_index_fecundity': [...]}

    @staticmethod
    # retourne dict_fecundity = {mp: {'nbr_femelles_analysées': int, 'nbr_femelles_concernées': int, 'fécondité_moyenne': float}}
    def fecundity(dict_pack):
        nature = 'reproduction'
        list_pack_repro = []
        list_mp_repro = []
        for mp in dict_pack:
            try:
                pack_id = dict_pack[mp][nature]
            except KeyError:
                pass
            else:
                list_mp_repro.append(mp)
                list_pack_repro.append(pack_id)

        dict_index_fecundity = Reprotoxicity.index_fecundity_female(list_pack_repro)  # {pack_id: {'list_molting_stage': [...], 'list_index_fecundity': [...]}

        # Initialisation du dictionnaire de sortie
        # {mp: {{'nbr_femelles_analysées': int, 'nbr_femelles_concernées': int, 'fécondité_moyenne': float}}
        dict_fecundity = {mp: {'nbr_femelles_analysées': None, 'nbr_femelles_concernées': None, 'fécondité_moyenne': None} for mp in dict_pack.keys()}

        for pack_id in dict_index_fecundity.keys():
            list_index_fecundity_not_clean = dict_index_fecundity[pack_id]['list_index_fecundity']
            list_molting_stage_not_clean = dict_index_fecundity[pack_id]['list_molting_stage']

            list_index_fecundity = [x for x in list_index_fecundity_not_clean if x != 0]
            list_molting_stage = [x for x in list_molting_stage_not_clean if x is not None]

            mp = list_mp_repro[list_pack_repro.index(pack_id)]

            nbr_femelles_concernees = len(list_index_fecundity) - list_index_fecundity.count(0)
            dict_fecundity[mp]['nbr_femelles_concernées'] = nbr_femelles_concernees

            cpt_molting_stage = Counter(list_molting_stage)
            cpt_filtre = [cpt_molting_stage.get(molting_stage) for molting_stage in ['b', 'c1', 'c2', 'd1', 'd2']]

            nbr_femelles_analysees = 0
            for x in cpt_filtre:
                if x is not None:
                    nbr_femelles_analysees += x

            if nbr_femelles_analysees == 0:
                dict_fecundity[mp]['nbr_femelles_analysées'] = 'NA'
            else:
                dict_fecundity[mp]['nbr_femelles_analysées'] = nbr_femelles_analysees

            if nbr_femelles_analysees >= 10 and len(list_index_fecundity) != 0:
                fecondite_moyenne = sum(list_index_fecundity)/len(list_index_fecundity)
            else:
                fecondite_moyenne = "NA"
            dict_fecundity[mp]['fécondité_moyenne'] = fecondite_moyenne

        return dict_fecundity

    @staticmethod
    # retourne dict_molting = {mp: {'cycle de mue': ..%, 'cycle de mue attendu': ..%, 'nb_femelles_retard': int}}
    def molting_cycle(dict_pack):
        nature = 'reproduction'
        list_pack_repro = []
        list_mp_repro = []
        for mp in dict_pack:
            try:
                pack_id = dict_pack[mp][nature]
            except KeyError:
                pass
            else:
                list_mp_repro.append(mp)
                list_pack_repro.append(pack_id)

        SQL_request = f"  SELECT pack_id, molting_stage FROM {env.DATABASE_RAW}.MeasureReprotoxicity where pack_id IN {tuple(list_pack_repro) if len(list_pack_repro)>1 else '('+(str(list_pack_repro[0]) if len(list_pack_repro) else '0')+')'};"
        SQL_request_2 = f"  SELECT measurepoint_id, expected_C2,expected_D2 FROM {env.DATABASE_TREATED}.temperature_repro where measurepoint_id IN {tuple(list_mp_repro) if len(list_mp_repro)>1 else '('+(str(list_mp_repro[0]) if len(list_mp_repro) else '0')+')'};"
        resultat_molting_stage =  QueryScript(SQL_request).execute()
        resultat_expected_stage =  QueryScript(SQL_request_2).execute()

        dict_molting_stage = {pack_id: [] for pack_id in list_pack_repro}
        for row in resultat_molting_stage:
            [pack_id, molting_stage] = row
            dict_molting_stage[pack_id].append(molting_stage)

        dict_expected_stage = {mp: {'expected C2': None, 'expected D2': None} for mp in list_mp_repro}
        for row in resultat_expected_stage:
            [measurepoint_id, expected_C2, expected_D2] = row
            dict_expected_stage[measurepoint_id]['expected C2'] = expected_C2
            dict_expected_stage[measurepoint_id]['expected D2'] = expected_D2

        # Initialisation du dictionnaire de sortie
        dict_molting = {mp: {'cycle de mue': None, 'cycle de mue attendu': None, 'nb_femelles_retard': None} for mp in dict_pack.keys()}

        # Remplissage du dictionnaire de sortie
        for i, mp in enumerate(list_mp_repro):
            pack_id = list_pack_repro[i]
            expected_C2 = dict_expected_stage[mp]['expected C2']
            expected_D2 = dict_expected_stage[mp]['expected D2']
            dict_molting[mp]['cycle de mue attendu'] = expected_C2 if (expected_C2 == 'NA' or expected_C2 is None) else round(expected_C2-expected_D2)

            list_molting_stage = dict_molting_stage[pack_id]
            cpt_molting_stage = Counter(list_molting_stage)
            cpt_analysees = [cpt_molting_stage.get(molting_stage) for molting_stage in ['b', 'c1', 'c2', 'd1', 'd2']]
            cpt_c2_d1 = [cpt_molting_stage.get(molting_stage) for molting_stage in ['c2', 'd1']]

            nbr_femelles_analysees = 0
            for x in cpt_analysees:
                if x is not None:
                    nbr_femelles_analysees += x

            nbr_femelles_c2_d1 = 0
            for x in cpt_c2_d1:
                if x is not None:
                    nbr_femelles_c2_d1 += x

            if nbr_femelles_analysees == 0:
                molting_percent = 'NA'
            else:
                molting_percent = nbr_femelles_c2_d1/nbr_femelles_analysees

            dict_molting[mp]['cycle de mue'] = molting_percent if (molting_percent == 'NA' or molting_percent is None) else round(molting_percent*100)
            dict_molting[mp]['nb_femelles_retard'] = nbr_femelles_c2_d1

        return dict_molting  # {mp: {'cycle de mue': ..%, 'cycle de mue attendu': ..%, 'nb_femelles_retard': int}}

    @staticmethod
    # retourne dict_surface_femelles_concernees, dict_surface_des_retards
    # dict_surface_femelles_concernees = {mp: nbr_femelles_concernees}
    # dict_surface_des_retards = {pack_id: [oocyte_area_mm, ...]}
    def number_female_concerned_area(dict_pack):
        nature = 'reproduction'
        list_pack_repro = []
        list_mp_repro = []
        for mp in dict_pack:
            try:
                pack_id = dict_pack[mp][nature]
            except KeyError:
                pass
            else:
                list_mp_repro.append(mp)
                list_pack_repro.append(pack_id)

        output = QueryScript(
            f"  SELECT pack_id, female, molting_stage, oocyte_area_pixel, oocyte_area_mm   FROM {env.DATABASE_RAW}.MeasureReprotoxicity WHERE pack_id IN {tuple(list_pack_repro) if len(list_pack_repro)>1 else '('+(str(list_pack_repro[0]) if len(list_pack_repro) else '0')+')'};"
        ).execute()

        # Reformatage des données de la requête
        dict_surface_ovocytaire = {pack_id: {'px_to_mm': None, 'data': []} for pack_id in list_pack_repro}

        for row in output:
            [pack_id, female, molting_stage, oocyte_area_pixel, oocyte_area_mm] = row

            if female == '' or female == '0bis':
                continue

            if int(female) == 0:
                try:
                    dict_surface_ovocytaire[pack_id]['px_to_mm'] = oocyte_area_pixel / (oocyte_area_mm * 97.82)  # Formule écrite en dure dans l'excel contenant les macros
                except TypeError:
                    pass
            else:
                data = [molting_stage, oocyte_area_pixel, oocyte_area_mm]
                dict_surface_ovocytaire[pack_id]['data'].append(data)

        # Calcul des surfaces des retards
        dict_surface_des_retards = {pack_id: [] for pack_id in list_pack_repro}

        for pack_id in dict_surface_ovocytaire.keys():
            px_to_mm = dict_surface_ovocytaire[pack_id]['px_to_mm']
            data = dict_surface_ovocytaire[pack_id]['data']

            if len(data) == 0:
                continue

            else:
                for [molting_stage, oocyte_area_pixel, oocyte_area_mm] in data:
                    if oocyte_area_mm is not None:
                        surface_retard = oocyte_area_mm
                        dict_surface_des_retards[pack_id].append(surface_retard)
                        continue

                    if molting_stage in ['c1', 'b'] and oocyte_area_pixel is not None:
                        if px_to_mm is None:
                            continue
                        surface_retard = oocyte_area_pixel * px_to_mm
                        dict_surface_des_retards[pack_id].append(surface_retard)
                    else:
                        continue

        # Calcul nbr_femelles_concernées
        dict_surface_femelles_concernees = {mp: 0 for mp in dict_pack.keys()}

        for mp in dict_surface_femelles_concernees.keys():
            if mp not in list_mp_repro:
                continue
            else:
                pack_id = dict_pack[mp]['reproduction']
                nbr_femelles_concernees = len(dict_surface_des_retards[pack_id])
                dict_surface_femelles_concernees[mp] = nbr_femelles_concernees

        return dict_surface_femelles_concernees, dict_surface_des_retards

    @staticmethod
    # Identique à la fonction LOI.BINOMIALE.INVERSE() de Excel
    def binom_inv(n, p, s):
        for k in range(n+1):
            if binom.cdf(k, n, p) > s:
                return k
        if k == n:
            return None

    @staticmethod
    # retourne dict_conform_resultat_mue = {pack_id: 'NA', 'Retard fort', 'Retard modéré' ou 'Conforme'}
    def conform_resultat_mue(dict_pack):

        nature = 'reproduction'
        list_pack_repro = []
        list_mp_repro = []
        for mp in dict_pack:
            try:
                pack_id = dict_pack[mp][nature]
            except KeyError:
                pass
            else:
                list_mp_repro.append(mp)
                list_pack_repro.append(pack_id)

        # Récupération du nombre de retard et du nombre de femelles analysées
        output_molting = QueryScript(
            f"  SELECT pack_id, molting_stage FROM {env.DATABASE_RAW}.MeasureReprotoxicity where pack_id IN {tuple(list_pack_repro) if len(list_pack_repro)>1 else '('+(str(list_pack_repro[0]) if len(list_pack_repro) else '0')+')'};"
        ).execute()

        dict_molting_stage = {pack_id: [] for pack_id in list_pack_repro}
        for row in output_molting:
            [pack_id, molting_stage] = row
            dict_molting_stage[pack_id].append(molting_stage)

        dict_nombre_femelles = {pack_id: {'nbr_retards': 0, 'nbr_analysées': 0} for pack_id in list_pack_repro}
        for pack_id in list_pack_repro:
            list_molting_stage = dict_molting_stage[pack_id]
            cpt_molting_stage = Counter(list_molting_stage)
            cpt_analysees = [cpt_molting_stage.get(molting_stage) for molting_stage in ['b', 'c1', 'c2', 'd1', 'd2']]
            cpt_retards = [cpt_molting_stage.get(molting_stage) for molting_stage in ['b', 'c1']]

            nbr_analysees = sum([x for x in cpt_analysees if x is not None])
            nbr_retards = sum([x for x in cpt_retards if x is not None])

            dict_nombre_femelles[pack_id]['nbr_retards'] = nbr_retards
            dict_nombre_femelles[pack_id]['nbr_analysées'] = nbr_analysees

        ## Calcul des valeurs de test unilatéral
        # Récupération du pourcentage attendu en B/C1
        output_expected = QueryScript(
            f"  SELECT measurepoint_id, expected_C2   FROM {env.DATABASE_TREATED}.temperature_repro WHERE measurepoint_id IN {tuple(list_mp_repro) if len(list_mp_repro)>1 else '('+(str(list_mp_repro[0]) if len(list_mp_repro) else '0')+')'} and version=  {env.CHOSEN_VERSION()};"
        ).execute()
        dict_expected_BC1 = {pack_id: 0 for pack_id in list_pack_repro}

        for row in output_expected:
            [mp, expected_C2] = row
            pack_id = dict_pack[mp]['reproduction']
            dict_expected_BC1[pack_id] = 100-expected_C2

        # Récupération des seuils de référence
        output_reference = QueryScript(
            f"  SELECT name, value   FROM {env.DATABASE_TREATED}.r2_constant WHERE name IN ('Risque 1 Mue', 'Risque 2 Mue') and version=  {env.CHOSEN_VERSION()};"
        ).execute()
        for row in output_reference:
            [name, value] = row
            if name == 'Risque 1 Mue':
                seuil_test_5percent = value
            else:
                seuil_test_1percent = value

        # Calcul des valeurs de test unilatéral
        dict_test_unilateral = {pack_id: {'test_5percent': 0, 'test_1percent': 0} for pack_id in list_pack_repro}

        for pack_id in dict_test_unilateral.keys():
            nbr_analysees = dict_nombre_femelles[pack_id]['nbr_analysées']
            expected_BC1 = dict_expected_BC1[pack_id]

            test_5percent = Reprotoxicity.binom_inv(nbr_analysees, expected_BC1/100, seuil_test_5percent)
            test_1percent = Reprotoxicity.binom_inv(nbr_analysees, expected_BC1/100, seuil_test_1percent)

            dict_test_unilateral[pack_id]['test_5percent'] = test_5percent
            dict_test_unilateral[pack_id]['test_1percent'] = test_1percent

        ## Calcul de la conformité des mues
        dict_conform_resultat_mue = {mp: "NA" for mp in dict_pack.keys()}

        for pack_id in list_pack_repro:
            mp = list_mp_repro[list_pack_repro.index(pack_id)]
            nbr_analysees = dict_nombre_femelles[pack_id]['nbr_analysées']
            if nbr_analysees < 10:
                dict_conform_resultat_mue[mp] = "NA"
                continue

            nbr_retards = dict_nombre_femelles[pack_id]['nbr_retards']
            test_5percent = dict_test_unilateral[pack_id]['test_5percent']
            test_1percent = dict_test_unilateral[pack_id]['test_1percent']
            if nbr_retards > test_5percent:
                dict_conform_resultat_mue[mp] = "Retard fort"
            elif nbr_retards > test_1percent:
                dict_conform_resultat_mue[mp] = "Retard modéré"
            else:
                dict_conform_resultat_mue[mp] = "Conforme"

        return dict_conform_resultat_mue

    @staticmethod
    # retourne dict_conform_surface_retard = {pack_id: 'NA', 'PE', 'Conforme BC1' ou 'Conforme'}
    def conform_surface_retard(dict_pack, dict_surface_femelles_concernees, dict_surface_des_retards, dict_fecundity):
        nature = 'reproduction'
        list_pack_repro = []
        list_mp_repro = []
        for mp in dict_pack:
            try:
                pack_id = dict_pack[mp][nature]
            except KeyError:
                pass
            else:
                list_mp_repro.append(mp)
                list_pack_repro.append(pack_id)

        ## Surface moyenne des retards
        dict_surface_moyenne_retards = {mp: None for mp in dict_pack.keys()}
        for pack_id in list_pack_repro:
            mp = list_mp_repro[list_pack_repro.index(pack_id)]
            nbr_analysees = dict_fecundity[mp]['nbr_femelles_analysées']
            list_surface_retards = dict_surface_des_retards[pack_id]
            if nbr_analysees == 'NA':
                continue
            if nbr_analysees >= 10:
                try:
                    dict_surface_moyenne_retards[mp] = sum(list_surface_retards)/len(list_surface_retards)
                except ZeroDivisionError:
                    pass



        ## Seuil unilatéral 5%
        # Récupération des références
        names = ['Constante surface des retards 1', 'Moyenne des surfaces de référence C2', 'SD des surfaces de référence C2']

        output_ref = QueryScript(
            f"  SELECT name, value   FROM {env.DATABASE_TREATED}.r2_constant WHERE name IN {tuple(names) if len(names)>1 else '('+(str(names[0]) if len(names) else '0')+')'} and version= {env.CHOSEN_VERSION()};"
        ).execute()
        for row in output_ref:
            [name, value] = row
            if name == 'Constante surface des retards 1':
                cst_surface_des_retards = value
            if name == 'Moyenne des surfaces de référence C2':
                moyenne_surface_refC2 = value
            if name == 'SD des surfaces de référence C2':
                SD_surface_refC2 = value

        # Calcul des seuils
        dict_seuil_unilateral_5percent = {pack_id: None for pack_id in list_pack_repro}
        for pack_id in list_pack_repro:
            mp = list_mp_repro[list_pack_repro.index(pack_id)]
            nbr_concernees = dict_surface_femelles_concernees[mp]
            try:
                seuil_5percent = moyenne_surface_refC2 - cst_surface_des_retards * SD_surface_refC2 / sqrt(nbr_concernees)
            except ZeroDivisionError:
                pass
            else:
                dict_seuil_unilateral_5percent[pack_id] = seuil_5percent

        ## Calcul de la conformité des surfaces des retards
        # Récupération de données
        dict_conform_resultat_mue = Reprotoxicity.conform_resultat_mue(dict_pack)

        # Initialisation du dictionnaire de sortie
        dict_conform_surface_retard = {mp: "NA" for mp in dict_pack.keys()}

        for pack_id in list_pack_repro:
            mp = list_mp_repro[list_pack_repro.index(pack_id)]
            nbr_analysees = dict_fecundity[mp]['nbr_femelles_analysées']

            if nbr_analysees == 'NA' or nbr_analysees < 10:
                continue

            conform_mue = dict_conform_resultat_mue[mp]
            if conform_mue == "Retard fort" or conform_mue == "Retard modéré":
                surface_moyenne_retards = dict_surface_moyenne_retards[mp]
                seuil_5percent = dict_seuil_unilateral_5percent[pack_id]
                if surface_moyenne_retards is None or seuil_5percent is None:
                    continue
                if surface_moyenne_retards > seuil_5percent:
                    dict_conform_surface_retard[mp] = "PE"
                else:
                    dict_conform_surface_retard[mp] = "Conforme BC1"
            else:
                dict_conform_surface_retard[mp] = "Conforme"

        return dict_conform_surface_retard, dict_surface_moyenne_retards

    @staticmethod
    # retourne dict_perturbation_endocrinienne = {mp: 'NA' ou moyenne des surfaces des retards}
    def perturbation_endocrinienne(dict_pack, dict_surface_femelles_concernees, dict_surface_des_retards, dict_fecundity):
        nature = 'reproduction'
        list_pack_repro = []
        list_mp_repro = []
        for mp in dict_pack:
            try:
                pack_id = dict_pack[mp][nature]
            except KeyError:
                pass
            else:
                list_mp_repro.append(mp)
                list_pack_repro.append(pack_id)

        # Récupération de données
        dict_conform_surface_retard, dict_surface_moyenne_retards = Reprotoxicity.conform_surface_retard(dict_pack, dict_surface_femelles_concernees, dict_surface_des_retards, dict_fecundity)

        # Initialisation du dictionnaire de sortie
        dict_perturbation_endocrinienne = {mp: "NA" for mp in dict_pack.keys()}

        for mp in dict_pack.keys():
            if mp not in list_mp_repro:
                continue
            conform_surface = dict_conform_surface_retard[mp]
            moyenne_surface = dict_surface_moyenne_retards[mp]

            if conform_surface == "Conforme":
                continue
            else:
                dict_perturbation_endocrinienne[mp] = moyenne_surface

        return dict_perturbation_endocrinienne


               
                       




               
   


     






          
          
          










  
    



     
     
     
     

    
