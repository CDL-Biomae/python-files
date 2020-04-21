from log import MainApp

if __name__ =="__main__":
    app = MainApp()
    app.title("Digital Lab App")
    app.geometry("540x360+100+100")
    app.minsize(480, 360)
    if not app.has_to_quit:
        app.mainloop()
