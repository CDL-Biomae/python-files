from tools import QueryScript
from report import *

import pandas as pd
from termcolor import colored
from openpyxl import load_workbook


def create_filename(list_campaigns):
    filename = 'Rapport_pour'
    for c in list_campaigns:
        filename += f"_{c}"
    filename += '.xlsx'

    return filename


def write_in_new_excel(dataframe, filename, sheet, startcol=1, startrow=1):
    PATH = f"output\\{filename}"
    writer = pd.ExcelWriter(path=PATH, engine='openpyxl')
    dataframe.to_excel(writer, sheet_name=f"{sheet}", index=False, startcol=startcol, startrow=startrow)
    writer.save()
    writer.close()
    print(
        f"L'onglet \"{sheet}\" a été créé dans le nouveau fichier \"{filename}\"")


def write_in_existing_excel(dataframe, filename, sheet, startcol=1, startrow=1):
    PATH = f"output\\{filename}"
    book = load_workbook(PATH)
    writer = pd.ExcelWriter(path=PATH, engine='openpyxl')
    writer.book = book
    dataframe.to_excel(writer, sheet_name=f"{sheet}", index=False, startcol=startcol, startrow=startrow)
    writer.save()
    writer.close()
    print(f"L'onglet \"{sheet}\" a été créé dans le fichier \"{filename}\"")


def measure_points_fusion(campaign_ref):
    output = QueryScript(
        f"SELECT DISTINCT(measurepoint_fusion_id) FROM key_dates WHERE measurepoint_id IN (SELECT id FROM measurepoint WHERE reference LIKE '{campaign_ref}%');"
    )
    return output.execute()

def all_measure_points(campaign_ref):
    output = QueryScript(
        f"SELECT id FROM measurepoint WHERE reference LIKE '{campaign_ref}%';"
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

## MAIN FUNCTION ##


def main(list_campaigns):  # Prend en entrée une liste de reference de campagne, ex: ['AG-003-01', 'AG-003-02']
    filename = create_filename(list_campaigns)
    # print(list_campaigns)
    # print(filename)
    print('[+] Starting initialisation...')
    head_dataframe = create_head_dataframe(list_campaigns)
    # print(head_dataframe.head())
    dict_mp = create_dict_mp(list_campaigns)

    # create_tox_dataframe(head_dataframe, list_campaigns, dict_mp)

    ## CREATION DE L'ONGLET VERSION ##

    print('\n[!] Création de l\'onglet \"Version\"...')
    version_dataframe = create_version_dataframe()
    write_in_new_excel(version_dataframe, filename, 'Version', startrow=3)
    add_style_version(version_dataframe, list_campaigns, filename)

    ## CREATION DE L'ONGLET STATIONS ##

    print('\n[!] Création de l\'onglet \"Stations\"...')
    stations_dataframe = create_stations_dataframe(head_dataframe, list_campaigns, dict_mp)
    write_in_existing_excel(stations_dataframe, filename, 'Stations')
    add_style_stations(stations_dataframe, filename)

    ## CREATION DE L'ONGLET CAMPAGNES ##

    print('\n[!] Création de l\'onglet \"Campagnes\"...')
    campagnes_dataframe = create_campagnes_dataframe(head_dataframe, list_campaigns, dict_mp)
    write_in_existing_excel(campagnes_dataframe, filename, 'Campagnes')
    add_style_campagnes(campagnes_dataframe, filename)

    ## CREATION DE L'ONGLET PHYSICO-CHIMIE ##

    print('\n[!] Création de l\'onglet \"Physico-chimie\"...')
    physicochimie_dataframe = create_physicochimie_dataframe(head_dataframe, list_campaigns, dict_mp)
    write_in_existing_excel(physicochimie_dataframe, filename, 'Physico-chimie_refChimie', startrow=2)
    write_in_existing_excel(physicochimie_dataframe, filename, 'Physico-chimie_refToxicité', startrow=2)
    add_style_physicochimie(physicochimie_dataframe, filename)

    ## CREATION DE L'ONGLET NQE ##

    print('\n[!] Création de l\'onglet \"NQE Biote\"...')
    nqe_dataframe = create_nqe_dataframe(head_dataframe, list_campaigns, dict_mp)
    write_in_existing_excel(nqe_dataframe, filename, 'NQE Biote', startrow=3)
    add_style_nqe(nqe_dataframe, filename)
    
    ## CREATION DE L'ONGLET BBAC ##

    print('\n[!] Création de l\'onglet \"BBAC\"...')
    bbac_dataframe = create_bbac_dataframe(head_dataframe, list_campaigns, dict_mp)
    bbac2_dataframe = create_bbac2_dataframe(head_dataframe, list_campaigns, dict_mp)
    write_in_existing_excel(bbac_dataframe, filename, 'BBAC', startrow=3)
    write_in_existing_excel(bbac2_dataframe, filename, 'BBAC2', startrow=3)
    add_style_bbac(bbac_dataframe, filename)


