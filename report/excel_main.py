from report import *
from database import get_dict_pack_fusion
import pandas as pd
from termcolor import colored
from openpyxl import load_workbook
import env


def create_filename(list_campaigns):
    filename = 'Rapport_pour'
    for c in list_campaigns:
        filename += f"_{c}"
    filename += '.xlsx'

    return filename


def write_in_new_excel(dataframe, filename, folder_PATH, sheet, startcol=1, startrow=1):
    PATH = f"{folder_PATH}\\{filename}"
    writer = pd.ExcelWriter(path=PATH, engine='openpyxl')
    dataframe.to_excel(writer, sheet_name=f"{sheet}", index=False, startcol=startcol, startrow=startrow)
    writer.save()
    writer.close()
    print(
        f"L'onglet \"{sheet}\" a été créé dans le nouveau fichier \"{filename}\"")


def write_in_existing_excel(dataframe, filename, folder_PATH, sheet, startcol=1, startrow=1):
    PATH = f"{folder_PATH}\\{filename}"
    book = load_workbook(PATH)
    writer = pd.ExcelWriter(path=PATH, engine='openpyxl')
    writer.book = book
    dataframe.to_excel(writer, sheet_name=f"{sheet}", index=False, startcol=startcol, startrow=startrow)
    writer.save()
    writer.close()
    print(f"L'onglet \"{sheet}\" a été créé dans le fichier \"{filename}\"")


def measure_points_fusion(campaign_ref):
     
    output = QueryScript(
        f" SELECT DISTINCT(measurepoint_fusion_id)   FROM {env.DATABASE_TREATED}.key_dates WHERE measurepoint_id IN (  SELECT id   FROM {env.DATABASE_RAW}.measurepoint WHERE reference LIKE '{campaign_ref}%' and version={env.VERSION});"
    )
    return output.execute()

def all_measure_points(campaign_ref):
    output = QueryScript(
        f"  SELECT id   FROM {env.DATABASE_RAW}.measurepoint WHERE reference LIKE '{campaign_ref}%';"
    )
    return output.execute()

def create_dict_mp2(list_campaigns):
    dict = {}
    for c in list_campaigns:
        list_mp = all_measure_points(c)
        dict[c] = list_mp
    return dict

def create_dict_mp(list_campaigns):
    dict = {}
    for c in list_campaigns:
        list_mp = measure_points_fusion(c)
        dict[c] = list_mp
    return dict

def create_general_dict(list_campaigns):
    result = {}
    for campaign in list_campaigns:
        result.update(get_dict_pack_fusion(campaign))
    return result

## MAIN FUNCTION ##


