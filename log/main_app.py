import tkinter as tk
import webbrowser
from tkinter import filedialog, messagebox
from tools import QueryScript
import env
from datetime import datetime
from time import sleep
from .log_excel import LogExcelApp
from .log_word import LogWordApp
from .log_database import LogDatabaseApp
from .log_excel_EDI import LogExcelEDIApp


class MainApp(tk.Tk):
    
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
            tk.messagebox.showerror(title="Erreur", message="Impossible de se connecter à la base de données. \nCela peut venir de votre connection internet ou de votre VPN.")

    
    def switch_mode(self):
        if self.mode.get() == "creator":
            self.mode.set("database")
            self.other_mode.set("Créateur de livrable")
            self.frame_campaign.destroy()
            try :
                self.frame_empty.destroy()
            except AttributeError :
                pass
            try :
                self.frame_end.destroy()
            except AttributeError :
                pass
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

        self.frame_campaign.pack(expand="YES")
        self.bind("<Return>", self.enter)
        self.create_empty_space()
        self.photos_path = None
        self.agency = False
        self.campaign_number = 'XX' 
    
    def create_empty_space(self):
        self.frame_empty = tk.Frame(master=self)
        for _ in range(4):
            tk.Label(master=self.frame_empty, text=" \n").pack()
        self.frame_empty.pack(expand='YES')

    def quit_window(self):
        if self.log_window:
            self.log_window.destroy()    
    class ComplementDataApp(tk.Tk):
        def __init__(self, master=None, campaign_list=""):
            self.master = master
            tk.Label(master=self.master, text="    ").grid(row=0,column=0)
            tk.Label(master=self.master,text=f"Création du rapport d'expérimentation").grid(row=1,column=1,columnspan=2, sticky="w")
            self.agency = tk.IntVar()
            tk.Checkbutton(master, text="Agence", variable=self.agency).grid(row=2, column=1, sticky="w")
            self.photos_path = None
            tk.Label(master=self.master, text="Numéro de campagne").grid(row=3, column=1, sticky="w")
            self.campaign_number = tk.StringVar()
            self.campaign_number_entry = tk.Entry(master=self.master, textvariable=self.campaign_number).grid(row=3, column=2, sticky="w")
            tk.Label(master=self.master,text="Source des photos ").grid(row=4,column=1, sticky="w")
            tk.Button(master=self.master,text="Parcourir", command=self.photos_browse_button).grid(row=4,column=2, sticky="w")
            self.path = tk.StringVar()
            tk.Label(master=self.master, textvariable=self.path).grid(row=5,column=1,columnspan=2)
            tk.Label(master=self.master, text="    ").grid(row=6,column=0)

        def photos_browse_button(self):
            self.photos_path = tk.filedialog.askdirectory()
            self.master.master.photos_path = self.photos_path
            self.path.set(self.photos_path)
            if self.photos_path:
                tk.Button(master=self.master, text="Lancer", command=self.kill_window).grid(row=6, column=1, columnspan=2, ipadx=30)
            
        def kill_window(self):
            self.master.master.agency = self.agency.get()
            self.master.master.campaign_number = self.campaign_number.get()
            self.master.master.launch_word()
            self.master.destroy()

    def launch_word(self):
        if not self.photos_path:
            self.complement_data = tk.Toplevel(self)
            self.complement_data.transient(self)
            self.complement_data.geometry('350x200+150+150')
            self.complement_data_app = self.ComplementDataApp(master=self.complement_data, campaign_list=self.campaign_list)
        else :
            if self.complement_data :
                self.complement_data.destroy()
            for campaign in self.campaign_list:
                self.output_path = tk.filedialog.asksaveasfilename(title=f"Enregistrer le rapport d'expérimentation {campaign}",filetypes=[("Word (*.docx)","*.docx")], defaultextension=".docx", initialfile=f"Rapport d'expérimentation {campaign}")
                if not self.output_path:
                    return None

                self.change_chosen_version(self.version_choice.get())
                self.log_window = tk.Toplevel(self)
                self.log_window.transient(self)
                self.log_window.geometry('400x150+150+150')
                try :
                    self.log_app = LogWordApp(master=self.log_window, campaign=campaign, agency=self.agency,photos_path=self.photos_path, output_path=self.output_path, campaign_number=self.campaign_number)
                    self.output_path = None
                    self.photos_path = None
                    self.campaign_number = None
                except PermissionError :
                    self.log_window.destroy()
                    tk.messagebox.showerror(title="Erreur", message=f"Veuillez fermer le fichier \'{self.output_path.split('/')[-1]}\' avant de lancer.")
                except Exception as err :
                    self.log_window.destroy()
                    tk.messagebox.showerror(title="Erreur", message=err)
    def launch_excel(self): 

        self.output_path = tk.filedialog.asksaveasfilename(title="Enregistrer le rapport excel",filetypes=[("Excel (*.xslx)","*.xlsx")], defaultextension=".xlsx", initialfile=f"Rapport annexe {' '.join(self.campaign_list)}")
        if not self.output_path:
            return None
        self.change_chosen_version(self.version_choice.get())
        self.log_window = tk.Toplevel(self)
        self.log_window.transient(self)
        self.log_window.geometry('400x150+150+150')
        try :
            self.log_app = LogExcelApp(master=self.log_window, campaign_list=self.campaign_list, output_path=self.output_path)
            self.output_path = None
        except PermissionError :
            self.log_window.destroy()
            tk.messagebox.showerror(title="Erreur", message=f"Veuillez fermer le fichier \'{self.output_path.split('/')[-1]}\' avant de lancer.")
        except Exception as err :
            self.log_window.destroy()
            tk.messagebox.showerror(title="Erreur", message=err)

    def launch_edi(self): 

        for campaign in self.campaign_list:
            self.output_path = tk.filedialog.asksaveasfilename(title=f"Enregistrer le rapport EDI",filetypes=[("Excel (*.xlsx)","*.xlsx")], defaultextension=".xlsx", initialfile=f"Rapport EDI pour {campaign}")
            if not self.output_path:
                return None

            self.change_chosen_version(self.version_choice.get())
            self.log_window = tk.Toplevel(self)
            self.log_window.transient(self)
            self.log_window.geometry('400x150+150+150')
            try :
                self.log_app = LogExcelEDIApp(master=self.log_window, campaign=campaign,output_path=self.output_path)
                self.output_path = None
            except PermissionError :
                self.log_window.destroy()
                tk.messagebox.showerror(title="Erreur", message=f"Veuillez fermer le fichier \'{self.output_path.split('/')[-1]}\' avant de lancer.")
            except Exception as err :
                self.log_window.destroy()
                tk.messagebox.showerror(title="Erreur", message=err)
 
    def show_end(self):
        ######## Frame end
        self.frame_empty.destroy()
        self.frame_end = tk.Frame(master=self)
        self.launch_excel_button = tk.Button(
            master=self.frame_end, text="Rapport annexe", fg="#FFFFFF", background="#008000", command=self.launch_excel)
        self.launch_excel_button.pack()
        tk.Label(master=self.frame_end, text="").pack()
        self.launch_word_button = tk.Button(
            master=self.frame_end, text="Rapport d'expérimentation", fg="#FFFFFF", background="#0060AC", command=self.launch_word)
        self.launch_word_button.pack()
        tk.Label(master=self.frame_end, text="").pack()
        self.launch_edi_button = tk.Button(
            master=self.frame_end, text="Rapport EDI", fg="#FFFFFF", background="#008000", command=self.launch_edi)
        self.launch_edi_button.pack()
        self.frame_end.pack(expand='YES')


    def choose_version(self):
        self.version_choice.set(self.version_choice.get())

    def change_chosen_version(self, version=None):
        version_file = open("version.txt", "w")
        version_file.write(f"CHOSEN_VERSION={version}")
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
                self.show_end()
            self.campaign_list.append(self.campaign_input.get().upper())
            self.reset_input()

    def reset_campaign(self):
        if len(self.campaign_list) :
            self.campaign_list = [] 
            self.campaign_input_text.set("")
            self.frame_end.destroy()
            self.create_empty_space()

    def enter(self,event):
        self.add_campaign()


    def reset_input(self):
        self.campaign_input.delete(0, "end")



    def output_browse_button(self):
        campagn_list = self.campaign_list
        filename = tk.filedialog.asksaveasfilename(title="Enregistrer le rapport excel",filetypes=[("Excel (*.xlsx)","*.xlsx")], defaultextension=".xlsx", initialfile=f"Rapport d'annexe {' '.join(self.campagn_list)}")
        self.output_folder_path.set(filename)
    
    #####################################################################
    #####################################################################
    
    
    def init_database(self):
        self.frame_main = tk.Frame(master=self)
        self.frame_main.pack(expand='YES')
        tk.Button(master=self.frame_main, textvariable=self.other_mode, command=self.switch_mode, background="#87CEFA").grid(row=0)
        tk.Label(master=self.frame_main, text="Des nouvelles données ont\n été insérées récemment dans \n la base de données brutes ?").grid(row=1, column=0)
        tk.Button(master=self.frame_main, text="Rafraîchir la base données traitées", command=self.refresh).grid(row=1,column=1)
        tk.Label(master=self.frame_main, text="Version à mettre à jour :").grid(row=2, column=0)
        self.version_choice = tk.StringVar()
        self.version_choice.set(env.LATEST_VERSION())
        options_list = env.ALL_VERSIONS()
        options_list.append('toutes')
        options = tuple(options_list)
        tk.OptionMenu(
            self.frame_main, self.version_choice, *options).grid(row=2, column=1)
        
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
        self.version_date = tk.Label(master=self.frame_reference_1, text=datetime.now().strftime("%d/%m/%Y %H:%M:%S")).grid(row=1, column=0)
        self.version_comment = tk.Entry(master=self.frame_reference_1)
        self.version_comment.insert(0,'Commentaire...')
        self.version_comment.grid(row=1, column=1)
        
        
        
    def manage_database(self, case=0, xl_path=None, date=None, comment=None):
        self.change_chosen_version(self.version_choice.get())
        self.log_window = tk.Toplevel(self)
        self.log_window.transient(self)
        self.log_window.geometry('400x150+150+150')
        try :
            self.log_app = LogDatabaseApp(self.log_window, case, xl_path, date, comment)
        except Exception as err :
            tk.messagebox.showerror(title="Erreur", message=err)
    def refresh(self):
        if self.version_choice.get()=='toutes':
            for version in env.ALL_VERSIONS():
                self.change_chosen_version(version)
                self.manage_database(case=2)
        else :
            self.change_chosen_version(self.version_choice.get())
            self.manage_database(case=2)
    
    def add_new_version(self):
        self.change_chosen_version(max(env.ALL_VERSIONS())+1)
        self.manage_database(case=3, xl_path=self.reference_xl_path.get(), date=datetime.now().strftime("%d/%m/%Y %H:%M:%S"), comment=self.version_comment.get())
        

