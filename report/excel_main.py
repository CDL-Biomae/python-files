from report.xl import *
from report.style import *
from report.initialization import create_campaigns_dict, initialize_lists, create_head_dataframe, create_head_special_dataframe
from calcul import chemistry
import pandas as pd
from termcolor import colored
from openpyxl import load_workbook
import env


def create_filename(list_campaigns):
    '''
    Créé un nom de fichier à partir d'une liste de campagnes
    :param list_campaigns: ex: ['AG-003-01', 'AG-003-02']
    :return: filename: 'Rapport_pour_AG-003-01_AG-003-02.xlsx'
    '''
    filename = 'Rapport_pour'
    for c in list_campaigns:
        filename += f"_{c}"
    filename += '.xlsx'

    return filename


def write_in_new_excel(dataframe, filename, folder_PATH, sheet, startcol=1, startrow=1):
    '''
    Créé un nouveau fichier excel et rempli un onglet avec des données
    :param dataframe: données
    :param filename: nom du fichier
    :param folder_PATH: chemin vers le fichier
    :param sheet: nom de l'onglet
    :param startcol: colonne de démarrage de l'écriture
    :param startrow:  ligne de démarrage de l'écriture
    '''
    PATH = f"{folder_PATH}\\{filename}"
    writer = pd.ExcelWriter(path=PATH, engine='openpyxl')
    dataframe.to_excel(writer, sheet_name=f"{sheet}", index=False, startcol=startcol, startrow=startrow)
    writer.save()
    writer.close()
    print(
        f"L'onglet \"{sheet}\" a été créé dans le nouveau fichier \"{filename}\"")


def write_in_existing_excel(dataframe, filename, folder_PATH, sheet, startcol=1, startrow=1):
    '''
    Ajoute un onglet avec des données dans un fichier excel existant
    :param dataframe: données
    :param filename: nom du fichier
    :param folder_PATH: chemin vers le fichier
    :param sheet: nom de l'onglet
    :param startcol: colonne de démarrage de l'écriture
    :param startrow:  ligne de démarrage de l'écriture
    '''
    PATH = f"{folder_PATH}\\{filename}"
    book = load_workbook(PATH)
    writer = pd.ExcelWriter(path=PATH, engine='openpyxl')
    writer.book = book
    dataframe.to_excel(writer, sheet_name=f"{sheet}", index=False, startcol=startcol, startrow=startrow)
    writer.save()
    writer.close()
    print(f"L'onglet \"{sheet}\" a été créé dans le fichier \"{filename}\"")


## MAIN FUNCTION ##


