import tkinter as tk
from tkinter import filedialog
from report import main

def main_button():
    print(campaign_input.get())
    print(word.get(), excel.get())
    campaign_input.delete(0,'end')

def enter(event):
    main_button()

def browse_output_button():
    
    filename = tk.filedialog.askdirectory()
    output_path.set(filename)
    print(filename)

def browse_input_button():
    
    filename = tk.filedialog.askdirectory()
    input_path.set(filename)
    print(filename)


window = tk.Tk()
window.title('Digital Lab App')
window.geometry("540x360")
window.minsize(480, 360)
window.iconbitmap("cdl.ico")
folder_path = tk.StringVar()

frame_campaign = tk.Frame(master=window)
tk.Label(master=frame_campaign, text='Nom de campagne').grid(row=0,column=0)
campaign_input = tk.Entry(frame_campaign)
campaign_input.grid(row=0,column=1)
campaign_button = tk.Button(master=frame_campaign,text="Lancer", command=main_button)
campaign_button.grid(row=0, column=2)
agence = tk.IntVar()
agence.set(1)
agence_button = tk.Checkbutton(
        master=frame_campaign, text="Agence de l'eau", variable=agence)
agence_button.grid(row=1, column=1)
frame_campaign.pack(expand='YES')
window.bind('<Return>', enter)

frame_word_excel = tk.Frame(window)
tk.Label(master=frame_word_excel, text='Livrable').grid(row=0)
word = tk.IntVar()
word_button = tk.Checkbutton(
        master=frame_word_excel, text="Word", variable=word)
word_button.grid(row=1)
excel = tk.IntVar()
excel_button = tk.Checkbutton(
        master=frame_word_excel, text="Excel", variable=excel)
excel_button.grid(row=2)
frame_word_excel.pack(expand='YES')

frame_folder = tk.Frame(master=window)
output_path = tk.StringVar()
output_button = tk.Button(master=frame_folder,text="Choisir une destination de sortie", command=browse_output_button)
output_button.pack()
tk.Label(master=frame_folder,textvariable=output_path).pack()
input_path = tk.StringVar()
input_button = tk.Button(master=frame_folder,text="Choisir le dossier des photos", command=browse_input_button)
input_button.pack()
tk.Label(master=frame_folder,textvariable=input_path).pack()
frame_folder.pack(expand='YES')

window.mainloop()
