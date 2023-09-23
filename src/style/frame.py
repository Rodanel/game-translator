from tkinter import Frame

def set_frame_attrs(fr: Frame, mainFrame: Frame):
    fr = Frame(mainFrame)
    fr.grid(column=0, row=0, sticky='nesw')
    #fr.grid_rowconfigure(1, weight=1)
    #fr.grid_columnconfigure(1, weight=1)
    return fr