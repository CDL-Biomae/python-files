import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from database import version_filler, reference_filler, reference_key_date_filler, key_date_filler, average_temperature_filler, temperature_repro_filler, tox_table_filler

class LogDatabaseApp(tk.Tk):
    def __init__(self, master=None, case=0, xl_path=None, date=None, comment=None):
        self.master = master
        tk.Label(master=self.master, text="    ").grid(row=0,column=0)
        tk.Label(master=self.master,text=f"Mise à jour de la base de données traitées").grid(row=1,column=1, sticky="w")

        self.label_text = tk.Label(master=self.master)
        self.label_text.grid(row=3,column=1,sticky="w")
        self.progressbar_element = ttk.Progressbar(master=self.master,orient="horizontal",length=350,mode="determinate")
        self.progressbar_element.grid(row=2,column=1, sticky="w")
        self.progressbar_element["value"]=0
        self.progressbar_element["maximum"]=8
        self.quit_window = False
        self.main(case, xl_path, date, comment)
    
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


    def main(self, case=0, xl_path=None, date=None, comment=None):
        if case==0:
            return None
        if case==1 or case==3:
            version_filler.run(case, date, comment)
        self.text = "Remplissage des tables de références..."
        self.progressbar += 1
        
        reference_filler.run(case, xl_path)
        self.text = "Remplissage de la table de références des dates clés..."
        self.progressbar += 1

        reference_key_date_filler.run(case)
        self.text = "Remplissage de la table des dates clés..."
        self.progressbar += 1
        key_date_filler.run(case)
        self.text = "Remplissage de la table des calculs de température..."
        self.progressbar += 1

        temperatures = average_temperature_filler.run(case)
        self.text = "Remplissage de la table des calculs de température repro..."
        self.progressbar += 1
        temperature_repro_filler.run(case, temperatures)
        self.text = "Remplissage de la table des calculs de toxicité.."
        self.progressbar += 1

        tox_table_filler.run(case)
        self.progressbar += 1
        if case==2:
            version_filler.run(case, date, comment)
        
        self.progressbar = self.progressbar_element["maximum"]
        self.text = "Terminé"

        tk.Button(master=self.master, text="OK", command=self.kill_window).grid(row=4, column=1, ipadx=30)

