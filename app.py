import tkinter as tk
from tkinter import filedialog
from report import excel_main

def main_button():
    print(campaign_input.get())

def enter(event):
    print(campaign_input.get())
    
def reset():
    campaign_input.set('')

def browse_button():
    global folder_path
    filename = tk.filedialog.askdirectory()
    folder_path.set(filename)
    print(filename)


window = tk.Tk()
window.title('Digital Lab App')
window.geometry("540x360")
window.minsize(480, 360)
folder_path = tk.StringVar()

frame_campaign = tk.Frame(master=window)
tk.Label(master=frame_campaign, text='Nom de campagne').grid(row=0,column=0)
campaign_input = tk.Entry(frame_campaign)
campaign_input.grid(row=0,column=1)
campaign_button = tk.Button(master=frame_campaign,text="Lancer", command=main_button)
campaign_button.grid(row=0, column=2)
frame_campaign.pack(expand='YES')
window.bind('<Return>', enter)

frame_folder = tk.Frame(master=window)
folder_button = tk.Button(master=frame_folder,text="Choisir une destination ...", command=browse_button)
folder_button.pack()
lbl1 = tk.Label(master=frame_folder,textvariable=folder_path).pack()
frame_folder.pack(expand='YES')

window.mainloop()
