from os import path, listdir, remove, rmdir
import re
import subprocess
import time

from tkinter import Tk, StringVar, BooleanVar, Frame, Label, Entry, Checkbutton, messagebox, scrolledtext, END, WORD

from src.tools.rpa import RpaEditor
from src.tools.unren import unren_content
from src.style.frame import set_frame_attrs

# renpy panel object
class RenpyFrame(object):

    def __init__(self, root: Tk, filename:str):
        self.__root__ = root
        self.__frame__ = None
        self.__filename__ = filename
        self.__frame__ = set_frame_attrs(self.__frame__, root)
        self.__titleLabel__ = Label(self.__frame__, text="Renpy Game Translation")
        self.__titleLabel__.pack(side="top", fill="x", anchor="n")
        self.__gamePathLabel__ = Label(self.__frame__, text="Game: "+self.__filename__)
        self.__gamePathLabel__.pack(side="top", fill="x", anchor="n")
        self.__languageFrame__ = Frame(self.__frame__)
        self.__languageFrame__.pack(side="top", fill="x", anchor="n")
        self.__languageLabel__ = Label(self.__languageFrame__, text="Language (only english characters):")
        self.__languageLabel__.pack(side="left")
        self.__languageName__ = StringVar()
        self.__languageEntry__ = Entry(self.__languageFrame__, textvariable=self.__languageName__)
        self.__languageEntry__.pack(side="right", fill="x", expand=True)
        self.__lockLocalization__ = BooleanVar()
        self.__lockLocalizationCheck__ = Checkbutton(self.__frame__, text= "Lock translation. (Locks the game to this language. No need to update screens.rpy\nfile for adding language options if checked.)", variable=self.__lockLocalization__, onvalue=True, offvalue=False)
        self.__lockLocalizationCheck__.pack(side="top", fill="x", anchor="n")
        
        self.__progressText__ = scrolledtext.ScrolledText(self.__frame__, wrap=WORD, state="disabled")
        self.__progressText__.pack(side="top", fill="both", expand=True)

    # element properties
    @property
    def root(self) -> Tk:
        return self.__root__
    @property
    def filename(self) -> str:
        return self.__filename__
    @property
    def languageName(self) -> str:
        return self.__languageName__.get()
    @property
    def lockLocalization(self) -> bool:
        return self.__lockLocalization__.get()
    @property
    def progress(self) -> str:
        return self.__progressText__.get(1.0, END)
    @progress.setter
    def progress(self, value: str):
        self.__progressText__["state"] = "normal"
        self.__progressText__.insert(END, "\n"+value)
        self.__progressText__.see(END)
        self.__progressText__["state"] = "disabled"
    def clearProgress(self):
        self.__progressText__["state"] = "normal"
        self.__progressText__.delete(1.0, END)
        self.__progressText__["state"] = "disabled"
    # hide renpy panel    
    def destroy(self):
        if self.__frame__ is not None:
            self.__frame__.pack_forget()
            self.__frame__.destroy()
        self.__frame__ = None
        self = None


def clear_temp_rpyc_decompilers(dirname, bat_path):
    if path.exists(bat_path):
        remove(bat_path)
    decompiler_path = path.join(dirname, "decompiler")
    if path.exists(decompiler_path):
        for decompiler_file in listdir(decompiler_path):
            remove(path.join(decompiler_path, decompiler_file))
    if path.exists(decompiler_path):
        rmdir(decompiler_path)
    _decomp_cab = path.join(dirname, "_decomp.cab")
    if path.exists(_decomp_cab):
        remove(_decomp_cab)
    _decomp_cab_tmp = path.join(dirname, "_decomp.cab.tmp")
    if path.exists(_decomp_cab_tmp):
        remove(_decomp_cab_tmp)
    deobfuscate_py = path.join(dirname, "deobfuscate.py")
    if path.exists(deobfuscate_py):
        remove(deobfuscate_py)
    deobfuscate_pyo = path.join(dirname, "deobfuscate.pyo")
    if path.exists(deobfuscate_pyo):
        remove(deobfuscate_pyo)
    unren_log = path.join(dirname, "unren.log")
    if path.exists(unren_log):
        remove(unren_log)
    unrpyc_py = path.join(dirname, "unrpyc.py")
    if path.exists(unrpyc_py):
        remove(unrpyc_py)
    unrpyc_pyo = path.join(dirname, "unrpyc.pyo")
    if path.exists(unrpyc_pyo):
        remove(unrpyc_pyo)

def translate(renpyFrame: RenpyFrame):
    skip_rpa = False
    skip_rpyc = False
    print(renpyFrame.filename+ " will be translated to "+renpyFrame.languageName+"! Lock localization: "+ str(renpyFrame.lockLocalization))
    dirname = path.dirname(renpyFrame.filename)
    if len(renpyFrame.languageName) > 0 and re.match('^[abcdefghijklmnoprqstuwvyzx]+$',renpyFrame.languageName):
        renpyFrame.clearProgress()
        gamedir = path.join(dirname, "game")
        exception_occurred = False
        if not skip_rpa:
            for fname in listdir(gamedir):
                fullpath = path.join(gamedir, fname)
                if fname.endswith(".rpa"):
                    #renpyFrame.start_loading()
                    try:
                        renpyFrame.progress = "Exracting "+fname+"..."
                        print("Exracting "+fname+"...")
                        RpaEditor(fullpath, _extract=True, _version=2)
                    except Exception as e:
                        exception_occurred = True
                        error_text = "Could not extract \""+fname+"\" archive.\n\nError: "+str(e)
                        renpyFrame.progress = error_text
                        messagebox.showerror("Could not extract archive", message=error_text)                    
                        break
        if not exception_occurred and not skip_rpyc:
            try:
                renpyFrame.progress = "Starting decompiling rpyc files..."
                bat_path = path.join(dirname, "unren.bat")
                clear_temp_rpyc_decompilers(dirname, bat_path)
                f = open(bat_path, "x")
                f.write(unren_content)
                f.close()
                CREATE_NO_WINDOW = 0x08000000
                spRpyc = subprocess.Popen(bat_path, cwd=dirname, stdout=subprocess.PIPE, bufsize=1, creationflags=CREATE_NO_WINDOW)
                while True:
                    line = spRpyc.stdout.readline()
                    if not line:
                        break
                    else:
                        if str(line).startswith("b'"):
                            line = str(line)[2:]
                        if str(line).startswith("b\""):
                            line = str(line)[1:]
                        if str(line).startswith("\\x0c "):
                            line = str(line)[5:]
                        if str(line).startswith("\\x0c"):
                            line = str(line)[4:]
                        if str(line).endswith("\\r\\n'"):
                            line = str(line)[:-5]
                        if str(line).endswith("'\\n\""):
                            line = str(line)[:-4] + "\""
                        if str(line).endswith("\\n'"):
                            line = str(line)[:-3]
                        renpyFrame.progress = str(line)
                renpyFrame.progress = "Decompiling rpyc files completed. Removing temp files."
                clear_temp_rpyc_decompilers(dirname, bat_path)
                time.sleep(3)
                renpyFrame.progress = "Decompiling completed!"
            except Exception as e:
                exception_occurred = True
                error_text = "Could not decompile rpyc files.\n\nError: "+str(e)
                renpyFrame.progress = error_text
                messagebox.showerror("Could not decompile", message=error_text)
        #renpyFrame.stop_loading()
    else:
        renpyFrame.progress = "Language name should be contain only english lowercase characters."
    return