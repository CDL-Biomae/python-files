import pandas as pd
from tools import QueryScript
import env
import datetime
from calcul import Reprotoxicity 

def create_calcul_tox_dataframe(campaign_list, campaign_dict, J_dict,  measurepoint_list, pack_list) :

    constant_list = QueryScript(f"SELECT name, value   FROM {env.DATABASE_TREATED}.r2_constant WHERE version={env.CHOSEN_VERSION()}").execute()
    constant_dict = {}
    for name, value in constant_list:
        if name :
            constant_dict[name] = value

    matrix = []
    matrix.append(["Mois de transplantation"])
    matrix.append(["Population de gammares"])
    matrix.append(["Feuilles Biotests alimentation - reprotoxicité"])
    matrix.append(["Survie 7 jours"])
    matrix.append(["Moyenne de survie Alim 1 à 4 / Nb par réplictats"])
    matrix.append(["Survie Alim 1"])
    matrix.append(["Survie Alim 2"])
    matrix.append(["Survie Alim 3"])
    matrix.append(["Survie Alim 4"])
    matrix.append(["Moyenne de survie Alim X ; Nb par réplictats"])
    matrix.append([""])
    matrix.append(["Critère de validité - survie globale"])
    matrix.append(["Critère de validité - réplicat 1 (+75% survie)"])
    matrix.append(["Critère de validité - réplicat 2 (+75% survie)"])
    matrix.append(["Critère de validité - réplicat 3 (+75% survie)"])
    matrix.append(["Critère de validité - réplicat 4 (+75% survie)"])
    matrix.append(["Alimentation"])
    matrix.append(["Taille pixels - X x Contrôle étalon mm/pxl "])
    matrix.append(["TAILLE MALE"])
    matrix.append(["Taille - Minimum (mm)"])
    matrix.append(["Taille - Maximum (mm)"])
    matrix.append(["Taille - Ecart type"])
    matrix.append(["Taille - coefficient de variation"])
    matrix.append(["Taille mm - 1 "])
    matrix.append(["Taille mm - 2"])
    matrix.append(["Taille mm - 3"])
    matrix.append(["Taille mm - 4"])
    matrix.append(["Taille mm - 5"])
    matrix.append(["Taille mm - 6"])
    matrix.append(["Taille mm - 7"])
    matrix.append(["Taille mm - 8"])
    matrix.append(["Taille mm - 9"])
    matrix.append(["Taille mm - 10"])
    matrix.append(["Taille mm - 11"])
    matrix.append(["Taille mm - 12"])
    matrix.append(["Taille mm - 13"])
    matrix.append(["Taille mm - 14"])
    matrix.append(["Taille mm - 15"])
    matrix.append(["Taille mm - 16"])
    matrix.append(["Taille mm - 17"])
    matrix.append(["Taille mm - 18"])
    matrix.append(["Taille mm - 19"])
    matrix.append(["Taille mm - 20"])
    matrix.append(["Contrôle étalon mm/pxl"])
    matrix.append(["Etalon taille mm /  Etalon taille pixel"])
    matrix.append([""])
    matrix.append(["Valeurs brutes réplicat 0 (pxl)"])
    matrix.append(["Somme des valeurs brutes pour 10 (témoin) / Nombre de disques (témoin)"])
    matrix.append(["Somme des valeurs brutes pour 20 (témoin)"])
    matrix.append([""])
    matrix.append(["Pixels consommés-réplicat 1"])
    matrix.append(["Pixels consommés-réplicat 2"])
    matrix.append(["Pixels consommés-réplicat 3"])
    matrix.append(["Pixels consommés-réplicat 4"])
    matrix.append(["Somme des valeurs brutes pour 20 (témoin) - Somme des valeurs pour réplicat X"])
    matrix.append(["Pixels consommés/jour/individu - réplicat 1"])
    matrix.append(["Pixels consommés/jour/individu - réplicat 2"])
    matrix.append(["Pixels consommés/jour/individu - réplicat 3"])
    matrix.append(["Pixels consommés/jour/individu - réplicat 4"])
    matrix.append(["mm² consommés/jour/individu - réplicat 1"])
    matrix.append(["mm² consommés/jour/individu - réplicat 2"])
    matrix.append(["mm² consommés/jour/individu - réplicat 3"])
    matrix.append(["mm² consommés/jour/individu - réplicat 4"])
    matrix.append(["MM² CONSOMMES/JOUR/INDIVIDU - MOYENNE"])
    matrix.append(["MM² CONSOMMES/JOUR/INDIVIDU - SD"])
    matrix.append([""])
    matrix.append(["TEMPERATURE MOYENNE (°C) ALIM"])
    matrix.append(["TEMPERATURE MIN (°C) in situ"])
    matrix.append(["TEMPERATURE MAX (°C) in situ"])
    matrix.append([""])
    matrix.append(["Valeur d'alimentation attendue"])
    matrix.append(["Constante alim 1 x TEMPERATURE MOYENNE + Constante alim 2 + Constante alim 3 x (TAILLE MALE - Constante 4)"])
    matrix.append(["% inhibition (FI) - Réplicat 1"])
    matrix.append(["% inhibition (FI) - Réplicat 2"])
    matrix.append(["% inhibition (FI) - Réplicat 3"])
    matrix.append(["% inhibition (FI) - Réplicat 4"])
    matrix.append(["% INHIBITION (FI) - MOY"])
    matrix.append(["% INHIBITION (FI) - SD"])
    matrix.append(["(Valeur d'alimentation attendue - mm² consommés/jour/individu rép X) / valeur d'alimentation attendue x 100"])
    matrix.append(["% INHIBITION (FI) - MOY"])
    matrix.append(["(Valeur d'alimentation attendue - mm² consommés/jour/individu rép X) x -1 / valeur d'alimentation attendue x 100 --> inhibition = résultat négatif"])
    matrix.append(["Nombre de réplicats pris en compte"])
    # matrix.append(["Seuils varient en fonction du nombre de réplicats pris en compte"])
    # matrix.append(["Résultat (en fonction des anciens seuils variables)"])
    # matrix.append(["Intensité"])
    # matrix.append(["Proba - Réplicat 1"])
    # matrix.append(["Proba - Réplicat 2"])
    # matrix.append(["Proba - Réplicat 3"])
    # matrix.append(["Proba - Réplicat 4"])
    # matrix.append(["logVraisemblance"])
    # matrix.append(["Nombre de réplicats pris en compte"])
    # matrix.append(["Seuils varient en fonction du nombre de réplicats pris en compte"])
    # matrix.append(["Résultat"])
    # matrix.append(["Intensité"])
    matrix.append([""])
    matrix.append(["Neurotoxicité - Activité AChE"])
    matrix.append(["Moyenne des masses"])
    matrix.append(["Masse - Ecart type"])
    matrix.append(["Masse - coefficient de variation"])
    matrix.append(["Activité AChE attendue (nmol/mon)"])
    matrix.append(["Activité AChE - Réplicat 1"])
    matrix.append(["Activité AChE - Réplicat 2"])
    matrix.append(["Activité AChE - Réplicat 3"])
    matrix.append(["Activité AChE - Réplicat 4"])
    matrix.append(["Activité AChE - Réplicat 5"])
    matrix.append(["Constante ache 1 x (Moyenne des masses ^ (Constante ache 2))"])
    matrix.append(["Activité AChE moyenne observée (nmol/min)"])
    matrix.append(["sd observé"])
    matrix.append(["Critère de qualité"])
    matrix.append(["Commentaires"])
    matrix.append(["% INHIBITION - AChE"])
    matrix.append(["% INHIBITION (AChE) - Resultat rendu"])
    matrix.append([" --> inhibition = résultat négatif"])
    # matrix.append(["Résultat"])
    matrix.append([""])
    matrix.append(["Reprotoxicité"])
    matrix.append([""])
    matrix.append(["Nombre de B-C1"])
    matrix.append(["Nombre de C2-D1"])
    matrix.append(["Nombre de D2"])
    matrix.append(["Nombre de femelles analysées"])
    matrix.append(["Distribution observée - B/C1"])
    matrix.append(["Distribution observée - C2/D1"])
    matrix.append(["Distribution observée - D2"])
    matrix.append(["Distribution attendue - B/C1"])
    matrix.append(["Distribution attendue - C2/D1"])
    matrix.append(["Distribution attendue - D2"])
    matrix.append(["Test unilatéral 5%"])
    matrix.append(["Test unilatéral 1%"])
    matrix.append(["1 seule femelle ?"])
    matrix.append([""])
    matrix.append(["indice de fertilité - moyenne"])
    matrix.append(["Nombre de femelles concernées"])
    matrix.append(["Nombre de femelles avec un stade de mue C2 ou D1 et avec des ovocytes"])
    matrix.append(["% INHIBITION - FERTILITE"])
    # matrix.append(["Seuil 5%"])
    # matrix.append(["Seuil 1%"])
    # matrix.append(["Résultat - Fertilité"])
    matrix.append(["indice de fertilité - femelle 1"])
    matrix.append(["indice de fertilité - femelle 2"])
    matrix.append(["indice de fertilité - femelle 3"])
    matrix.append(["indice de fertilité - femelle 4"])
    matrix.append(["indice de fertilité - femelle 5"])
    matrix.append(["indice de fertilité - femelle 6"])
    matrix.append(["indice de fertilité - femelle 7"])
    matrix.append(["indice de fertilité - femelle 8"])
    matrix.append(["indice de fertilité - femelle 9"])
    matrix.append(["indice de fertilité - femelle 10"])
    matrix.append(["indice de fertilité - femelle 11"])
    matrix.append(["indice de fertilité - femelle 12"])
    matrix.append(["indice de fertilité - femelle 13"])
    matrix.append(["indice de fertilité - femelle 14"])
    matrix.append(["indice de fertilité - femelle 15"])
    matrix.append(["Si std mue fem X = C2 ou D1 alors SI somme des ovocytes > 0 alors somme des ovocytes / taille fem X sinon """])
    matrix.append([""])
    matrix.append(["indice de fécondité - moyenne"])
    matrix.append(["Nombre de femelles concernées"])
    matrix.append(["Nombre de femelles avec un stade de mue C2 ou D1 et avec des ovocytes"])
    matrix.append(["% INHIBITION - FECONDITE"])
    matrix.append(["% INHIBITION FECONDITE - Resultat rendu"])
    # matrix.append(["Seuil 5% fécondité"])
    # matrix.append(["Seuil 1% fécondité"])
    # matrix.append(["Résultat - Fécondité"])
    matrix.append(["indice de fécondité - femelle 1"])
    matrix.append(["indice de fécondité - femelle 2"])
    matrix.append(["indice de fécondité - femelle 3"])
    matrix.append(["indice de fécondité - femelle 4"])
    matrix.append(["indice de fécondité - femelle 5"])
    matrix.append(["indice de fécondité - femelle 6"])
    matrix.append(["indice de fécondité - femelle 7"])
    matrix.append(["indice de fécondité - femelle 8"])
    matrix.append(["indice de fécondité - femelle 9"])
    matrix.append(["indice de fécondité - femelle 10"])
    matrix.append(["indice de fécondité - femelle 11"])
    matrix.append(["indice de fécondité - femelle 12"])
    matrix.append(["indice de fécondité - femelle 13"])
    matrix.append(["indice de fécondité - femelle 14"])
    matrix.append(["indice de fécondité - femelle 15"])
    matrix.append(["Si std emb fem X = 2 ou 3 ou 4 alors SI nombre embryons > 0 alors nombre embryons / (taille fem X - 5) sinon """])
    matrix.append([""])
    matrix.append(["Surface des retards - PE"])
    matrix.append(["surface des retards - femelle 1"])
    matrix.append(["surface des retards - femelle 2"])
    matrix.append(["surface des retards - femelle 3"])
    matrix.append(["surface des retards - femelle 4"])
    matrix.append(["surface des retards - femelle 5"])
    matrix.append(["surface des retards - femelle 6"])
    matrix.append(["surface des retards - femelle 7"])
    matrix.append(["surface des retards - femelle 8"])
    matrix.append(["surface des retards - femelle 9"])
    matrix.append(["surface des retards - femelle 10"])
    matrix.append(["surface des retards - femelle 11"])
    matrix.append(["surface des retards - femelle 12"])
    matrix.append(["surface des retards - femelle 13"])
    matrix.append(["surface des retards - femelle 14"])
    matrix.append(["surface des retards - femelle 15"])
    matrix.append(["surface des retards - moyenne"])
    matrix.append(["Nombre de femelles concernées"])
    matrix.append(["SEUIL UNILATERAL 5%"])
    matrix.append([""])
    matrix.append(["Surfaces C2D1 inhibition (%)"])
    matrix.append(["Seuil 5% surface C2-D1"])
    matrix.append(["Seuil 1% surface C2-D1"])
    matrix.append(["Résultat"])
    matrix.append(["Intensité"])
    matrix.append(["pourcentage d'inhibition surfaces C2 D1 - femelle 1"])
    matrix.append(["pourcentage d'inhibition surfaces C2 D1 - femelle 2"])
    matrix.append(["pourcentage d'inhibition surfaces C2 D1 - femelle 3"])
    matrix.append(["pourcentage d'inhibition surfaces C2 D1 - femelle 4"])
    matrix.append(["pourcentage d'inhibition surfaces C2 D1 - femelle 5"])
    matrix.append(["pourcentage d'inhibition surfaces C2 D1 - femelle 6"])
    matrix.append(["pourcentage d'inhibition surfaces C2 D1 - femelle 7"])
    matrix.append(["pourcentage d'inhibition surfaces C2 D1 - femelle 8"])
    matrix.append(["pourcentage d'inhibition surfaces C2 D1 - femelle 9"])
    matrix.append(["pourcentage d'inhibition surfaces C2 D1 - femelle 10"])
    matrix.append(["pourcentage d'inhibition surfaces C2 D1 - femelle 11"])
    matrix.append(["pourcentage d'inhibition surfaces C2 D1 - femelle 12"])
    matrix.append(["pourcentage d'inhibition surfaces C2 D1 - femelle 13"])
    matrix.append(["pourcentage d'inhibition surfaces C2 D1 - femelle 14"])
    matrix.append(["pourcentage d'inhibition surfaces C2 D1 - femelle 15"])
    matrix.append(["pourcentage moyen d'inhibition"])
    matrix.append(["Nombre de femelles concernées"])
    matrix.append(["écart centré réduit surfaces C2 D1 - femelle 1"])
    matrix.append(["écart centré réduit surfaces C2 D1 - femelle 2"])
    matrix.append(["écart centré réduit surfaces C2 D1 - femelle 3"])
    matrix.append(["écart centré réduit surfaces C2 D1 - femelle 4"])
    matrix.append(["écart centré réduit surfaces C2 D1 - femelle 5"])
    matrix.append(["écart centré réduit surfaces C2 D1 - femelle 6"])
    matrix.append(["écart centré réduit surfaces C2 D1 - femelle 7"])
    matrix.append(["écart centré réduit surfaces C2 D1 - femelle 8"])
    matrix.append(["écart centré réduit surfaces C2 D1 - femelle 9"])
    matrix.append(["écart centré réduit surfaces C2 D1 - femelle 10"])
    matrix.append(["écart centré réduit surfaces C2 D1 - femelle 11"])
    matrix.append(["écart centré réduit surfaces C2 D1 - femelle 12"])
    matrix.append(["écart centré réduit surfaces C2 D1 - femelle 13"])
    matrix.append(["écart centré réduit surfaces C2 D1 - femelle 14"])
    matrix.append(["écart centré réduit surfaces C2 D1 - femelle 15"])
    matrix.append([""])
    matrix.append(["taille femelle 1 - mm²"])
    matrix.append(["taille femelle 2 - mm²"])
    matrix.append(["taille femelle 3 - mm²"])
    matrix.append(["taille femelle 4 - mm²"])
    matrix.append(["taille femelle 5 - mm²"])
    matrix.append(["taille femelle 6 - mm²"])
    matrix.append(["taille femelle 7 - mm²"])
    matrix.append(["taille femelle 8 - mm²"])
    matrix.append(["taille femelle 9 - mm²"])
    matrix.append(["taille femelle 10 - mm²"])
    matrix.append(["taille femelle 11 - mm²"])
    matrix.append(["taille femelle 12 - mm²"])
    matrix.append(["taille femelle 13 - mm²"])
    matrix.append(["taille femelle 14 - mm²"])
    matrix.append(["taille femelle 15 - mm²"])
    matrix.append([""])
    matrix.append(["surface ovocytaire 1 - µm²"])
    matrix.append(["surface ovocytaire 2 - µm²"])
    matrix.append(["surface ovocytaire 3 - µm²"])
    matrix.append(["surface ovocytaire 4 - µm²"])
    matrix.append(["surface ovocytaire 5 - µm²"])
    matrix.append(["surface ovocytaire 6 - µm²"])
    matrix.append(["surface ovocytaire 7 - µm²"])
    matrix.append(["surface ovocytaire 8 - µm²"])
    matrix.append(["surface ovocytaire 9 - µm²"])
    matrix.append(["surface ovocytaire 10 - µm²"])
    matrix.append(["surface ovocytaire 11 - µm²"])
    matrix.append(["surface ovocytaire 12 - µm²"])
    matrix.append(["surface ovocytaire 13 - µm²"])
    matrix.append(["surface ovocytaire 14 - µm²"])
    matrix.append(["surface ovocytaire 15 - µm²"])
    matrix.append([""])
    matrix.append(["somme des ovocytes - femelle 1"])
    matrix.append(["somme des ovocytes - femelle 2"])
    matrix.append(["somme des ovocytes - femelle 3"])
    matrix.append(["somme des ovocytes - femelle 4"])
    matrix.append(["somme des ovocytes - femelle 5"])
    matrix.append(["somme des ovocytes - femelle 6"])
    matrix.append(["somme des ovocytes - femelle 7"])
    matrix.append(["somme des ovocytes - femelle 8"])
    matrix.append(["somme des ovocytes - femelle 9"])
    matrix.append(["somme des ovocytes - femelle 10"])
    matrix.append(["somme des ovocytes - femelle 11"])
    matrix.append(["somme des ovocytes - femelle 12"])
    matrix.append(["somme des ovocytes - femelle 13"])
    matrix.append(["somme des ovocytes - femelle 14"])
    matrix.append(["somme des ovocytes - femelle 15"])
    matrix.append([""])
    matrix.append(["Std embryo 1"])
    matrix.append(["Std embryo 2"])
    matrix.append(["Std embryo 3"])
    matrix.append(["Std embryo 4"])
    matrix.append(["Std embryo 5"])
    matrix.append(["Std embryo 6"])
    matrix.append(["Std embryo 7"])
    matrix.append(["Std embryo 8"])
    matrix.append(["Std embryo 9"])
    matrix.append(["Std embryo 10"])
    matrix.append(["Std embryo 11"])
    matrix.append(["Std embryo 12"])
    matrix.append(["Std embryo 13"])
    matrix.append(["Std embryo 14"])
    matrix.append(["Std embryo 15"])
    matrix.append(["Nombre de stade embryo 1 - 2"])
    matrix.append(["Nombre de stade embryo 3 - 4"])
    matrix.append(["Nombre de stade embryo 5"])
    matrix.append(["Nombre de femelles anaylsées"])
    matrix.append(["Pourcentage observé - 1/2"])
    matrix.append(["Pourcentage observé - 3/4"])
    matrix.append(["Pourcentage observé - 5"])
    matrix.append(["Pourcentage attendu - 1/2"])
    matrix.append(["Pourcentage attendu - 3/4"])
    matrix.append(["Pourcentage attendu - 5"])
    matrix.append(["Test unilatéral 5%"])
    matrix.append(["Test unilatéral 1%"])
    # matrix.append(["Résultat"])
    # matrix.append(["Intensité"])
    # matrix.append(["1 seule femelle ?"])

    cage_data, remaining_leaves_data, specimen_size_data, average_temperature_data, female_data, temperature_repro_data = get_tox_data(measurepoint_list, pack_list)
    reference_list = [["",""]]
    campaign_reference = ""
    count = 1
    for campaign_index, campaign_id in enumerate(campaign_dict):
        campaign_reference = campaign_list[campaign_index]
        for place_id in campaign_dict[campaign_id]["place"]:
            place_reference =  campaign_reference + "-" + ( "0" + str(campaign_dict[campaign_id]["place"][place_id]['number']) if campaign_dict[campaign_id]["place"][place_id]['number']<10 else str(campaign_dict[campaign_id]["place"][place_id]['number']))
            if 'duplicate' in campaign_dict[campaign_id]["place"][place_id] and ('alimentation' in campaign_dict[campaign_id]["place"][place_id]['duplicate'] or 'neurology' in campaign_dict[campaign_id]["place"][place_id]['duplicate'] or 'reproduction' in campaign_dict[campaign_id]["place"][place_id]['duplicate']):
                for measurepoint_id in campaign_dict[campaign_id]["place"][place_id]["measurepoint"]:
                    measurepoint_reference = place_reference +  "-" + ( "0" + str(campaign_dict[campaign_id]["place"][place_id]["measurepoint"][measurepoint_id]['number']) if campaign_dict[campaign_id]["place"][place_id]["measurepoint"][measurepoint_id]['number']<10 else str(campaign_dict[campaign_id]["place"][place_id]["measurepoint"][measurepoint_id]['number']))
                    reference_list.append([measurepoint_reference, measurepoint_id])   
                    matrix[0].append(J_dict[place_id]['J0']['truncated_date'])
                    matrix[1].append('CRE')
                    matrix[2].append('Lot ' + J_dict[place_id]['J0']['truncated_date'][-4:])
                    matrix = add_result(matrix, campaign_dict[campaign_id]["place"][place_id]["measurepoint"][measurepoint_id],measurepoint_id, cage_data, remaining_leaves_data, specimen_size_data, average_temperature_data, female_data, temperature_repro_data, constant_dict)
                    count +=1
                    matrix = fill_empty(matrix, count)
            else :
                matrix[0].append(J_dict[place_id]['J0']['truncated_date'])
                matrix[1].append('CRE')
                matrix[2].append('Lot ' + J_dict[place_id]['J0']['truncated_date'][-4:])
                reference_list.append([place_reference, place_id])
                matrix = add_result(matrix, campaign_dict[campaign_id]["place"][place_id],place_id, cage_data, remaining_leaves_data, specimen_size_data, average_temperature_data, female_data, temperature_repro_data, constant_dict)
                count += 1
                matrix = fill_empty(matrix, count)

    df = pd.DataFrame(matrix, columns=list(map(lambda x : x[0], reference_list)))
    return df

