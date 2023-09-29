import json
from os import path, getcwd
from types import *
from src.games.detect_game import GameType

class Settings(object):
    LANGUAGE_NAME = "languageName"
    LANGUAGE_FOLDER_NAME = "languageFolderName"
    LOCK_LOCALIZATION = "lockLocalization"
    EXTRACT_RPA = "extractRpaFiles"
    DECOMPİLE_RPYC = "decompileRpycFiles"
    FORCE_REGENERATE_TRANSLATION_FILES = "forceRegenerateTranslationFiles"
    TRANSLATE_WITH_GOOGLE_TRANSLATE = "translateWithGoogleTranslate"
    GOOGLE_TRANSLATE_LANGUAGE_CODE = "googleTranslateLanguageCode"

    @classmethod
    def getDefault(cls, gameType: GameType):
        if gameType == GameType.RENPY:
            return {
                Settings.LANGUAGE_NAME: "",
                Settings.LANGUAGE_FOLDER_NAME: "",
                Settings.LOCK_LOCALIZATION: False,
                Settings.EXTRACT_RPA: True,
                Settings.DECOMPİLE_RPYC: True,
                Settings.FORCE_REGENERATE_TRANSLATION_FILES: False,
                Settings.TRANSLATE_WITH_GOOGLE_TRANSLATE: False,
                Settings.GOOGLE_TRANSLATE_LANGUAGE_CODE: "",
            }
        else:
            return {}

    def __init__(self):
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
    def save(self):
        map = json.dumps(self.data, indent=4)
        with open(self.__path__, "w" if path.exists(self.__path__) else "x") as outfile:
            outfile.write(map)
settings = Settings()