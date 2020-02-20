import tkinter as tk
from report import main

def main_button(campaign_input):
    print(campaign_input.get())

def reset():
    campaign_input.set()

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
campaign_name = tk.Label(master=frame_campaign, text='Nom de campagne').grid(row=0,column=0)
campaign_input = tk.Entry(frame_campaign).grid(row=0,column=1)
campaign_button = tk.Button(master=frame_campaign,text="Lancer", command=main_button).grid(row=1, column=0)
reset_button = tk.Button(master=frame_campaign,text="Effacer", command=reset).grid(row=1, column=1)
frame_campaign.pack(expand='YES')
window.bind('<Return>', main_button)

frame_folder = tk.Frame(master=window)
folder_button = tk.Button(master=frame_folder,text="Choisir une destination ...", command=browse_button)
folder_button.pack()
lbl1 = tk.Label(master=frame_folder,textvariable=folder_path).pack()
frame_folder.pack(expand='YES')

window.mainloop()