def fill_empty(matrix, count) :
    for row_index, row in enumerate(matrix):
        if len(row)<count :
            matrix[row_index].append("")
            return fill_empty(matrix,count)
    
    return matrix


def get_tox_data(measurepoint_list, pack_list) :
    pack_tuple = tuple(pack_list) if len(pack_list)>1  else "('"+str(pack_list[0])+"')"
    measurepoint_tuple = tuple(measurepoint_list) if len(measurepoint_list)>1  else "('"+str(measurepoint_list[0])+"')"
    
    cage_data = QueryScript(f"SELECT pack_id, replicate, scud_quantity, scud_survivor, weight, ache, nature FROM {env.DATABASE_RAW}.Cage WHERE pack_id IN  {pack_tuple}").execute()
    remaining_leaves_data =  QueryScript(f"SELECT pack_id, replicate, value   FROM {env.DATABASE_RAW}.MeasureLeaf WHERE pack_id IN {pack_tuple}").execute()
    specimen_size_data =  QueryScript(f"  SELECT pack_id, individual, size_px, size_mm   FROM {env.DATABASE_RAW}.MeasureSize WHERE pack_id IN {pack_tuple}").execute()
    average_temperature_data = QueryScript(f" SELECT measurepoint_id, sensor1_average, sensor1_min, sensor1_max  FROM {env.DATABASE_TREATED}.average_temperature WHERE measurepoint_id IN {measurepoint_tuple} AND version=  {env.CHOSEN_VERSION()}").execute()
    female_data = QueryScript(f"SELECT pack_id, female, molting_stage, oocyte_left, oocyte_right, specimen_size_px, specimen_size_mm, embryo_total, embryo_stage, oocyte_area_pixel, oocyte_area_mm FROM {env.DATABASE_RAW}.MeasureReprotoxicity").execute()
    temperature_repro_data =  QueryScript(f"SELECT measurepoint_id, expected_C2, expected_D2 FROM {env.DATABASE_TREATED}.temperature_repro WHERE version={env.CHOSEN_VERSION()}").execute()

    return cage_data, remaining_leaves_data, specimen_size_data, average_temperature_data, female_data, temperature_repro_data

