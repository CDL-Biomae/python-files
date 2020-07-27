import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from report.xl import *
from report.style import *
import pandas as pd
from openpyxl import load_workbook
from tools import QueryScript
import env

class LogChemistryExcelApp(tk.Tk):
    def __init__(self, master=None, campaign_list=[], output_path="", only_agency=False):
        self.master = master
        tk.Label(master=self.master, text="    ").grid(row=0,column=0)
        tk.Label(master=self.master,text=f"Création du bilan de données chimies {'pour' if len(campaign_list) else ''} {' '.join(campaign_list)}").grid(row=1,column=1, sticky="w")

        self.label_text = tk.Label(master=self.master)
        self.label_text.grid(row=3,column=1,sticky="w")
        self.progressbar_element = ttk.Progressbar(master=self.master,orient="horizontal",length=350,mode="determinate")
        self.progressbar_element.grid(row=2,column=1, sticky="w")
        self.progressbar_element["value"]=0
        self.progressbar_element["maximum"]=11
        self.quit_window = False
        self.main(campaign_list, output_path, only_agency)
    
    @property
    def text(self):
        """
        Read/write the line logged in the log window
        """
        return self.label_text.get()

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

    def main(self, campaign_list, output_path, only_agency):
        if only_agency and len(campaign_list)==0:
            contract_list = ["RMC-7j","AG-7j",'SN-7j','AP-7j','RM-7j', 'LB-7j', 'TOTAL-7j', "RMC-21j","AG-21j",'SN-21j','AP-21j','RM-21j', 'LB-21j', 'TOTAL-21j']
        else  :
            contract_list = [campaign.split('-')[0] + '-7j' for campaign in campaign_list] + ['TOTAL-7j'] + [campaign.split('-')[0] + '-21j' for campaign in campaign_list] + ['TOTAL-21j']
        self.text = "Chargement des données..."
        context_data = QueryScript(f"SELECT measurepoint_id, recordedAt, temperature, conductivity, oxygen, pH, barrel, comment FROM {env.DATABASE_RAW}.MeasureExposureCondition").execute()
        self.progressbar +=1
        main_data = QueryScript(f"SELECT distinct Place.agency_id, Measurepoint.id, Pack.id, Measurepoint.reference, start_date.date, end_date.date, Place.name, average_temperature.sensor3_min, average_temperature.sensor3_average, average_temperature.sensor3_max, Pack.sampling_weight, Pack.metal_tare_bottle_weight, Pack.organic_tare_bottle_weight, Pack.organic_total_weight, Pack.sampling_quantity,T0.reference, T0.sampling_weight, T0.metal_tare_bottle_weight, T0.organic_tare_bottle_weight, T0.organic_total_weight, T0.sampling_quantity , Survival.percent FROM {env.DATABASE_RAW}.Measurepoint JOIN (SELECT Measurepoint.id, Measurepoint.reference, Pack.sampling_weight, Pack.metal_tare_bottle_weight, Pack.organic_tare_bottle_weight, Pack.organic_total_weight, Pack.sampling_quantity FROM {env.DATABASE_RAW}.Measurepoint JOIN {env.DATABASE_RAW}.Pack ON Pack.measurepoint_id=Measurepoint.id WHERE code_t0_id IS NULL) as T0 ON T0.id=Measurepoint.code_t0_id JOIN {env.DATABASE_RAW}.Pack ON Pack.measurepoint_id=Measurepoint.id JOIN (SELECT measurepoint_id, date FROM {env.DATABASE_TREATED}.key_dates WHERE key_dates.date_id=6 AND version={env.CHOSEN_VERSION()} AND date IS NOT NULL) as start_date ON start_date.measurepoint_id=Measurepoint.id JOIN (SELECT measurepoint_id, date FROM {env.DATABASE_TREATED}.key_dates WHERE key_dates.date_id=7 AND version={env.CHOSEN_VERSION()} AND date IS NOT NULL) as end_date ON end_date.measurepoint_id=Measurepoint.id JOIN {env.DATABASE_RAW}.Place ON Place.id=Measurepoint.place_id JOIN {env.DATABASE_TREATED}.average_temperature ON average_temperature.measurepoint_id=Measurepoint.id JOIN ( SELECT AVG(scud_survivor/scud_quantity*100) as percent, pack_id FROM biomae.Cage GROUP BY pack_id) as Survival ON Survival.pack_id=Pack.id WHERE Pack.nature='chemistry' AND average_temperature.version={env.CHOSEN_VERSION()} AND Measurepoint.code_t0_id IS NOT NULL;").execute()
        self.progressbar +=1
        agency_data = QueryScript(f"SELECT id, code, network, hydroecoregion FROM {env.DATABASE_RAW}.Agency").execute()
        self.progressbar +=1
        
        analysis_data = QueryScript(f"SELECT pack_id, value, sandre, name FROM {env.DATABASE_RAW}.Analysis").execute()
        self.progressbar +=1
        chemical_threshold_data = QueryScript(f"SELECT sandre, familly, 7j_graduate_50, 21j_graduate_50 FROM {env.DATABASE_TREATED}.r3 WHERE version={env.CHOSEN_VERSION()}").execute()
        self.progressbar +=1
        context_threshold_data = QueryScript(f"SELECT parameter, min, max FROM {env.DATABASE_TREATED}.r1 WHERE version={env.CHOSEN_VERSION()} AND parameter like '%chimie%'").execute()
        self.progressbar +=1
        self.text = "Création des onglets"

        chemistry_dataframe, report_dataframe = create_chemistry_dataframe(context_data, main_data, analysis_data, chemical_threshold_data, context_threshold_data, agency_data, contract_list)
        self.progressbar +=1
        self.write_in_new_excel(chemistry_dataframe, output_path, 'Data', startrow=0, startcol=0)
        self.progressbar +=1
        self.write_in_existing_excel(report_dataframe, output_path, 'Bilan', startrow=0, startcol=0)
        self.progressbar +=1
        add_style_chemistry(output_path)
        self.progressbar = self.progressbar_element["maximum"]
        self.text = "Terminé"

        tk.Button(master=self.master, text="OK", command=self.kill_window).grid(row=4, column=1, ipadx=30)

