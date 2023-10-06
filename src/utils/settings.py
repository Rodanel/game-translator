import json
from os import path, getcwd
from types import *
from src.games.detect_game import GameType
import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from src.utils.locale import Locale

class Settings(object):
    LANGUAGE_NAME = "languageName"
    LANGUAGE_FOLDER_NAME = "languageFolderName"
    LOCK_LOCALIZATION = "lockLocalization"
    EXTRACT_RPA = "extractRpaFiles"
    IGNORED_RPA_FILES = "ignoredRPAFiles"
    DECOMPİLE_RPYC = "decompileRpycFiles"
    OPTIMIZE_TEXTS = "optimizeTexts"
    FORCE_REGENERATE_TRANSLATION_FILES = "forceRegenerateTranslationFiles"
    TRANSLATE_WITH_GOOGLE_TRANSLATE = "translateWithGoogleTranslate"
    GOOGLE_TRANSLATE_LANGUAGE_CODE = "googleTranslateLanguageCode"

    LOCALE = "locale"

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
                Settings.OPTIMIZE_TEXTS: False,
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
            with open(self.__path__, "r", encoding="utf8") as outfile:
                self.data = json.load(outfile)
        else:
            self.data = json.loads("{}")
            self.save()
        self.__locale__ = Locale(locale=self.localeText)
    
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
    def localeText(self):
        if Settings.LOCALE not in self.data:
            self.data[Settings.LOCALE] = Locale.DEFAULT_LOCALE
            self.save()
        return self.data[Settings.LOCALE]
    @localeText.setter
    def localeText(self, value:str):
        self.data[Settings.LOCALE] = value
        self.save()
        self.__locale__ = Locale(locale=value)
        for upt in self.__onUpdates__:
            try:
                if upt[0] == Settings.LOCALE:
                    upt[1]()
            except:
                print("Settings not updated.")
        
    @property
    def locale(self) -> Locale:
        return self.__locale__
    def save_locale(self, locale):
        self.localeText = locale
        self.close_window()
    def save(self):
        map = json.dumps(self.data, indent=4, ensure_ascii=False)
        with open(self.__path__, "w" if path.exists(self.__path__) else "x", encoding="utf8") as outfile:
            outfile.write(map)
    def onUpdate(self, prop, func):
        self.__onUpdates__.append([prop, func])
    def close_window(self):
        if self.__window__ is not None:
            self.__window__.grab_release()
            self.__window__.destroy()
            self.__window__ = None
    def window(self, mainWindow: ttk.Window):
        if self.__window__ is None:
            self.__window__ = ttk.Toplevel(mainWindow)

            # set title
            self.__window__.title(self.locale.settings)
            _loc_x = mainWindow.winfo_x()
            _loc_y = mainWindow.winfo_y()
            _window_width = 300
            _window_height = 70
            # find the center point
            _center_x = int(_loc_x +(mainWindow.winfo_width() / 2) - (_window_width / 2))
            _center_y = int(_loc_y +(mainWindow.winfo_height() / 2) - (_window_height / 2))
            self.__window__.geometry(f'{_window_width}x{_window_height}+{_center_x}+{_center_y}')
            self.__window__.resizable(False, False)
            self.__window__.minsize(_window_width, _window_height)
            self.__window__.protocol("WM_DELETE_WINDOW", self.close_window)
            #self.__window__.pack(side="top", fill="both", expand=True)
            settingsMainFrame = ttk.Frame(self.__window__, padding=5)
            settingsMainFrame.pack(side=TOP, fill=BOTH, expand=True)
            settingsLocaleFrame = ttk.Frame(settingsMainFrame)
            settingsLocaleFrame.pack(side=TOP, fill=X, anchor=N)
            settingsLocaleLabel = ttk.Label(settingsLocaleFrame, text=self.locale.languageDot)
            settingsLocaleLabel.pack(side=LEFT)
            settingsMargin = ttk.Frame(settingsLocaleFrame, width=5)
            settingsMargin.pack(side=LEFT)
            settingsLocale = ttk.StringVar()
            settingsLocaleCombobox = ttk.Combobox(settingsLocaleFrame, textvariable=settingsLocale)
            settingsLocaleCombobox["values"] = self.locale.locales
            settingsLocale.set(self.localeText)
            settingsLocaleCombobox.pack(side=RIGHT, fill=X, expand=True)
            settingsLocaleCombobox["state"] = "readonly"
            settingsButtonsFrame = ttk.Frame(settingsMainFrame)
            settingsButtonsFrame.pack(side=BOTTOM, fill=X)
            settingsSaveButton = ttk.Button(settingsButtonsFrame, text=settings.locale.saveButton, bootstyle=SUCCESS, command=lambda:self.save_locale(settingsLocale.get()))
            settingsSaveButton.pack(side=RIGHT)
            settingsButtonsMargin = ttk.Frame(settingsButtonsFrame, width=5)
            settingsButtonsMargin.pack(side=RIGHT)
            settingsCancelButton = ttk.Button(settingsButtonsFrame, text=settings.locale.cancelButton, bootstyle=DANGER, command=self.close_window)
            settingsCancelButton.pack(side=RIGHT)
            self.__window__.grab_set()
            self.__window__.wait_window()
        else:
            messagebox.showwarning(settings.locale.alreadyActiveTitle, message=settings.locale.settingsWindowAlreadyActive)
settings = Settings()