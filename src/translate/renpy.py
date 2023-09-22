from os import path

from tkinter import StringVar, BooleanVar, Frame, Label, Entry, Checkbutton

from src.style.frame import set_frame_attrs


class RenpyFrame(object):

    def __init__(self, mainFrame: Frame, filename:str):
        self.__frame__ = None
        self.__filename__ = filename
        self.__languageName__ = StringVar()
        self.__lockLocalization__ = BooleanVar()
        set_frame_attrs(self.__frame__, mainFrame)
        self.__titleLabel__ = Label(self.__frame__, text="Renpy Game Translation")
        self.__titleLabel__.grid(column=0, row=0, columnspan=2, sticky='new')
        self.__gamePathLabel__ = Label(self.__frame__, text="Game: "+self.__filename__)
        self.__gamePathLabel__.grid(column=0, row=1, columnspan=2, sticky='new')
        self.__languageLabel__ = Label(self.__frame__, text="Language (only english characters):")
        self.__languageLabel__.grid(column=0, row=2, sticky='nw')
        self.__languageEntry__ = Entry(self.__frame__, textvariable=self.__languageName__)
        self.__languageEntry__.grid(column=1, row=2, sticky='new')
        self.__lockLocalizationCheck__ = Checkbutton(self.__frame__, text= "Lock translation. (Locks the game to this language. No need to update screens.rpy\nfile for adding language options if checked.)", variable=self.__lockLocalization__, onvalue=True, offvalue=False)
        self.__lockLocalizationCheck__.grid(column=0, row=3, columnspan=2, sticky="new")
    
    @property
    def frame(self) -> Frame:
        return self.__frame__
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
    def titleLabel(self) -> Label:
        return self.__titleLabel__
    @titleLabel.setter
    def titleLabel(self, value: Label):
        self.__titleLabel__ = value
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
    def languageEntry(self) -> Entry:
        return self.__languageEntry__
    @languageEntry.setter
    def languageEntry(self, value: Entry):
        self.__languageEntry__ = value
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
    return