def excel_main(list_campaigns, folder_PATH = "output"):
    '''
    Créé un fichier excel annexe pour le rapport d'étude
    :param list_campaigns: ex: ['AG-003-01', 'AG-003-02']
    :param folder_PATH:
    :return:
    '''
    filename = create_filename(list_campaigns)
    print('[+] Starting initialisation...')
    
    campaigns_dict = create_campaigns_dict(references=list_campaigns)
    campaigns_dict, measurepoint_list, chemistry_measurepoint_list, chemistry_pack_list, chemistry_7j_measurepoint_list, chemistry_21j_measurepoint_list, tox_measurepoint_list, agency_code_list, J_dict = initialize_lists(campaigns_dict)
    head_dataframe, head_filtered_dataframe, place_list = create_head_dataframe(campaigns_dict)
    head_chemistry_dataframe, head_chemistry_7j_dataframe, head_chemistry_21j_dataframe, head_tox_dataframe =  create_head_special_dataframe(campaigns_dict, chemistry_measurepoint_list, chemistry_7j_measurepoint_list, chemistry_21j_measurepoint_list, tox_measurepoint_list)

    # ## CREATION DE L'ONGLET VERSION ##

    print('\n[!] Création de l\'onglet \"Version\"...')
    version_dataframe = create_version_dataframe()
    write_in_new_excel(version_dataframe, filename, folder_PATH, 'Version', startrow=3)
    add_style_version(version_dataframe, list_campaigns, filename, folder_PATH)

    ## CREATION DE L'ONGLET STATIONS ##

    print('\n[!] Création de l\'onglet \"Stations\"...')
    stations_dataframe = create_stations_dataframe(head_filtered_dataframe, campaigns_dict, measurepoint_list, agency_code_list, place_list)
    write_in_existing_excel(stations_dataframe, filename, folder_PATH, 'Stations')
    add_style_stations(stations_dataframe, filename, folder_PATH)

    ## CREATION DE L'ONGLET CAMPAGNES ##

    print('\n[!] Création de l\'onglet \"Campagnes\"...')
    campagnes_dataframe = create_campagnes_dataframe(head_dataframe, campaigns_dict, J_dict)
    write_in_existing_excel(campagnes_dataframe, filename, folder_PATH, 'Campagnes')
    add_style_campagnes(campagnes_dataframe, filename, folder_PATH)

    ## CREATION DE L'ONGLET SURVIE ##

    if len(chemistry_pack_list):
        print('\n[!] Création de l\'onglet \"Survie\"...')
        survie_dataframe = create_survie_dataframe(campaigns_dict, chemistry_measurepoint_list)
        write_in_existing_excel(survie_dataframe, filename, folder_PATH, 'Survie', startcol=2, startrow=2)
        add_style_survie(survie_dataframe, filename, folder_PATH)


    ## CREATION DE L'ONGLET PHYSICO-CHIMIE ##
    if len(measurepoint_list) :
        print('\n[!] Création de l\'onglet \"Physico-chimie\"...')
        physicochimie_dataframe = create_physicochimie_dataframe(head_dataframe, measurepoint_list, campaigns_dict, J_dict)
        write_in_existing_excel(physicochimie_dataframe, filename, folder_PATH, 'Physico-chimie_refChimie', startrow=2)
        write_in_existing_excel(physicochimie_dataframe, filename, folder_PATH, 'Physico-chimie_refToxicité', startrow=2)
        add_style_physicochimie(physicochimie_dataframe, filename, folder_PATH)

    # CREATION DE L'ONGLET BBAC ##


    
    if len(chemistry_pack_list):
        result_dict = chemistry.result(campaigns_dict, chemistry_pack_list)
        t0_associated = QueryScript(f"SELECT code_t0_id, id  FROM {env.DATABASE_RAW}.Measurepoint WHERE id IN {tuple(chemistry_measurepoint_list)};").execute()
        dict_t0 = {}
        for campaign_id in campaigns_dict:
            for place_id in campaigns_dict[campaign_id]["place"]:
                for measurepoint_id in campaigns_dict[campaign_id]["place"][place_id]["measurepoint"]:
                    for code_t0_id, mp_id in t0_associated:
                        if measurepoint_id==mp_id and place_id not in dict_t0:
                            dict_t0[measurepoint_id] = {"code_t0_id": code_t0_id}
        if len(chemistry_7j_measurepoint_list):
            print('\n[!] Création de l\'onglet \"BBAC 7j\"...')
            bbac_dataframe = create_bbac_7j_dataframe(head_chemistry_7j_dataframe, result_dict, chemistry_7j_measurepoint_list)
            bbac2_dataframe = create_bbac2_7j_dataframe(head_chemistry_7j_dataframe, result_dict, chemistry_7j_measurepoint_list)
            write_in_existing_excel(bbac_dataframe, filename, folder_PATH, 'BBAC_7j', startrow=3)
            write_in_existing_excel(bbac2_dataframe, filename, folder_PATH, 'BBAC2_7j', startrow=3)
            add_style_bbac_7j(bbac_dataframe, filename, folder_PATH, dict_t0)
        if len(chemistry_21j_measurepoint_list):
            print('\n[!] Création de l\'onglet \"BBAC 21j\"...')
            bbac_dataframe = create_bbac_21j_dataframe(head_chemistry_21j_dataframe, result_dict, chemistry_21j_measurepoint_list)
            bbac2_dataframe = create_bbac2_21j_dataframe(head_chemistry_21j_dataframe, result_dict, chemistry_21j_measurepoint_list)
            write_in_existing_excel(bbac_dataframe, filename, folder_PATH, 'BBAC_21j', startrow=3)
            write_in_existing_excel(bbac2_dataframe, filename, folder_PATH, 'BBAC2_21j', startrow=3)
            add_style_bbac_21j(bbac_dataframe, filename, folder_PATH, dict_t0)

        # CREATION DE L'ONGLET NQE ##

        print('\n[!] Création de l\'onglet \"NQE Biote\"...')
        nqe_dataframe = create_nqe_dataframe(head_chemistry_dataframe, result_dict, chemistry_measurepoint_list)
        write_in_existing_excel(nqe_dataframe, filename, folder_PATH, 'NQE Biote', startrow=3)
        add_style_nqe(nqe_dataframe, filename, folder_PATH, dict_t0)
    else:
        print('\n[!] Pas de chimie détectée ! ')

    ## CREATION DE L'ONGLET TOX ##
    if len(tox_measurepoint_list):
        print('\n[!] Création de l\'onglet \"Tox\"...')
        tox_dataframe = create_tox_dataframe(campaigns_dict, tox_measurepoint_list)
        write_in_existing_excel(tox_dataframe, filename, folder_PATH, 'Tox', startrow=3)
        add_style_tox(tox_dataframe, filename, folder_PATH)
    else :
        print('\n[!] Pas de tox détectée ! ')


    print(colored('\n --> Rapport terminé', 'green'))


