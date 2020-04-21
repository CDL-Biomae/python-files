import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from report.xl import *
from report.style import *
from report.initialization import create_campaigns_dict, initialize, create_head_dataframe, create_head_special_dataframe
from calcul import chemistry
import pandas as pd
from termcolor import colored
from openpyxl import load_workbook
import env

class LogExcelApp(tk.Tk):
    def __init__(self, master=None, campaign_list=[], output_path=""):
        self.master = master
        tk.Label(master=self.master, text="    ").grid(row=0,column=0)
        tk.Label(master=self.master,text=f"Création du rapport annexe pour {' '.join(campaign_list)}").grid(row=1,column=1, sticky="w")

        self.label_text = tk.Label(master=self.master)
        self.label_text.grid(row=3,column=1,sticky="w")
        self.progressbar_element = ttk.Progressbar(master=self.master,orient="horizontal",length=350,mode="determinate")
        self.progressbar_element.grid(row=2,column=1, sticky="w")
        self.progressbar_element["value"]=0
        self.progressbar_element["maximum"]=12
        self.quit_window = False
        self.main(campaign_list, output_path)
    
    @property
    def text(self):
        """
        Read/write the line logged in the log window
        """
        return self.text_value.get()

    @text.setter
    def text(self, value):
        self.label_text.config(text = value)

    
    @property
    def progressbar(self):
        """
        Read/write the last line logged in the log window
        """
        return self.progressbar_element["value"]

    @progressbar.setter
    def progressbar(self, value):
        self.progressbar_element["value"] = value
        self.progressbar_element.update()

    def kill_window(self):
        self.master.destroy()

    def write_in_new_excel(self, dataframe, PATH, sheet, startcol=1, startrow=1):
        '''
        Créé un nouveau fichier excel et rempli un onglet avec des données
        :param dataframe: données
        :param filename: nom du fichier
        :param PATH: chemin vers le fichier
        :param sheet: nom de l'onglet
        :param startcol: colonne de démarrage de l'écriture
        :param startrow:  ligne de démarrage de l'écriture
        '''
        writer = pd.ExcelWriter(path=PATH, engine='openpyxl')
        dataframe.to_excel(writer, sheet_name=f"{sheet}", index=False, startcol=startcol, startrow=startrow)
        writer.save()
        writer.close()
        self.progressbar += 1

    def write_in_existing_excel(self, dataframe, PATH, sheet, startcol=1, startrow=1):
        '''
        Ajoute un onglet avec des données dans un fichier excel existant
        :param dataframe: données
        :param filename: nom du fichier
        :param folder_PATH: chemin vers le fichier
        :param sheet: nom de l'onglet
        :param startcol: colonne de démarrage de l'écriture
        :param startrow:  ligne de démarrage de l'écriture
        '''
        book = load_workbook(PATH)
        writer = pd.ExcelWriter(path=PATH, engine='openpyxl')
        writer.book = book
        dataframe.to_excel(writer, sheet_name=f"{sheet}", index=False, startcol=startcol, startrow=startrow)
        writer.save()
        writer.close()
        self.progressbar += 1

    def main(self, campaign_list, output_path):
        self.text = "Chargement des données..."
        campaigns_dict, measurepoint_list, chemistry_measurepoint_list, chemistry_pack_list, chemistry_7j_measurepoint_list, chemistry_21j_measurepoint_list, tox_measurepoint_list, agency_code_list, J_dict = initialize(campaign_list)
        head_dataframe, head_filtered_dataframe, place_list = create_head_dataframe(campaigns_dict)
        head_chemistry_dataframe, head_chemistry_7j_dataframe, head_chemistry_21j_dataframe =  create_head_special_dataframe(campaigns_dict, chemistry_measurepoint_list, chemistry_7j_measurepoint_list, chemistry_21j_measurepoint_list)

        ## CREATION DE L'ONGLET VERSION ##
        self.text = "Création de l'onglet Version..."
        version_dataframe = create_version_dataframe()
        self.write_in_new_excel(version_dataframe, output_path, 'Version', startrow=3)
        add_style_version(version_dataframe, campaign_list, output_path)


        ## CREATION DE L'ONGLET STATIONS ##
        self.text = "Création de l'onglet Station..."
        stations_dataframe = create_stations_dataframe(head_filtered_dataframe, campaigns_dict, measurepoint_list, agency_code_list, place_list)
        self.write_in_existing_excel(stations_dataframe, output_path, 'Stations')
        add_style_stations(stations_dataframe, output_path)


        ## CREATION DE L'ONGLET CAMPAGNES ##

        self.text = "Création de l'onglet Campagnes..."
        campagnes_dataframe = create_campagnes_dataframe(head_dataframe, campaigns_dict, J_dict)
        self.write_in_existing_excel(campagnes_dataframe, output_path, 'Campagnes')
        add_style_campagnes(campagnes_dataframe, output_path)


        ## CREATION DE L'ONGLET SURVIE ##

        if len(chemistry_pack_list):
            self.text = "Création de l'onglet Survie..."
            survie_dataframe = create_survie_dataframe(campaigns_dict, chemistry_measurepoint_list,chemistry_pack_list)
            self.write_in_existing_excel(survie_dataframe, output_path, 'Survie', startcol=2, startrow=2)
            add_style_survie(survie_dataframe, output_path)


        ## CREATION DE L'ONGLET PHYSICO-CHIMIE ##
        if len(measurepoint_list) :
            self.text = "Création de l'onglet Physicochimie..."
            physicochimie_dataframe = create_physicochimie_dataframe(head_dataframe, measurepoint_list, campaigns_dict, J_dict)
            self.write_in_existing_excel(physicochimie_dataframe, output_path, 'Physico-chimie_refChimie', startrow=2)
            self.write_in_existing_excel(physicochimie_dataframe, output_path, 'Physico-chimie_refToxicité', startrow=2)
            add_style_physicochimie(physicochimie_dataframe, output_path)

        # CREATION DE L'ONGLET BBAC ##


        
        self.text = "Création des onglets BBAC..."
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
            if len(list(result_dict.keys())):
                if len(chemistry_7j_measurepoint_list):
                    bbac_dataframe = create_bbac_7j_dataframe(head_chemistry_7j_dataframe, result_dict, chemistry_7j_measurepoint_list)
                    bbac2_dataframe = create_bbac2_7j_dataframe(head_chemistry_7j_dataframe, result_dict, chemistry_7j_measurepoint_list)
                    self.write_in_existing_excel(bbac_dataframe, output_path, 'BBAC_7j', startrow=3)
                    self.write_in_existing_excel(bbac2_dataframe, output_path, 'BBAC2_7j', startrow=3)
                    add_style_bbac_7j(bbac_dataframe, output_path, dict_t0)
                if len(chemistry_21j_measurepoint_list):
                    bbac_dataframe = create_bbac_21j_dataframe(head_chemistry_21j_dataframe, result_dict, chemistry_21j_measurepoint_list)
                    bbac2_dataframe = create_bbac2_21j_dataframe(head_chemistry_21j_dataframe, result_dict, chemistry_21j_measurepoint_list)
                    self.write_in_existing_excel(bbac_dataframe, output_path, 'BBAC_21j', startrow=3)
                    self.write_in_existing_excel(bbac2_dataframe, output_path, 'BBAC2_21j', startrow=3)
                    add_style_bbac_21j(bbac_dataframe, output_path, dict_t0)  

                # CREATION DE L'ONGLET NQE ##
                self.text = "Création de l'onglet NQE Biote..."
                nqe_dataframe = create_nqe_dataframe(head_chemistry_dataframe, result_dict, chemistry_measurepoint_list)
                self.write_in_existing_excel(nqe_dataframe, output_path, 'NQE Biote', startrow=3)
                add_style_nqe(nqe_dataframe, output_path, dict_t0) 


        ## CREATION DE L'ONGLET TOX ##
        if len(tox_measurepoint_list):
            self.text = "Création de l'onglet Tox..."
            tox_dataframe = create_tox_dataframe(campaigns_dict, tox_measurepoint_list)
            self.write_in_existing_excel(tox_dataframe, output_path, 'Tox', startrow=3)
            add_style_tox(tox_dataframe, output_path)
        
        self.progressbar = self.progressbar_element["maximum"]

        self.text = "Terminé"

        tk.Button(master=self.master, text="OK", command=self.kill_window).grid(row=4, column=1, ipadx=30)

