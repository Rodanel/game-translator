from os import path, listdir
import re, threading

from tkinter import Tk, StringVar, BooleanVar, Frame, Label, Entry, Checkbutton, messagebox

from src.tools.rpa import RpaEditor
from src.style.frame import set_frame_attrs

class RenpyFrame(object):

    def __init__(self, root: Tk, mainFrame: Frame, filename:str):
        self.__root__ = root
        self.__frame__ = None
        self.__filename__ = filename
        self.__frame__ = set_frame_attrs(self.__frame__, mainFrame)
        self.__titleLabel__ = Label(self.__frame__, text="Renpy Game Translation")
        self.__titleLabel__.grid(column=0, row=0, columnspan=2, sticky='new')
        self.__progress__ = StringVar()
        self.__timer_id__ = None
        self.__progressLabel__ = Label(self.__frame__, textvariable=self.__progress__)
        self.__progressLabel__.grid(column=0, row=1, columnspan=2, sticky='new')
        self.__gamePathLabel__ = Label(self.__frame__, text="Game: "+self.__filename__)
        self.__gamePathLabel__.grid(column=0, row=2, columnspan=2, sticky='new')
        self.__languageLabel__ = Label(self.__frame__, text="Language (only english characters):")
        self.__languageLabel__.grid(column=0, row=3, sticky='nw')
        self.__languageName__ = StringVar()
        self.__languageEntry__ = Entry(self.__frame__, textvariable=self.__languageName__)
        self.__languageEntry__.grid(column=1, row=3, sticky='new')
        self.__lockLocalization__ = BooleanVar()
        self.__lockLocalizationCheck__ = Checkbutton(self.__frame__, text= "Lock translation. (Locks the game to this language. No need to update screens.rpy\nfile for adding language options if checked.)", variable=self.__lockLocalization__, onvalue=True, offvalue=False)
        self.__lockLocalizationCheck__.grid(column=0, row=4, columnspan=2, sticky="new")

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

    @property
    def root(self) -> Tk:
        return self.__root__
    @property
    def frame(self) -> Frame:
        return self.__frame__
    @property
    def filename(self) -> str:
        return self.__filename__
    @property
    def titleLabel(self) -> Label:
        return self.__titleLabel__
    @titleLabel.setter
    def titleLabel(self, value: Label):
        self.__titleLabel__ = value
    def progressDefault(self):
        self.progressLabel["foreground"] = "black"
    def progressRed(self):
        self.progressLabel["foreground"] = "red"
    @property
    def progress(self) -> str:
        return self.__progress__.get()
    @progress.setter
    def progress(self, value: str):
        return self.__progress__.set(value)
    @property
    def progressLabel(self) -> Label:
        return self.__progressLabel__
    @progressLabel.setter
    def progressLabel(self, value: Label):
        self.__progressLabel__ = value
    @property
    def gamePathLabel(self) -> Label:
        return self.__gamePathLabel__
    @gamePathLabel.setter
    def gamePathLabel(self, value: Label):
        self.__gamePathLabel__ = value
    @property
    def languageLabel(self) -> Label:
        return self.__languageLabel__
    @languageLabel.setter
    def languageLabel(self, value: Label):
        self.__languageLabel__ = value
    @property
    def languageName(self) -> str:
        return self.__languageName__.get()
    @property
    def languageEntry(self) -> Entry:
        return self.__languageEntry__
    @languageEntry.setter
    def languageEntry(self, value: Entry):
        self.__languageEntry__ = value
    @property
    def lockLocalization(self) -> bool:
        return self.__lockLocalization__.get()
    @property
    def lockLocalizationCheck(self) -> Checkbutton:
        return self.__lockLocalizationCheck__
    @lockLocalizationCheck.setter
    def lockLocalizationCheck(self, value: Checkbutton):
        self.__lockLocalizationCheck__ = value
    
    def destroy(self):
        if self.titleLabel is not None:
            self.titleLabel.destroy()
        self.titleLabel = None
        if self.gamePathLabel is not None:
            self.gamePathLabel.destroy()
        self.gamePathLabel = None
        if self.languageLabel is not None:
            self.languageLabel.destroy()
        self.languageLabel = None
        if self.languageEntry is not None:
            self.languageEntry.destroy()
        self.languageEntry = None
        if self.lockLocalizationCheck is not None:
            self.lockLocalizationCheck.destroy()
        self.lockLocalizationCheck = None
        if self.frame is not None:
            self.frame.destroy()
        self.frame = None
        self = None



def translate(renpyFrame: RenpyFrame):
    print(renpyFrame.filename+ " will be translated to "+renpyFrame.languageName+"! Lock localization: "+ str(renpyFrame.lockLocalization))
    dirname = path.dirname(renpyFrame.filename)
    if len(renpyFrame.languageName) > 0 and re.match('^[abcdefghijklmnoprqstuwvyzx]+$',renpyFrame.languageName):
        renpyFrame.progressDefault()
        gamedir = path.join(dirname, "game")
        exception_occurred = False
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
        if not exception_occurred:
            renpyFrame.progress = "Rpa archives exracted successfully!"
        renpyFrame.stop_loading()
    else:
        renpyFrame.progressRed()
        renpyFrame.progress = "Language name should be contain only english lowercase characters."
    return