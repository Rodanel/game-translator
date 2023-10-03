import tkinter as tk
from ttkbootstrap import *
import ttkbootstrap as ttk

def set_frame_attrs(fr: ttk.Frame, root: tk.Tk):
    fr = ttk.Frame(root)
    fr.pack(side=TOP, fill=BOTH, expand=True, anchor=N)
    return fr