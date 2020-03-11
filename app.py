import tkinter as tk
from tkinter import filedialog
from tools import QueryScript
import env
from report import excel_main, word_main
from database import fill
from datetime import date

class App(tk.Tk):
    
    def __init__(self):
        tk.Tk.__init__(self)
        self.mode = tk.StringVar()
        self.mode.set("creator")
        self.version_file = open("version.txt", "w")
        try :
            self.version_file.write(f"CHOSEN_VERSION={env.LATEST_VERSION()}")
            self.version_file.close()
            self.other_mode = tk.StringVar()
            self.other_mode.set("Gestionnaire de base de données")
            self.init_creator()
            self.has_to_quit = False
        except AttributeError:
            self.has_to_quit = True

    
    def switch_mode(self):
        if self.mode.get() == "creator":
            self.mode.set("database")
            self.other_mode.set("Créateur de livrable")
            self.frame_campaign.destroy()
            self.frame_choice.destroy()
            if self.word_showed.get():
                self.frame_end.destroy()
                self.frame_word.destroy()
            elif self.excel_showed.get():
                self.frame_end.destroy()
            self.init_database()
        elif self.mode.get() ==  "database":
            self.mode.set("creator")
            self.other_mode.set("Gestionnaire de base de données")
            self.frame_main.destroy()
            self.frame_reference.destroy()
            self.init_creator()
            
    #######################################################################
    #######################################################################     
            
    def init_creator(self):

        ##### Frame d"informations de campagnes et de version
        self.frame_campaign = tk.Frame(master=self)
        tk.Button(master=self.frame_campaign, textvariable=self.other_mode, command=self.switch_mode, background="#87CEFA").grid(row=0)
        tk.Label(master=self.frame_campaign, text="Nom de campagne").grid(row=1, column=0)
        self.campaign_input = tk.Entry(self.frame_campaign)
        self.campaign_list = []
        self.campaign_input.grid(row=1, column=1)
        self.campaign_button = tk.Button(master=self.frame_campaign,
                                    text="Ajouter", command=self.add_campaign)
        self.campaign_button.grid(row=1, column=2)
        self.campaign_input_text = tk.StringVar()
        tk.Label(master=self.frame_campaign, text="Campagne(s) choisie(s) :").grid(
            row=2, column=0)
        tk.Label(master=self.frame_campaign, textvariable=self.campaign_input_text).grid(
            row=2, column=1)
        tk.Label(master=self.frame_campaign, text="Version choisie :").grid(
            row=3, column=0)
        self.reset_button = tk.Button(master=self.frame_campaign,
                                    text="Annuler", command=self.reset_campaign)
        self.reset_button.grid(row=2, column=2)

        self.version_choice = tk.StringVar()
        self.version_choice.set(env.LATEST_VERSION())
        tk.OptionMenu(
            self.frame_campaign, self.version_choice, *env.ALL_VERSIONS()).grid(row=3, column=1)

        self.frame_campaign.pack()
        self.bind("<Return>", self.enter)
        self.word_showed =  tk.IntVar(0)
        self.excel_showed =  tk.IntVar(0)
        
        
        ########### Frame des checkbox des livrables

        self.frame_choice = tk.Frame(master=self)
        self.excel_wanted = tk.IntVar(0)
        tk.Checkbutton(self.frame_choice, text="Annexe du Rapport d'étude (Excel)",
                    variable=self.excel_wanted, command=self.choose_excel).pack()
        self.word_wanted = tk.IntVar(0)
        tk.Checkbutton(self.frame_choice, text="Rapport d'expérimentation (Word)",
                    variable=self.word_wanted, command=self.choose_word).pack()
        self.frame_choice.pack()
        
        ###########################################
        

        
    def main_button(self):
        self.change_chosen_version()
        if len(self.campaign_list):
            if self.word_wanted.get():
                if not self.output_folder_path.get():
                    self.output_browse_button()
                if not self.input_folder_path.get():
                    self.input_browse_button()
                self.num_campaign_text.set(self.campaign_input.get())
                if self.num_campaign_text.get() == "":
                    self.num_campaign_text.set("XX")
                for campaign in self.campaign_list:
                    word_main(campaign, self.agence.get(),
                            self.input_folder_path.get(), self.output_folder_path.get(), self.num_campaign_text.get())
            if self.excel_wanted.get():
                if not self.output_folder_path.get():
                    self.output_browse_button()
                excel_main(self.campaign_list, self.output_folder_path.get())

    def choose_word(self):
        if self.word_showed.get() :
            self.frame_word.destroy()
            self.word_showed.set(0)
            if not self.excel_showed.get():
                self.frame_end.destroy()
        else:
            if self.excel_showed.get():
                self.frame_end.destroy()
            self.frame_word = tk.Frame(master=self)
            self.frame_campaign_num = tk.Frame(master=self.frame_word) 
            tk.Label(master=self.frame_campaign_num, text="Numéro de la campagne").grid(
                row=0,column=0)
            self.num_campaign_input = tk.Entry(self.frame_campaign_num)
            self.num_campaign_input.grid(row=0,column=1)
            tk.Label(master=self.frame_campaign_num).grid(row=0,column=2)
            self.frame_campaign_num.grid(row=0)
            self.num_campaign_text = tk.StringVar()
            self.agence = tk.IntVar(0)
            tk.Checkbutton(self.frame_word, text="Agence de l'eau", variable=self.agence).grid(row=1)
            self.input_folder_path = tk.StringVar()
            self.input_folder_button = tk.Button(
                master=self.frame_word, text="Choisir une source des photos ...", command=self.input_browse_button)
            self.input_folder_button.grid(row=2)
            tk.Label(master=self.frame_word, textvariable=self.input_folder_path).grid(row=3)
            self.frame_word.pack()
            self.word_showed.set(1)
            self.show_end()
    
    def show_end(self):
        ######## Frame end

        self.frame_end = tk.Frame(master=self)
        self.output_folder_path = tk.StringVar()
        self.output_folder_button = tk.Button(
            master=self.frame_end, text="Choisir une destination ...", command=self.output_browse_button)
        self.output_folder_button.pack()
        tk.Label(master=self.frame_end, textvariable=self.output_folder_path).pack()
        self.frame_end.pack()
        self.launch_button = tk.Button(
            master=self.frame_end, text="Lancer", background="#32CD32", command=self.main_button)
        self.launch_button.pack()
        self.frame_end.pack(expand='YES')
    
        #################################

    def choose_excel(self):
        if not self.word_showed.get() :
            if self.excel_showed.get() :
                self.frame_end.destroy()
                self.excel_showed.set(0)
            else :
                self.show_end()
                self.excel_showed.set(1)
        else :
            if self.excel_showed.get() :
                self.excel_showed.set(0)
            else :
                self.excel_showed.set(1)




    def change_chosen_version(self):
        version_file = open("version.txt", "w")
        version_file.write(f"CHOSEN_VERSION={self.version_choice.get()}")
        version_file.close()


    def add_campaign(self):
        is_existing = QueryScript(
            f"SELECT * FROM {env.DATABASE_RAW}.Campaign WHERE reference='{self.campaign_input.get()}'").execute()
        if len(is_existing) and not self.campaign_input.get() in self.campaign_list :
            if self.campaign_input_text.get() != "":
                self.campaign_input_text.set(self.campaign_input_text.get() + "\n")
                self.campaign_input_text.set(self.campaign_input_text.get() + self.campaign_input.get().upper())
            else :
                self.campaign_input_text.set(self.campaign_input.get().upper())
            self.campaign_list.append(self.campaign_input.get().upper())
            self.reset_input()

    def reset_campaign(self):
        self.campaign_list
        self.campaign_list = []
        self.campaign_input_text.set("")

    def enter(self,event):
        self.add_campaign()


    def reset_input(self):
        self.campaign_input.delete(0, "end")


    def input_browse_button(self):
        filename = tk.filedialog.askdirectory()
        self.input_folder_path.set(filename)


    def output_browse_button(self):
        filename = tk.filedialog.askdirectory()
        self.output_folder_path.set(filename)
    
    #####################################################################
    #####################################################################
    
    
    def init_database(self):
        self.frame_main = tk.Frame(master=self)
        self.frame_main.pack(expand='YES')
        tk.Button(master=self.frame_main, textvariable=self.other_mode, command=self.switch_mode, background="#87CEFA").grid(row=0)
        tk.Label(master=self.frame_main, text="Des nouvelles données ont\n été insérées récemment dans \n la base de données brutes ?").grid(row=1, column=0)
        tk.Button(master=self.frame_main, text="Rafraîchir la base données traitées", command=self.refresh).grid(row=1,column=1)
        
        self.frame_reference = tk.Frame(master=self)
        self.frame_reference_1 = tk.Frame(master=self.frame_reference)
        tk.Label(master=self.frame_reference_1, text="Nouvelle version ? ").grid(row=0,column=0)
        
        self.reference_xl_path = tk.StringVar()
        tk.Button(master=self.frame_reference_1, text="Choisir le fichier excel de référence...", command=self.browse_reference_xl).grid(row=0,column=1)
        self.frame_reference_1.pack(expand='YES')
        
        
        self.frame_reference_2 = tk.Frame(master=self.frame_reference)
        tk.Label(master=self.frame_reference_2, textvariable=self.reference_xl_path).grid(row=0)
        self.frame_reference_2.pack(expand='YES')
        
        self.frame_reference.pack(expand='YES')
        
        
    def browse_reference_xl(self):
        filename = tk.filedialog.askopenfilename()
        self.reference_xl_path.set(filename)
        tk.Button(master=self.frame_reference_2, text="Ajouter cette version", background="#32CD32", command=self.add_new_version).grid(row=1)
        self.version_date = tk.Label(master=self.frame_reference_1, text=date.today().strftime("%d/%m/%Y")).grid(row=1, column=0)
        self.version_comment = tk.Entry(master=self.frame_reference_1)
        self.version_comment.insert(0,'Commentaire...')
        self.version_comment.grid(row=1, column=1)
        
        
        
        
    def refresh(self):
        fill.run(2)
    
    def add_new_version(self):
        fill.run(3, xl_path=self.reference_xl_path.get(), date=date.today().strftime("%d/%m/%Y"), comment=self.version_comment.get())
        




if __name__ == "__main__":
    app = App()
    app.title("Digital Lab App")
    app.geometry("540x360")
    app.minsize(480, 360)
    if not app.has_to_quit:
        app.mainloop()
