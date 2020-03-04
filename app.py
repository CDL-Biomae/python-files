import tkinter as tk
from tkinter import filedialog
from tools import QueryScript
import env
from report import excel_main, word_main


def main_button():
    change_chosen_version()
    if len(campaign_list):
        if word_wanted.get():
            if not output_folder_path.get():
                output_browse_button()
            if not input_folder_path.get():
                input_browse_button()
            num_campaign_text.set(num_campaign_input.get())
            if num_campaign_text.get() == "":
                num_campaign_text.set("XX")
            for campaign in campaign_list:
                word_main(campaign, agence.get(),
                          input_folder_path.get(), output_folder_path.get(), num_campaign_text.get())
        if excel_wanted.get():
            if not output_folder_path.get():
                output_browse_button()
            excel_main(campaign_list, output_folder_path.get())


def change_chosen_version():
    version_file = open('version.txt', 'w')
    version_file.write(f'CHOSEN_VERSION={version_choice.get()}')
    version_file.close()


def add_campaign():
    is_existing = QueryScript(
        f"SELECT * FROM {env.DATABASE_RAW}.campaign WHERE reference='{campaign_input.get()}'").execute()
    if len(is_existing):
        if len(campaign_list):
            campaign_input_text.set(campaign_input_text.get() + '\n')
        campaign_input_text.set(
            campaign_input_text.get() + campaign_input.get().upper())
        campaign_list.append(campaign_input.get().upper())
    reset()


def enter(event):
    add_campaign()


def reset():
    campaign_input.delete(0, 'end')


def input_browse_button():
    global input_folder_path
    filename = tk.filedialog.askdirectory()
    input_folder_path.set(filename)


def output_browse_button():
    global output_folder_path
    filename = tk.filedialog.askdirectory()
    output_folder_path.set(filename)


version_file = open('version.txt', 'w')
version_file.write(f'CHOSEN_VERSION={env.LATEST_VERSION}')
version_file.close()

window = tk.Tk()
window.title('Digital Lab App')
window.geometry("540x360")
window.minsize(480, 360)

frame_campaign = tk.Frame(master=window)
tk.Label(master=frame_campaign, text='Nom de campagne').grid(row=0, column=0)
campaign_input = tk.Entry(frame_campaign)
campaign_list = []
campaign_input.grid(row=0, column=1)
campaign_button = tk.Button(master=frame_campaign,
                            text="Ajouter", command=add_campaign)
campaign_button.grid(row=0, column=2)
campaign_input_text = tk.StringVar()
tk.Label(master=frame_campaign, text='Campagne(s) choisie(s) :').grid(
    row=1, column=0)
tk.Label(master=frame_campaign, textvariable=campaign_input_text).grid(
    row=1, column=1)
tk.Label(master=frame_campaign, text='Version choisie :').grid(
    row=2, column=0)
version_choice = tk.StringVar()
version_choice.set(env.LATEST_VERSION)
version_menu = tk.OptionMenu(
    frame_campaign, version_choice, *env.ALL_VERSIONS).grid(row=2, column=1)

frame_campaign.pack(expand='YES')
window.bind('<Return>', enter)

tk.Label(master=frame_campaign, text='Numéro de la campagne').grid(
    row=3, column=0)
num_campaign_input = tk.Entry(frame_campaign)
num_campaign_input.grid(row=3, column=1)
num_campaign_text = tk.StringVar()

frame_choice = tk.Frame(master=window)
agence = tk.IntVar(0)
agence.set(1)
tk.Checkbutton(frame_choice, text="Agence de l'eau", variable=agence).pack()
excel_wanted = tk.IntVar(0)
tk.Checkbutton(frame_choice, text="Annexe du Rapport d'étude (Excel)",
               variable=excel_wanted).pack()
word_wanted = tk.IntVar(0)
tk.Checkbutton(frame_choice, text="Rapport d'étude (Word)",
               variable=word_wanted).pack()
launch_button = tk.Button(
    master=frame_choice, text="Lancer", command=main_button)
launch_button.pack()
frame_choice.pack(expand='YES')

frame_folder = tk.Frame(master=window)
output_folder_path = tk.StringVar()
output_folder_button = tk.Button(
    master=frame_folder, text="Choisir une destination ...", command=output_browse_button)
output_folder_button.pack()
tk.Label(master=frame_folder, textvariable=output_folder_path).pack()
input_folder_path = tk.StringVar()
input_folder_button = tk.Button(
    master=frame_folder, text="Choisir une source des photos ...", command=input_browse_button)
input_folder_button.pack()
tk.Label(master=frame_folder, textvariable=input_folder_path).pack()
frame_folder.pack(expand='YES')

window.mainloop()
