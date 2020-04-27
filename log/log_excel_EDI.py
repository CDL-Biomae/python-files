import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from report.xl import create_edi_dataframe
from report.style import add_style_edi
from report.initialization import initialize
import pandas as pd
from openpyxl import load_workbook
import env

class LogExcelEDIApp(tk.Tk):
    def __init__(self, master=None, campaign=None, output_path=""):
        self.master = master
        tk.Label(master=self.master, text="    ").grid(row=0,column=0)
        tk.Label(master=self.master,text=f"Création du rapport EDI pour {campaign}").grid(row=1,column=1, sticky="w")

        self.label_text = tk.Label(master=self.master)
        self.label_text.grid(row=3,column=1,sticky="w")
        self.progressbar_element = ttk.Progressbar(master=self.master,orient="horizontal",length=350,mode="determinate")
        self.progressbar_element.grid(row=2,column=1, sticky="w")
        self.progressbar_element["value"]=0
        self.progressbar_element["maximum"]=3
        self.quit_window = False
        self.main(campaign, output_path)
    
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

    def write_in_new_excel(self, dataframe, PATH, sheet, startcol=0, startrow=0):
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


    def main(self, campaign, output_path):
        self.text = "Chargement des données..."
        campaigns_dict, measurepoint_list, chemistry_measurepoint_list, chemistry_pack_list, chemistry_7j_measurepoint_list, chemistry_21j_measurepoint_list, _, _, _ = initialize([campaign])
        self.progressbar +=1
        place_dict = None
        for campaign_id in campaigns_dict:
            place_dict = campaigns_dict[campaign_id]["place"]
            break
        edi_dataframe = create_edi_dataframe(campaign, place_dict, chemistry_measurepoint_list, chemistry_pack_list, chemistry_7j_measurepoint_list, chemistry_21j_measurepoint_list)

        self.write_in_new_excel(edi_dataframe, output_path, 'Export EDI', startrow=2)
        self.progressbar +=1
        add_style_edi(edi_dataframe, output_path)
        self.progressbar +=1

        
        
        self.progressbar = self.progressbar_element["maximum"]

        self.text = "Terminé"

        tk.Button(master=self.master, text="OK", command=self.kill_window).grid(row=4, column=1, ipadx=30)

