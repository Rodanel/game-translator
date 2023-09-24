from os import path, listdir, remove, rmdir
import re
import subprocess
import time

from tkinter import Tk, StringVar, BooleanVar, Frame, Label, Entry, Checkbutton, messagebox

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
        
        self.__timer_id__ = None
        self.__progress__ = StringVar()
        self.__progressLabel__ = Label(self.__frame__, textvariable=self.__progress__, wraplength=450)
        self.__progressLabel__.pack(side="top", fill="both", expand=True)

    def start_loading(self, n=0):
        if self.progress.endswith("..."):
            self.progress = self.progress[:-2]
        elif self.progress.endswith(".."):
            self.progress = self.progress + "."
        elif self.progress.endswith("."):
            self.progress = self.progress + "."
        self.__timer_id__ = self.frame.after(500, self.start_loading, n+1)
    def stop_loading(self):
        if self.__timer_id__:
            self.frame.after_cancel(self.__timer_id__)

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
    def progressDefault(self):
        self.__progressLabel__["foreground"] = "black"
    def progressRed(self):
        self.__progressLabel__["foreground"] = "red"
    @property
    def progress(self) -> str:
        return self.__progress__.get()
    @progress.setter
    def progress(self, value: str):
        return self.__progress__.set(value)

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
        renpyFrame.progressDefault()
        gamedir = path.join(dirname, "game")
        exception_occurred = False
        if not skip_rpa:
            for fname in listdir(gamedir):
                fullpath = path.join(gamedir, fname)
                if fname.endswith(".rpa"):
                    renpyFrame.start_loading()
                    try:
                        renpyFrame.progress = "Exracting "+fname+"..."
                        print("Exracting "+fname+"...")
                        RpaEditor(fullpath, _extract=True, _version=2)
                    except Exception as e:
                        renpyFrame.progress = ""
                        exception_occurred = True
                        messagebox.showerror("Could not extract archive", message="Could not extract \""+fname+"\" archive.\n\nError: "+str(e))                    
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
                counter = 0
                while True:
                    line = spRpyc.stdout.readline()
                    counter += 1
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
                    if counter < 5:
                        renpyFrame.progress = renpyFrame.progress+"\n"+str(line)
                    else:
                        renpyFrame.progress = line
                        counter = 0
                    if not line: break
                renpyFrame.progress = "Decompiling rpyc files completed. Removing temp files."
                clear_temp_rpyc_decompilers(dirname, bat_path)
                time.sleep(3)
                renpyFrame.progress = "Decompiling completed!"
            except Exception as e:
                renpyFrame.progress = ""
                exception_occurred = True
                messagebox.showerror("Could not decompile", message="Could not decompile rpyc files.\n\nError: "+str(e))
        renpyFrame.stop_loading()
    else:
        renpyFrame.progressRed()
        renpyFrame.progress = "Language name should be contain only english lowercase characters."
    return