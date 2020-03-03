import tkinter as tk
from tkinter import filedialog
from report import excel_main, word_main
from tools import QueryScript
import env


def main_button():
    if len(campaign_list):
        if word_wanted.get():
            if not output_folder_path.get():
                output_browse_button()
            if not input_folder_path.get():
                input_browse_button()
            for campaign in campaign_list:
                word_main(campaign, agence.get(),
                          input_folder_path.get(), output_folder_path.get())
        if excel_wanted.get():
            if not output_folder_path.get():
                output_browse_button()
            excel_main(campaign_list, output_folder_path.get())

        reset()


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


def next_version():
    print('oui')


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
tk.Label(master=frame_campaign, text=env.VERSION).grid(
    row=2, column=0)
version_button = tk.Button(
    master=frame_campaign, text="+", command=next_version)
version_button.grid(row=2, column=1)

frame_campaign.pack(expand='YES')
window.bind('<Return>', enter)

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
