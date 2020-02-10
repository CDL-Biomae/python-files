from tools import QueryScript
from report import create_head_dataframe
from report import create_stations_dataframe
from report import create_campagnes_dataframe
from report import create_physicochimie_dataframe
from report import add_style_stations
import pandas as pd
from openpyxl import load_workbook


def create_filename(list_campaigns):
    filename = 'Rapport_pour'
    for c in list_campaigns:
        filename += f"_{c}"
    filename += '.xlsx'

    return filename


def write_in_new_excel(dataframe, filename, sheet):
    PATH = f"output\\{filename}"
    writer = pd.ExcelWriter(path=PATH, engine='openpyxl')
    dataframe.to_excel(writer, sheet_name=f"{sheet}", index=False, startcol=1, startrow=1)
    writer.save()
    writer.close()
    print(
        f"L'onglet \"{sheet}\" a été créé dans le nouveau fichier \"{filename}\"")


def write_in_existing_excel(dataframe, filename, sheet):
    PATH = f"output\\{filename}"
    book = load_workbook(PATH)
    writer = pd.ExcelWriter(path=PATH, engine='openpyxl')
    writer.book = book
    dataframe.to_excel(writer, sheet_name=f"{sheet}", index=False, startcol=1, startrow=1)
    writer.save()
    writer.close()
    print(f"L'onglet \"{sheet}\" a été créé dans le fichier \"{filename}\"")


def measure_points(campaign_ref):
    output = QueryScript(
        f"SELECT DISTINCT(measurepoint_fusion_id) FROM key_dates WHERE measurepoint_id IN (SELECT id FROM measurepoint WHERE reference LIKE '{campaign_ref}%');"
    )
    return output.execute()


def create_dict_mp(list_campaigns):
    dict = {}
    for c in list_campaigns:
        list_mp = measure_points(c)
        dict[c] = list_mp
    return dict

## MAIN FUNCTION ##
# Prend en entrée une liste de reference de campagne, ex: ['AG-003-01', 'AG-003-02']


def main(list_campaigns):
    filename = create_filename(list_campaigns)
    print(filename)
    print('[+] Starting initialisation...')
    head_dataframe = create_head_dataframe(list_campaigns)
    print(head_dataframe.head())
    dict_mp = create_dict_mp(list_campaigns)

    ## CREATION DE L'ONGLET STATIONS ##
    stations_dataframe = create_stations_dataframe(
        head_dataframe, list_campaigns, dict_mp)
    write_in_new_excel(stations_dataframe, filename, 'Stations')
    add_style_stations(stations_dataframe, filename)

    ## CREATION DE L'ONGLET CAMPAGNES ##
    # campagnes_dataframe = create_campagnes_dataframe(
    #     head_dataframe, list_campaigns, dict_mp)
    # write_in_existing_excel(campagnes_dataframe, filename, 'Campagnes')

    ## CREATION DE L'ONGLET PHYSICO-CHIMIE ##
    # physicochimie_dataframe = create_physicochimie_dataframe(head_dataframe, list_campaigns, dict_mp)
    # write_in_existing_excel(physicochimie_dataframe, filename, 'Physico-chimie')

