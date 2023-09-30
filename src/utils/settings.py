import json
from os import path, getcwd
from types import *
from src.games.detect_game import GameType
from tkinter import *
from tkinter import ttk, messagebox
from src.style.buttons import enabledButtonColor, enabledRedButtonColor
from src.utils.languages.base import LanguageBase
from src.utils.languages.turkish import Turkish
from src.utils.languages.enum import Language

class Settings(object):
    LANGUAGE_NAME = "languageName"
    LANGUAGE_FOLDER_NAME = "languageFolderName"
    LOCK_LOCALIZATION = "lockLocalization"
    EXTRACT_RPA = "extractRpaFiles"
    IGNORED_RPA_FILES = "ignoredRPAFiles"
    DECOMPİLE_RPYC = "decompileRpycFiles"
    FORCE_REGENERATE_TRANSLATION_FILES = "forceRegenerateTranslationFiles"
    TRANSLATE_WITH_GOOGLE_TRANSLATE = "translateWithGoogleTranslate"
    GOOGLE_TRANSLATE_LANGUAGE_CODE = "googleTranslateLanguageCode"

    LANGUAGE = "language"

    @classmethod
    def getDefault(cls, gameType: GameType):
        if gameType == GameType.RENPY:
            return {
                Settings.LANGUAGE_NAME: "",
                Settings.LANGUAGE_FOLDER_NAME: "",
                Settings.LOCK_LOCALIZATION: False,
                Settings.EXTRACT_RPA: True,
                Settings.IGNORED_RPA_FILES: [],
                Settings.DECOMPİLE_RPYC: True,
                Settings.FORCE_REGENERATE_TRANSLATION_FILES: False,
                Settings.TRANSLATE_WITH_GOOGLE_TRANSLATE: False,
                Settings.GOOGLE_TRANSLATE_LANGUAGE_CODE: "",
            }
        else:
            return {}

    def __init__(self):
        self.__window__ = None
        self.__onUpdates__ = []
        self.__path__ = path.join(getcwd(), "settings.json")
        if path.exists(self.__path__):
            with open(self.__path__, "r") as outfile:
                self.data = json.load(outfile)
        else:
            self.data = json.loads("{}")
            self.save()
    
    def addDefaultGameSettingsIFNotExists(self, gameType: GameType, gameLocation: str, save: bool = True):
        if str(gameType) not in self.data:
            self.data[str(gameType)] = {}
        if gameLocation not in self.data[str(gameType)]:
            self.data[str(gameType)][gameLocation] = Settings.getDefault(gameType)
        if save:
            self.save()
    def updateGame(self, gameType: GameType, gameLocation:str, gameSettings: dict):
        self.addDefaultGameSettingsIFNotExists(gameType, gameLocation, save=False)
        for key, value in gameSettings.items():
            self.data[str(gameType)][gameLocation][key] = value
        self.save()
    
    @property
    def filePath(self):
        return self.__path__
    @property
    def languageText(self):
        if Settings.LANGUAGE not in self.data:
            self.data[Settings.LANGUAGE] = str(Language.ENGLISH)
            self.save()
        return self.data[Settings.LANGUAGE]
    @languageText.setter
    def languageText(self, value:str):
        self.data[Settings.LANGUAGE] = value
        self.save()
        for upt in self.__onUpdates__:
            try:
                if upt[0] == Settings.LANGUAGE:
                    upt[1]()
            except:
                print("Settings not updated.")
        
    @property
    def language(self) -> LanguageBase:
        return Language.fromStr(self.languageText)
    def save_language(self, language):
        self.languageText = language
        self.close_window()
    def save(self):
        map = json.dumps(self.data, indent=4)
        with open(self.__path__, "w" if path.exists(self.__path__) else "x") as outfile:
            outfile.write(map)
    def onUpdate(self, prop, func):
        self.__onUpdates__.append([prop, func])
    def close_window(self):
        if self.__window__ is not None:
            self.__window__.destroy()
            self.__window__ = None
    def window(self, mainWindow: Tk):
        if self.__window__ is None:
            self.__window__ = Toplevel(mainWindow)

            # set title
            self.__window__.title(self.language.settings)
            _screen_width = self.__window__.winfo_screenwidth()
            _screen_height = self.__window__.winfo_screenheight()
            _window_width = 300
            _window_height = 50
            # find the center point
            _center_x = int(_screen_width / 2 - _window_width / 2)
            _center_y = int(_screen_height / 2 - _window_height / 2)
            self.__window__.geometry(f'{_window_width}x{_window_height}+{_center_x}+{_center_y}')
            self.__window__.resizable(False, False)
            self.__window__.minsize(_window_width, _window_height)
            self.__window__.protocol("WM_DELETE_WINDOW", self.close_window)
            #self.__window__.pack(side="top", fill="both", expand=True)
            settingsLanguageFrame = Frame(self.__window__)
            settingsLanguageFrame.pack(side=TOP, fill=X, anchor=N)
            settingsLanguageLabel = Label(settingsLanguageFrame, text=self.language.languageDot)
            settingsLanguageLabel.pack(side=LEFT)
            settingsMargin = Frame(settingsLanguageFrame, width=5)
            settingsMargin.pack(side=LEFT)
            settingsLanguage = StringVar()
            settingsLanguageCombobox = ttk.Combobox(settingsLanguageFrame, textvariable=settingsLanguage)
            settingsLanguageCombobox["values"] = [str(Language.ENGLISH), str(Language.TURKISH)]
            settingsLanguage.set(self.languageText)
            settingsLanguageCombobox.pack(side=RIGHT, fill=X, expand=True)
            settingsLanguageCombobox["state"] = "readonly"
            settingsButtonsFrame = Frame(self.__window__)
            settingsButtonsFrame.pack(side="bottom", fill="x")
            settingsSaveButton = Button(settingsButtonsFrame, text=settings.language.saveButton, background=enabledButtonColor, foreground="white", command=lambda:self.save_language(settingsLanguage.get()))
            settingsSaveButton.pack(side="right")
            settingsButtonsMargin = Frame(settingsButtonsFrame, width=5)
            settingsButtonsMargin.pack(side="right")
            settingsCancelButton = Button(settingsButtonsFrame, text=settings.language.cancelButton, background=enabledRedButtonColor, foreground="white", command=self.close_window)
            settingsCancelButton.pack(side="right")
            self.__window__.wait_window()
        else:
            messagebox.showwarning("Already Active", message="Settings window already is active.")
settings = Settings()