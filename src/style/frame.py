from tkinter import Tk, Frame, BOTH, N

def set_frame_attrs(fr: Frame, root: Tk):
    fr = Frame(root)
    fr.pack(fill=BOTH, expand=True, anchor=N)
    return fr