def standard_deviation(liste) :
    if len(liste) == 0 :
        return None
    average = sum(liste)/len(liste)
    deviation = 0
    for element in liste :
        deviation += (element - average)**2
    return (deviation/len(liste))**(0.5)

def add_result(matrix, place_or_seperated_measurepoint, place_or_measurepoint_id, cage_data, remaining_leaves_data, specimen_size_data, average_temperature_data, female_data, temperature_repro_data, constant_dict):
    is_place = False
    if 'measurepoint' in place_or_seperated_measurepoint :
        is_place = True
    new_matrix = matrix
    alimentation_measurepoint_id = None
    neurology_measurepoint_id = None
    reproduction_measurepoint_id = None

    alimentation_pack_id = None
    neurology_pack_id = None
    reproduction_pack_id = None

    ### get biotest pack and measurepoint id

    if is_place :
        for measurepoint_id in place_or_seperated_measurepoint['measurepoint'] :
            for pack_id in place_or_seperated_measurepoint['measurepoint'][measurepoint_id]['pack'] :
                if place_or_seperated_measurepoint['measurepoint'][measurepoint_id]['pack'][pack_id] == 'alimentation':
                    alimentation_measurepoint_id = measurepoint_id
                    alimentation_pack_id = pack_id
                if place_or_seperated_measurepoint['measurepoint'][measurepoint_id]['pack'][pack_id] == 'neurology':
                    neurology_measurepoint_id = measurepoint_id
                    neurology_pack_id = pack_id
                if place_or_seperated_measurepoint['measurepoint'][measurepoint_id]['pack'][pack_id] == 'reproduction':
                    reproduction_measurepoint_id = measurepoint_id
                    reproduction_pack_id = pack_id
    else : 
        for pack_id in place_or_seperated_measurepoint['pack'] :
            if place_or_seperated_measurepoint['pack'][pack_id] == 'alimentation':
                alimentation_measurepoint_id = place_or_measurepoint_id
                alimentation_pack_id = pack_id
            if place_or_seperated_measurepoint['pack'][pack_id] == 'neurology':
                neurology_measurepoint_id = place_or_measurepoint_id
                neurology_pack_id = pack_id
            if place_or_seperated_measurepoint['pack'][pack_id] == 'reproduction':
                reproduction_measurepoint_id = place_or_measurepoint_id
                reproduction_pack_id = pack_id
    
    ############# ALIMENTATION

    if alimentation_pack_id :

        ### Survivor
        
        survior_replicate_list = []
        scud_quantity_alim = None
        for pack_id, replicate, scud_quantity, scud_survivor, _, _, nature in cage_data:
            if alimentation_pack_id and alimentation_pack_id==pack_id and nature=='alimentation':
                if scud_survivor!=None and scud_quantity :
                    scud_quantity_alim = scud_quantity
                    new_matrix[4+replicate].append((scud_quantity+scud_survivor)/2)
                    survior_replicate_list.append(scud_survivor)
                    if (scud_quantity+scud_survivor)/2/scud_quantity>0.75 :
                        new_matrix[11+replicate].append("OK")
                    else :
                        new_matrix[11+replicate].append("NON")
        if len(survior_replicate_list) :
            new_matrix[3].append(round(sum(survior_replicate_list)/len(survior_replicate_list)/scud_quantity_alim*100,1))
            if sum(survior_replicate_list)/len(survior_replicate_list) > 0.75 :
                new_matrix[11].append("OK")
            else :
                new_matrix[11].append("NON")

        size_px_individual_list = [None] * 20
        size_mm_individual_list = [None] * 20
        size_list = []
        ratio = None

        ### Size 
        for pack_id, individual, size_px, size_mm in specimen_size_data:
            individual=int(individual)
            if alimentation_pack_id and alimentation_pack_id==pack_id:
                if size_px and size_mm :
                    ratio = size_mm/size_px
                elif size_px and individual!=0 :
                    size_px_individual_list[individual-1] = size_px
                if size_mm and individual!=0 :
                    size_mm_individual_list[individual-1] = size_mm
                    size_list.append(size_mm)

        if ratio : 
            for index, size in enumerate(size_px_individual_list) : 
                if size :
                    size_mm_individual_list[index] = size*ratio
                    size_list.append(size*ratio)

                
        not_None_individual_size = 0
        individual_size_sum = 0
        for individual_size in size_mm_individual_list:
            if individual_size : 
                individual_size_sum += individual_size
                not_None_individual_size +=1
        individual_size_average = individual_size_sum/not_None_individual_size if not_None_individual_size else None
        
        if not_None_individual_size:
            new_matrix[18].append(individual_size_average)
            new_matrix[19].append(min(size_list))
            new_matrix[20].append(max(size_list))
            if standard_deviation(size_list) :
                new_matrix[21].append(standard_deviation(size_list))
                new_matrix[22].append(standard_deviation(size_list)/individual_size_average)
            for index, size in enumerate(size_mm_individual_list):
                new_matrix[23+index].append(size)
            if ratio:
                new_matrix[43].append(ratio)

        ### leaf size

        standard_raw_value_in_px = None
        for pack_id, replicate, value in remaining_leaves_data :
            if pack_id == alimentation_pack_id :
                if replicate == 0:
                    standard_raw_value_in_px = value / constant_dict["Nombre de disques (témoin)"]
        replicate_eaten_surface_list = []
        if standard_raw_value_in_px :
            new_matrix[46].append(standard_raw_value_in_px)
            raw_value_sum = standard_raw_value_in_px * constant_dict["Nombre de disques par réplicat"]
            if raw_value_sum : 
                new_matrix[48].append(raw_value_sum)
                for pack_id, replicate, value in remaining_leaves_data :
                    if alimentation_pack_id == pack_id :
                        if replicate != 0 and value:
                            new_matrix[49+replicate].append(raw_value_sum - value)
                            if len(survior_replicate_list)>=replicate and survior_replicate_list[replicate-1]:
                                new_matrix[54+replicate].append((raw_value_sum - value)/(survior_replicate_list[replicate-1]+scud_quantity_alim)*2/constant_dict["Nombre de jour du test"])       
                                new_matrix[58+replicate].append((raw_value_sum - value)/(survior_replicate_list[replicate-1]+scud_quantity_alim)*2/constant_dict["Nombre de jour du test"]*0.0071)       
                                replicate_eaten_surface_list.append((raw_value_sum - value)/(survior_replicate_list[replicate-1]+scud_quantity_alim)*2/constant_dict["Nombre de jour du test"]*0.0071)                    
        if len(replicate_eaten_surface_list):
            new_matrix[63].append(sum(replicate_eaten_surface_list)/len(replicate_eaten_surface_list))
            new_matrix[64].append(standard_deviation(replicate_eaten_surface_list))

        average_temperature = None
        for measurepoint_id, sensor1_average, sensor1_min, sensor1_max in average_temperature_data :
            if alimentation_measurepoint_id and measurepoint_id == alimentation_measurepoint_id :
                average_temperature = sensor1_average
                new_matrix[66].append(sensor1_average)    
                new_matrix[67].append(sensor1_min)    
                new_matrix[68].append(sensor1_max)    

        inhibition_list = []
        inhibition_average = None
        if average_temperature and individual_size_average :
            standard_eaten_value  = constant_dict["Constante alim 1"]*average_temperature + constant_dict["Constante alim 2"] + constant_dict["Constante alim 3"] * (individual_size_average - constant_dict["Constante alim 4"])
            new_matrix[70].append(standard_eaten_value)
            for index, surface in enumerate(replicate_eaten_surface_list) :
                inhibition = ( standard_eaten_value - surface ) / standard_eaten_value * 100
                inhibition_list.append(inhibition)
                new_matrix[72+index].append(inhibition)
            if len(inhibition_list) :
                inhibition_average = sum(inhibition_list)/len(inhibition_list)
                new_matrix[76].append(inhibition_average)
                new_matrix[77].append(standard_deviation(inhibition_list))
                new_matrix[79].append(-inhibition_average)
                new_matrix[81].append(len(inhibition_list))


    ########## NEUROLOGY

    if neurology_pack_id :
        weight_list = []
        ache_list = []
        for pack_id, replicate, _, _, weight, ache, nature in cage_data :
            
            if pack_id == neurology_pack_id  and nature=='neurology':
                if weight :
                    weight_list.append(weight)
                if ache :
                    ache_list.append(ache)
                    new_matrix[87+int(replicate)].append(ache)
        
        standard_ache_activity = None
        if len(weight_list) :
            new_matrix[84].append(sum(weight_list)/len(weight_list))
            new_matrix[85].append(standard_deviation(weight_list))
            new_matrix[86].append(standard_deviation(weight_list)/(sum(weight_list)/len(weight_list)))
            
            standard_ache_activity = constant_dict["Constante ache 1"] + constant_dict["Constante ache 2"] * sum(weight_list)/len(weight_list) ** constant_dict["Constante ache 3"]
            new_matrix[87].append(standard_ache_activity)

        if len(ache_list) :
            ache_average = sum(ache_list)/len(ache_list)
            new_matrix[94].append(ache_average)
            new_matrix[95].append(standard_deviation(ache_list))
            if standard_deviation(ache_list) > constant_dict["Seuil de qualité"] :
                new_matrix[96].append("NON")
            else :
                new_matrix[96].append("OK")

            if standard_ache_activity :
                inhibition = ( standard_ache_activity - ache_average ) / standard_ache_activity * 100
                new_matrix[98].append(inhibition)
                new_matrix[99].append(-inhibition)
        
        if len(ache_list) < 5 or len(weight_list) < 5 :
            new_matrix[97].append("Moins de 5 replicats") 

    ######### FECONDITY

    if reproduction_pack_id :
        size_ratio = None
        female_count = 0
        female_b_or_c1_count = 0
        female_c2_or_d1_count = 0
        female_d2_count = 0
        for pack_id, female, molting_stage, oocyte_left, oocyte_right, specimen_size_px, speciment_size_mm, embryo_total, embryo_stage, _, _ in female_data :
            if pack_id == reproduction_pack_id and female!="" and int(female)!=0 and molting_stage: 

                if molting_stage == 'b' or molting_stage == 'c1' :
                    # if oocyte_area_pixel :
                    #     if int(female)<=15 :
                    #         new_matrix[156+int(female)].append(oocyte_area_pixel/0.206)
                    female_b_or_c1_count += 1
                if molting_stage == 'c2' or molting_stage == 'd1' :
                    female_c2_or_d1_count += 1
                if molting_stage == 'd2' :
                    female_d2_count += 1
                female_count += 1
                # if oocyte_area_pixel :
                #     if int(female)<=15 :
                #         new_matrix[230+int(female)].append(oocyte_area_pixel/0.206)
            
            elif pack_id == reproduction_pack_id and female=="0" :
                if specimen_size_px and speciment_size_mm :
                    size_ratio = speciment_size_mm/specimen_size_px
            
        new_matrix[104].append(female_b_or_c1_count)
        new_matrix[105].append(female_c2_or_d1_count)
        new_matrix[106].append(female_d2_count)
        new_matrix[107].append(female_count)

        if female_count :
            new_matrix[108].append(female_b_or_c1_count/female_count*100)
            new_matrix[109].append(female_c2_or_d1_count/female_count*100)
            new_matrix[110].append(female_d2_count/female_count*100)

        if reproduction_measurepoint_id :
            for measurepoint_id, expected_C2, expected_D2 in temperature_repro_data :
                if measurepoint_id == reproduction_measurepoint_id and expected_C2 and expected_D2 :
                    new_matrix[111].append(100 - expected_C2)
                    new_matrix[112].append(expected_C2 - expected_D2)
                    new_matrix[113].append(expected_D2)
                    new_matrix[114].append(Reprotoxicity.binom_inv(female_count, (100 - expected_C2)/100, 0.95 ))
                    new_matrix[115].append(Reprotoxicity.binom_inv(female_count, (100 - expected_C2)/100, 0.99 ))
                    if female_b_or_c1_count == 1 :
                        new_matrix[116].append("1 fem !!!")
            
            fertility_list = []
            female_size_list = [None] * 16 
            for pack_id, female, molting_stage, oocyte_left, oocyte_right, specimen_size_px, specimen_size_mm, _, _, _, _ in female_data :
                if pack_id == reproduction_pack_id and female!="" and int(female)>0 and int(female)<=15 :
                    female = int(female) if female else 0
                    if specimen_size_mm and specimen_size_mm!="0" :
                        female_size_list[female] = specimen_size_mm
                        new_matrix[218+female].append(specimen_size_mm)
                        if (molting_stage == 'c2' or molting_stage == 'd1') and oocyte_left!=None and oocyte_right!=None and oocyte_left+oocyte_right>0 :
                            new_matrix[121+female].append((oocyte_left+oocyte_right)/specimen_size_mm)
                            fertility_list.append((oocyte_left+oocyte_right)/specimen_size_mm)
                    elif size_ratio and specimen_size_px :
                        female_size_list[female] = specimen_size_px*size_ratio
                        new_matrix[218+female].append(specimen_size_px*size_ratio)
                        if oocyte_left!=None and oocyte_right!=None and oocyte_left+oocyte_right>0 and (molting_stage == 'c2' or molting_stage == 'd1') :
                            new_matrix[121+female].append((oocyte_left+oocyte_right)/(specimen_size_px*size_ratio))
                            fertility_list.append((oocyte_left+oocyte_right)/female_size_list[female])

            if len(fertility_list) >= 1 and female_count>=10 :
                fertility_average = sum(fertility_list)/len(fertility_list)
                new_matrix[118].append(fertility_average)
                new_matrix[119].append(len(fertility_list))
                new_matrix[121].append((constant_dict["indice de fertilité attendu - moyenne-1"] - fertility_average)/constant_dict["indice de fertilité attendu - moyenne-1"]*100)
            
            else : 
                new_matrix[118].append("NA")
                new_matrix[119].append("<10")


            fecondity_list = []
            embryo_stage_list = [] 
            embryo_stage_1_2_count = 0
            embryo_stage_3_4_count = 0
            embryo_stage_5_count = 0
            embryo_stage_count = 0
            for pack_id, female, molting_stage, oocyte_left, oocyte_right, specimen_size_px, specimen_size_mm, embryo_total, embryo_stage, _, _ in female_data :
                if pack_id == reproduction_pack_id and embryo_stage in [2,3,4] and female!="" and int(female)<=15 :
                    female = int(female) if female else 0
                    new_matrix[250+female].append(oocyte_left+oocyte_right)
                    new_matrix[266+female].append(embryo_stage)
                    embryo_stage_list.append(embryo_stage)
                    if embryo_stage in [1,2]:
                        embryo_stage_1_2_count += 1 
                    if embryo_stage in [3,4]:
                        embryo_stage_3_4_count += 1
                    if embryo_stage in [5]:
                        embryo_stage_5_count += 1 
                    if female>0 and len(female_size_list)>female and female_size_list[female] and embryo_total :
                        fecondity_list.append(embryo_total/(female_size_list[female] - 5))
                        new_matrix[143+female].append(embryo_total/(female_size_list[female] - 5))
            if len(fecondity_list) >= 1 and female_count>=10 :
                fecondity_average = sum(fecondity_list)/len(fecondity_list)
                new_matrix[139].append(fecondity_average)
                new_matrix[140].append(len(fecondity_list))
                new_matrix[141].append((constant_dict["indice de fertilité attendu - moyenne"] - fecondity_average)/constant_dict["indice de fertilité attendu - moyenne"]*100)
                new_matrix[142].append(-(constant_dict["indice de fertilité attendu - moyenne"] - fecondity_average)/constant_dict["indice de fertilité attendu - moyenne"]*100)
            else : 
                new_matrix[139].append("NA")
                new_matrix[140].append("<10")

            surface_list = []
            surface_inhibition_list = []
            surface_reduced_list = []
            for pack_id, female, molting_stage, _, _, _, _, _, _, oocyte_area_pixel, oocyte_area_mm in female_data :
                if pack_id == reproduction_pack_id:
                    if female and int(female)>0 and int(female)<=15 :
                        if not oocyte_area_mm and oocyte_area_pixel and size_ratio :
                            oocyte_area_mm = oocyte_area_pixel
                        if oocyte_area_mm :
                            new_matrix[234+int(female)].append(oocyte_area_mm)
                            if molting_stage=="c1" or molting_stage=="b" :
                                new_matrix[161+int(female)].append(oocyte_area_mm)
                                surface_list.append(oocyte_area_mm)
                            if molting_stage=="c2" :
                                new_matrix[185+int(female)].append((oocyte_area_mm-constant_dict["Moyenne des surfaces de référence C2"])/constant_dict["Moyenne des surfaces de référence C2"]*(-100))
                                new_matrix[202+int(female)].append((oocyte_area_mm-constant_dict["Moyenne des surfaces de référence C2"])/constant_dict["SD des surfaces de référence C2"])
                                surface_inhibition_list.append((oocyte_area_mm-constant_dict["Moyenne des surfaces de référence C2"])/constant_dict["Moyenne des surfaces de référence C2"]*(-100))
                                surface_reduced_list.append((oocyte_area_mm-constant_dict["Moyenne des surfaces de référence C2"])/constant_dict["SD des surfaces de référence C2"])
                            if molting_stage=="d1" :
                                new_matrix[185+int(female)].append((oocyte_area_mm-constant_dict["Moyenne des surfaces de référence D1"])/constant_dict["Moyenne des surfaces de référence D1"]*(-100))
                                new_matrix[202+int(female)].append((oocyte_area_mm-constant_dict["Moyenne des surfaces de référence D1"])/constant_dict["SD des surfaces de référence D1"])
                                surface_inhibition_list.append((oocyte_area_mm-constant_dict["Moyenne des surfaces de référence D1"])/constant_dict["Moyenne des surfaces de référence D1"]*(-100))
                                surface_reduced_list.append((oocyte_area_mm-constant_dict["Moyenne des surfaces de référence D1"])/constant_dict["SD des surfaces de référence D1"])
            if len(surface_list) :
                new_matrix[177].append(sum(surface_list)/len(surface_list))
                new_matrix[178].append(len(surface_list))
                new_matrix[179].append(constant_dict["Moyenne des surfaces de référence C2"]-constant_dict["Constante surface des retards 1"]*constant_dict["SD des surfaces de référence C2"]/len(surface_list)**0.5)
                if len(surface_inhibition_list):
                    new_matrix[201].append(sum(surface_inhibition_list)/len(surface_inhibition_list))
                    new_matrix[202].append(len(surface_inhibition_list))
                if len(surface_reduced_list) :
                    C2D1_inhibition = sum(surface_reduced_list)/len(surface_reduced_list)
                    new_matrix[181].append(C2D1_inhibition)
                    threshold_1 = -constant_dict["Constante 1 surface C2 D1"]/len(surface_inhibition_list)
                    threshold_2 = -constant_dict["Constante 2 surface C2 D1"]/len(surface_inhibition_list)
                    new_matrix[182].append(threshold_1)
                    new_matrix[183].append(threshold_2)
                    new_matrix[184].append("Inhibition" if C2D1_inhibition<threshold_1 else "Conforme")
                    if C2D1_inhibition<threshold_1 :
                        new_matrix[185].append("forte" if C2D1_inhibition<threshold_2  else "modéré")
                    

            if len(embryo_stage_list) :
                new_matrix[282].append(embryo_stage_1_2_count)
                new_matrix[283].append(embryo_stage_3_4_count)
                new_matrix[284].append(embryo_stage_5_count)    
                new_matrix[285].append(len(embryo_stage_list))
                new_matrix[286].append(embryo_stage_1_2_count/len(embryo_stage_list)*100)
                new_matrix[287].append(embryo_stage_3_4_count/len(embryo_stage_list)*100)
                new_matrix[288].append(embryo_stage_5_count/len(embryo_stage_list)*100)
                new_matrix[292].append(Reprotoxicity.binom_inv(len(embryo_stage_list),embryo_stage_1_2_count/len(embryo_stage_list) /100, 0.95 ))
                new_matrix[293].append(Reprotoxicity.binom_inv(len(embryo_stage_list),embryo_stage_1_2_count/len(embryo_stage_list) /100, 0.99 ))

    return new_matrix