def excel_main(list_campaigns, folder_PATH = "output"):  # Prend en entrée une liste de reference de campagne, ex: ['AG-003-01', 'AG-003-02'] et
    filename = create_filename(list_campaigns)
    print('[+] Starting initialisation...')
    head_dataframe = create_head_dataframe(list_campaigns)
    # print(head_dataframe.head())
    dict_mp = create_dict_mp(list_campaigns)

    # create_tox_dataframe(head_dataframe, list_campaigns, dict_mp)

    # ## CREATION DE L'ONGLET VERSION ##

    print('\n[!] Création de l\'onglet \"Version\"...')
    version_dataframe = create_version_dataframe()
    write_in_new_excel(version_dataframe, filename, folder_PATH, 'Version', startrow=3)
    add_style_version(version_dataframe, list_campaigns, filename, folder_PATH)

    # ## CREATION DE L'ONGLET STATIONS ##

    print('\n[!] Création de l\'onglet \"Stations\"...')
    stations_dataframe = create_stations_dataframe(head_dataframe, list_campaigns, dict_mp)
    write_in_existing_excel(stations_dataframe, filename, folder_PATH, 'Stations')
    add_style_stations(stations_dataframe, filename, folder_PATH)

    # ## CREATION DE L'ONGLET CAMPAGNES ##

    print('\n[!] Création de l\'onglet \"Campagnes\"...')
    campagnes_dataframe = create_campagnes_dataframe(head_dataframe, list_campaigns, dict_mp)
    write_in_existing_excel(campagnes_dataframe, filename, folder_PATH, 'Campagnes')
    add_style_campagnes(campagnes_dataframe, filename, folder_PATH)

    # ## CREATION DE L'ONGLET SURVIE ##

    print('\n[!] Création de l\'onglet \"Survie\"...')
    survie_dataframe = create_survie_dataframe(head_dataframe, list_campaigns, dict_mp)
    write_in_existing_excel(survie_dataframe, filename, folder_PATH, 'Survie', startcol=2, startrow=2)
    add_style_survie(survie_dataframe, filename, folder_PATH)

    # ## CREATION DE L'ONGLET PHYSICO-CHIMIE ##

    print('\n[!] Création de l\'onglet \"Physico-chimie\"...')
    physicochimie_dataframe = create_physicochimie_dataframe(head_dataframe, list_campaigns, dict_mp)
    write_in_existing_excel(physicochimie_dataframe, filename, folder_PATH, 'Physico-chimie_refChimie', startrow=2)
    write_in_existing_excel(physicochimie_dataframe, filename, folder_PATH, 'Physico-chimie_refToxicité', startrow=2)
    add_style_physicochimie(physicochimie_dataframe, filename, folder_PATH)


    # CREATION DE L'ONGLET BBAC ##
    dict_general = create_general_dict(list_campaigns)
    t0_associated = QueryScript(f"SELECT code_t0_id, id  FROM biomae.measurepoint WHERE id IN {tuple([mp for mp in dict_general])};").execute()
    dict_t0 = {}
    for mp in dict_general:
        dict_t0[mp] = dict_general[mp]
        index = [element[1] for element in t0_associated].index(mp)
        dict_t0[mp]['code_t0_id'] = t0_associated[index]
        
    print('\n[!] Création de l\'onglet \"BBAC 7j\"...')
    bbac_dataframe = create_bbac_7j_dataframe(head_dataframe, dict_general)
    bbac2_dataframe = create_bbac2_7j_dataframe(head_dataframe, dict_general)
    write_in_existing_excel(bbac_dataframe, filename, folder_PATH, 'BBAC_7j', startrow=3)
    write_in_existing_excel(bbac2_dataframe, filename, folder_PATH, 'BBAC2_7j', startrow=3)
    add_style_bbac_7j(bbac_dataframe, filename, folder_PATH, dict_t0)

    print('\n[!] Création de l\'onglet \"BBAC 21j\"...')
    bbac_dataframe = create_bbac_21j_dataframe(head_dataframe, dict_general)
    bbac2_dataframe = create_bbac2_21j_dataframe(head_dataframe, dict_general)
    write_in_existing_excel(bbac_dataframe, filename, folder_PATH, 'BBAC_21j', startrow=3)
    write_in_existing_excel(bbac2_dataframe, filename, folder_PATH, 'BBAC2_21j', startrow=3)
    add_style_bbac_21j(bbac_dataframe, filename, folder_PATH, dict_t0)

    # CREATION DE L'ONGLET NQE ##

    print('\n[!] Création de l\'onglet \"NQE Biote\"...')
    nqe_dataframe = create_nqe_dataframe(head_dataframe, dict_general)
    write_in_existing_excel(nqe_dataframe, filename, folder_PATH, 'NQE Biote', startrow=3)
    add_style_nqe(nqe_dataframe, filename, folder_PATH, dict_t0)

    ## CREATION DE L'ONGLET TOX ##

    print('\n[!] Création de l\'onglet \"Tox\"...')
    tox_dataframe = create_tox_dataframe(head_dataframe, list_campaigns, dict_mp)
    write_in_existing_excel(tox_dataframe, filename, folder_PATH, 'Tox', startrow=3)
    add_style_tox(tox_dataframe, filename, folder_PATH)

    print(colored('\n --> Rapport terminé', 'green'))


