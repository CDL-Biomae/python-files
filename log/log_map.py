import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from tools import QueryScript
from report.initialization import initialize
from io import BytesIO
from PIL import Image, ImageTk
from calcul import chemistry, elements_crustacean
import requests
import os 
import env

class LogMapApp(tk.Tk):
    def __init__(self, master=None, campaign_list=[]):
        self.master = master
        self.campaign_list = campaign_list
        tk.Label(master=self.master, text="    ").grid(row=0,column=0)
        tk.Label(master=self.master,text=f"Création de carte de résultat pour {' '.join(campaign_list)}").grid(row=1,column=1, sticky="w")

        self.label_text = tk.Label(master=self.master)
        self.text = "Chargement des résultats..."
        self.label_text.grid(row=3,column=1,sticky="w")
        self.quit_window = False
        self.progressbar_element = ttk.Progressbar(master=self.master,orient="horizontal",length=350,mode="determinate")
        self.progressbar_element.grid(row=2,column=1,columnspan=4, sticky="w")
        self.progressbar_element["value"]=0
        self.progressbar_element["maximum"]=5
        self.campaigns_dict, self.measurepoint_list, self.chemistry_measurepoint_list, self.chemistry_pack_list, self.chemistry_7j_measurepoint_list, self.chemistry_21j_measurepoint_list, self.tox_measurepoint_list, _, _ = initialize(campaign_list)
        self.progressbar+=1
        self.geographic_data = QueryScript(f"SELECT id, longitudeSpotted, latitudeSpotted FROM {env.DATABASE_RAW}.Measurepoint WHERE id IN  {tuple(self.measurepoint_list) if len(self.measurepoint_list)>1 else '('+(str(self.measurepoint_list[0]) if len(self.measurepoint_list) else '0')+')'}").execute()
        self.progressbar+=1
        self.tox_data = QueryScript(f"SELECT measurepoint_id, male_survival_7_days, round(alimentation, 1), round(neurotoxicity, 1), female_survivor, round(percent_inhibition_fecondite, 1) FROM {env.DATABASE_TREATED}.toxtable WHERE version=  {env.CHOSEN_VERSION()} AND measurepoint_id IN {tuple(self.tox_measurepoint_list) if len(self.tox_measurepoint_list)>1 else '('+(str(self.tox_measurepoint_list[0]) if len(self.tox_measurepoint_list) else '0')+')'};").execute()
        self.progressbar+=1
        self.threshold_tox = QueryScript(f"SELECT parameter, threshold, meaning FROM {env.DATABASE_TREATED}.r2_threshold").execute()
        self.progressbar+=1
        self.threshold_chemistry = QueryScript(f"SELECT parameter, sandre, nqe, 7j_threshold, 7j_graduate_25, 7j_graduate_50, 7j_graduate_75, 21j_threshold, 21j_graduate_25, 21j_graduate_50, 21j_graduate_75 FROM {env.DATABASE_TREATED}.r3").execute()
        self.biotest_chosen = tk.StringVar()
        self.biotest_list = []
        if len(self.tox_measurepoint_list): 
            self.biotest_list.append("Alimentation")
            self.biotest_list.append("Neurotoxicité")
            self.biotest_list.append("Reprotoxicité")
        if len(self.chemistry_pack_list):
            self.result_dict = chemistry.result(self.campaigns_dict, self.chemistry_pack_list)
            self.biotest_list.append("NQE")
            if len(self.chemistry_7j_measurepoint_list):
                self.biotest_list.append("Chimie(7j)")
            if len(self.chemistry_21j_measurepoint_list):
                self.biotest_list.append("Chimie(21j)")

        self.biotest_chosen.set(self.biotest_list[0])

        tk.Label(master=self.master, text='Biotest :').grid(row=4,column=1)
        tk.OptionMenu(self.master, self.biotest_chosen, *self.biotest_list, command=self.show_sandre).grid(row=4,column=2)

        self.frame_selection = tk.Frame(master=self.master)
        self.frame_selection.grid(row=4,column=3, columnspan=2)
        self.show_sandre(self.biotest_chosen.get())
        self.progressbar+=1
        for campaign_id  in self.campaigns_dict:
            for place_id in self.campaigns_dict[campaign_id]["place"]:
                for measurepoint_id in self.campaigns_dict[campaign_id]["place"][place_id]["measurepoint"]:
                    for mp_id, longitude, latitude in self.geographic_data:
                        if measurepoint_id==mp_id :
                            if longitude :
                                self.campaigns_dict[campaign_id]["place"][place_id]["longitude"] = longitude
                            if latitude :
                                self.campaigns_dict[campaign_id]["place"][place_id]["latitude"] = latitude
        self.t0_associated = QueryScript(f"SELECT code_t0_id, id  FROM {env.DATABASE_RAW}.Measurepoint WHERE id IN {tuple(self.chemistry_measurepoint_list)};").execute()
        self.dict_t0 = {}
        for campaign_id in self.campaigns_dict:
            for place_id in self.campaigns_dict[campaign_id]["place"]:
                for measurepoint_id in self.campaigns_dict[campaign_id]["place"][place_id]["measurepoint"]:
                    for code_t0_id, mp_id in self.t0_associated:
                        if measurepoint_id==mp_id and place_id not in self.dict_t0:
                            self.dict_t0[measurepoint_id] = {"code_t0_id": code_t0_id}
        self.t0_value_list = QueryScript(f"SELECT Analysis.prefix, Analysis.value, Analysis.sandre, Measurepoint.id FROM {env.DATABASE_RAW}.Analysis JOIN {env.DATABASE_RAW}.Pack ON Pack.id=Analysis.pack_id JOIN {env.DATABASE_RAW}.Measurepoint ON Measurepoint.id=Pack.measurepoint_id WHERE Measurepoint.id in (SELECT distinct code_t0_id FROM {env.DATABASE_RAW}.Measurepoint WHERE id IN {tuple(self.measurepoint_list) if len(self.measurepoint_list)>1 else '('+(str(self.measurepoint_list[0]) if len(self.measurepoint_list) else '0')+')'})").execute()

        self.text = "Choisissez une mode d'affichage"
        tk.Button(master=self.master, text="Générer la carte", command=self.main).grid(row=5,column=1)
        self.image =  None

    def show_sandre(self, selection):
        
        self.frame_selection.destroy()
        self.frame_selection = tk.Frame(master=self.master)
        self.frame_selection.grid(row=4,column=3, columnspan=2)
        if not self.biotest_chosen.get() in ["Alimentation", "Neurotoxicité", "Reprotoxicité"]:
            self.sandre_selected = tk.StringVar()
            self.sandre_able = []
            if self.biotest_chosen.get() == 'NQE':
                for parameter, sandre, nqe, threshold_7j, graduate_7j_25, graduate_7j_50, graduate_7j_75, threshold_21j, graduate_21j_25, graduate_21j_50, graduate_21j_75 in self.threshold_chemistry:
                    for element in elements_crustacean:
                        if sandre==str(element) :
                            self.sandre_able.append([sandre,f"{sandre} : {parameter}"])
            if self.biotest_chosen.get() == 'Chimie(7j)':
                for parameter, sandre, nqe, threshold_7j, graduate_7j_25, graduate_7j_50, graduate_7j_75, threshold_21j, graduate_21j_25, graduate_21j_50, graduate_21j_75 in self.threshold_chemistry:
                    if threshold_7j :
                        self.sandre_able.append([sandre,f"{sandre} : {parameter}"])
            if self.biotest_chosen.get() == 'Chimie(21j)':
                for parameter, sandre, nqe, threshold_7j, graduate_7j_25, graduate_7j_50, graduate_7j_75, threshold_21j, graduate_21j_25, graduate_21j_50, graduate_21j_75 in self.threshold_chemistry:
                    if threshold_21j :
                        self.sandre_able.append([sandre,f"{sandre} : {parameter}"])
            self.sandre_selected.set(self.sandre_able[0][1])
            self.sandre_selection_label = tk.Label(master=self.frame_selection, text='Sandre :').grid(row=0,column=0)
            self.sandre_selection_menu = tk.OptionMenu(self.frame_selection, self.sandre_selected, *[element[1] for element in self.sandre_able], command=self.select_sandre).grid(row=0,column=1)
        else :
            self.sandre_selection_label = tk.Label(master=self.frame_selection, text='').grid(row=0,column=0)
            self.sandre_selection_menu = tk.Label(self.frame_selection, text='').grid(row=0,column=1)

    def save(self):
        self.output_path = tk.filedialog.asksaveasfilename(title=f"Enregistrer l'image",filetypes=[("PNG (*.png)","*.png")], defaultextension=".png", initialfile=f"Carte des résultats {' '.join(self.campaign_list)} - {self.last_choice}")
        if self.output_path :
            self.image.save(self.output_path, "PNG")

    def select_sandre(self, selection):
        self.sandre_selected.set(selection)

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

    def main(self):
        threshold_list = [None, None, None, None]
        if self.threshold_tox :
            if self.biotest_chosen.get()=='Alimentation':
                for parameter, threshold, meaning in self.threshold_tox:
                    if parameter=='alimentation':
                        if meaning=="pas d'effet":
                            threshold_list[0]=threshold
                        if meaning=="effet faible":
                            threshold_list[1]=threshold
                        if meaning=="effet modéré":
                            threshold_list[2]=threshold
                        if meaning=="effet élevé":
                            threshold_list[3]=threshold

            if self.biotest_chosen.get()=='Neurotoxicité':
                for parameter, threshold, meaning in self.threshold_tox:
                    if parameter=='neurotoxicité AChE':
                        if meaning=="pas d'effet":
                            threshold_list[0]=threshold
                        if meaning=="effet faible":
                            threshold_list[1]=threshold
                        if meaning=="effet modéré":
                            threshold_list[2]=threshold
                        if meaning=="effet élevé":
                            threshold_list[3]=threshold

            if self.biotest_chosen.get()=='Reprotoxicité':
                for parameter, threshold, meaning in self.threshold_tox:
                    if parameter=='reproduction':
                        if meaning=="pas d'effet":
                            threshold_list[0]=threshold
                        if meaning=="effet faible":
                            threshold_list[1]=threshold
                        if meaning=="effet modéré":
                            threshold_list[2]=threshold
                        if meaning=="effet élevé":
                            threshold_list[3]=threshold
            if self.biotest_chosen.get()=='NQE':
                for parameter, sandre, nqe, threshold_7j, graduate_7j_25, graduate_7j_50, graduate_7j_75, threshold_21j, graduate_21j_25, graduate_21j_50, graduate_21j_75 in self.threshold_chemistry:
                    sandre_chosen = None 
                    for element in self.sandre_able:
                        if element[1]==self.sandre_selected.get():
                            sandre_chosen=element[0]
                    if sandre_chosen and sandre==sandre_chosen:
                        if nqe:
                            threshold_list[0]=nqe
                            threshold_list[1]=nqe
                            threshold_list[2]=nqe
                            threshold_list[3]=nqe
            if self.biotest_chosen.get()=='Chimie(7j)':
                for parameter, sandre, nqe, threshold_7j, graduate_7j_25, graduate_7j_50, graduate_7j_75, threshold_21j, graduate_21j_25, graduate_21j_50, graduate_21j_75 in self.threshold_chemistry:
                    sandre_chosen = None 
                    for element in self.sandre_able:
                        if element[1]==self.sandre_selected.get():
                            sandre_chosen=element[0]
                    if sandre_chosen and sandre==sandre_chosen:
                        if threshold_7j:
                            threshold_list[0]=threshold_7j
                            if graduate_7j_25:
                                threshold_list[1]=graduate_7j_25
                                threshold_list[2]=graduate_7j_50
                                threshold_list[3]=graduate_7j_75
                            else :
                                threshold_list[1]=threshold_7j
                                threshold_list[2]=threshold_7j
                                threshold_list[3]=threshold_7j
            if self.biotest_chosen.get()=='Chimie(21j)':
                for parameter, sandre, nqe, threshold_7j, graduate_7j_25, graduate_7j_50, graduate_7j_75, threshold_21j, graduate_21j_25, graduate_21j_50, graduate_21j_75 in self.threshold_chemistry:
                    sandre_chosen = None 
                    for element in self.sandre_able:
                        if element[1]==self.sandre_selected.get():
                            sandre_chosen=element[0]
                    if sandre_chosen and sandre==sandre_chosen:
                        if threshold_21j:
                            threshold_list[0]=threshold_21j
                            if graduate_21j_25:
                                threshold_list[1]=graduate_21j_25
                                threshold_list[2]=graduate_21j_50
                                threshold_list[3]=graduate_21j_75
                            else :
                                threshold_list[1]=threshold_21j
                                threshold_list[2]=threshold_21j
                                threshold_list[3]=threshold_21j




        markers = []
        for campaign_id  in self.campaigns_dict:
            for place_id in self.campaigns_dict[campaign_id]["place"]:
                number = self.campaigns_dict[campaign_id]['place'][place_id]['number']
                color = 'AFAFAF'
                value = 0
                if "longitude" in self.campaigns_dict[campaign_id]["place"][place_id] and "latitude" in self.campaigns_dict[campaign_id]["place"][place_id]:
                    longitude = self.campaigns_dict[campaign_id]['place'][place_id]['longitude']
                    latitude = self.campaigns_dict[campaign_id]['place'][place_id]['latitude']
                for measurepoint_id in self.campaigns_dict[campaign_id]['place'][place_id]["measurepoint"]:
                    if self.biotest_chosen.get() in ['Alimentation', 'Neurotoxicité','Reprotoxicité']:
                        for mp_id, male_survival, alim, neuro, female_survival, fecondity in self.tox_data:
                            if mp_id==measurepoint_id:
                                if self.biotest_chosen.get()=='Alimentation' and male_survival:
                                    value = -alim if alim else None
                                if self.biotest_chosen.get()=='Neurotoxicité':
                                    value = -neuro if neuro else None
                                if self.biotest_chosen.get()=='Reprotoxicité' and female_survival:
                                    value = -fecondity if fecondity else None
                    else :
                        for element in self.sandre_able:
                            if element[1]==self.sandre_selected.get():
                                sandre_chosen=int(element[0])
                        if measurepoint_id in self.result_dict and sandre_chosen in self.result_dict[measurepoint_id]:
                            if isinstance(self.result_dict[measurepoint_id][sandre_chosen],str) and self.result_dict[measurepoint_id][sandre_chosen][0]=="<":
                                value=-1
                            else :
                                value = self.result_dict[measurepoint_id][sandre_chosen]
                            t0_found = False 
                            for prefix, t0_value, sandre, mp_id in self.t0_value_list :
                                if sandre_chosen == int(sandre) and mp_id==self.dict_t0[measurepoint_id]["code_t0_id"]:
                                    if not t0_value or (isinstance(t0_value,float) and threshold_list[0] and t0_value>float(threshold_list[0])):
                                        value=0
                                    t0_found=True
                if value and ((self.biotest_chosen.get() in ["NQE","Chimie(7j)","Chimie(21j)"] and t0_found) or self.biotest_chosen.get() in ['Alimentation', 'Neurotoxicité','Reprotoxicité']):
                    value=float(value)
                    if threshold_list[0] and value>float(threshold_list[0]):
                        if threshold_list[1] and value>float(threshold_list[1]):
                            if threshold_list[2] and value>float(threshold_list[2]):
                                if threshold_list[3] and value>float(threshold_list[3]):
                                    color = 'FF0000'
                                else :
                                    color = 'FFA500'
                            else :
                                color = 'FFFF00'
                        else :
                            color = '008000'
                    else :
                        color = '0000FF'



                markers.append(f"pin-s-{round(10*(number - int(number))) if number!=int(number) else number}+{color}({longitude},{latitude})")
        access_token = env.ACCESS_TOKEN_MAPBOX
        url = f"https://api.mapbox.com/styles/v1/mapbox/streets-v11/static/{','.join(markers)}/auto/500x500?access_token={access_token}"
        response = requests.get(url)
        self.image = Image.open(BytesIO(response.content))
        image = ImageTk.PhotoImage(self.image)
        self.master.geometry = '600x600+150+150'
        self.output_map = tk.Canvas(self.master, width=500, height=500, bg='white')
        self.output_map.create_image(252,252,image=image)
        self.output_map.image = image
        self.output_map.grid(row=6, column=1, columnspan=4)
        self.last_choice = f"{self.biotest_chosen.get()}{(' - '+ str(sandre_chosen)) if self.biotest_chosen.get() in ['NQE','Chimie(7j)','Chimie(21j)'] else ''}"
        tk.Button(master=self.master, text="Enregistrer", command=self.save).grid(row=5, column=2)