import os
from os import path, listdir, remove, rmdir, environ as myenv, mkdir, walk
import shutil
import zipfile
import signal
import re
import subprocess
import time
from datetime import datetime
import sys
import random
import string
import googletrans
from googletrans import Translator
import traceback
import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap import ScrolledText, Checkbutton
from ttkbootstrap.constants import *
import time

from src.games.detect_game import GameType
from src.games.renpy.rpa import RpaEditor
from src.games.renpy.unrpyc import unren_content
from src.style.frame import set_frame_attrs
from src.utils.settings import settings, Settings

CREATE_NO_WINDOW = 0x08000000


translator = Translator()
translator = Translator(service_urls=['translate.googleapis.com'])


def fsencode(s):
    """
    :doc: file_rare
    :name: renpy.fsencode

    Converts s from unicode to the filesystem encoding.
    """

    if not isinstance(s, str):
        return s

    fsencoding = sys.getfilesystemencoding() or "utf-8"
    return s.encode(fsencoding, "replace")

def fsdecode(s):
    """
    :doc: file_rare
    :name: renpy.fsdecode

    Converts s from filesystem encoding to unicode.
    """

    if not isinstance(s, str):
        return s

    fsencoding = sys.getfilesystemencoding() or "utf-8"
    #return s.decode(fsencoding)
    return s
def fix_console(line):
    line = str(line)
    if line.startswith("b'") or line.startswith("b\""):
        line = line[2:]
    if line.startswith("\\x0c"):
        line = line[4:]
    if line.endswith("\\r\\n'") or line.endswith("\\r\\n\""):
        line = line[:-5]
    elif line.endswith("\\n\"") or line.endswith("\\n'"):
        line = line[:-3]
    line = line.replace("\\\\", "\\")
    return line.strip()

# renpy panel object
class RenpyFrame(object):
        
    def __init__(self, root: ttk.Window, filename:str):

        self.__cancelled__ = False
        self.__decompileRpycProcess__ = None
        self.__generateTranslationProcess__ = None

        self.__rpaeditor__ = None
        self.__root__ = root
        self.__frame__ = None
        self.__filename__ = filename
        settings.addDefaultGameSettingsIFNotExists(GameType.RENPY, self.dirname)
        self.__frame__ = set_frame_attrs(self.__frame__, root)
        wrap_length = 500
        tb_width = 40
        self.__titleLabel__ = ttk.Label(self.__frame__, text=settings.locale.renpyGameTranslation, wraplength=wrap_length)
        self.__titleLabel__.pack(side="top", anchor="center")
        self.__gamePathLabel__ = ttk.Label(self.__frame__, text=settings.locale.gameName(gamePath=self.dirname), wraplength=wrap_length)
        self.__gamePathLabel__.pack(side="top", anchor="center")
    
        self.__languageNameFrame__ = ttk.Frame(self.__frame__)
        self.__languageNameFrame__.pack(side="top", fill="x", anchor="n")
        self.__languageNameLabel__ = ttk.Label(self.__languageNameFrame__, text=settings.locale.languageNameDot)
        self.__languageNameLabel__.pack(side="left", anchor="e")
        self.__languageName__ = ttk.StringVar()
        self.__languageNameEntry__ = ttk.Entry(self.__languageNameFrame__, textvariable=self.__languageName__, width=tb_width)
        self.__languageNameEntry__.pack(side="right")
    
        self.__languageFolderNameFrame__ = ttk.Frame(self.__frame__)
        self.__languageFolderNameFrame__.pack(side="top", fill="x", anchor="n")
        self.__languageFolderNameLabel__ = ttk.Label(self.__languageFolderNameFrame__, text=settings.locale.languageFolderNameDot)
        self.__languageFolderNameLabel__.pack(side="left", anchor="e")
        self.__languageFolderName__ = ttk.StringVar()
        self.__languageFolderNameEntry__ = ttk.Entry(self.__languageFolderNameFrame__, textvariable=self.__languageFolderName__, width=tb_width)
        self.__languageFolderNameEntry__.pack(side="right")
        
        self.__lockLocalization__ = ttk.BooleanVar()
        self.__lockLocalizationCheck__ = ttk.Checkbutton(self.__frame__, style="Roundtoggle.Toolbutton", padding=5, text=settings.locale.lockTranslation, variable=self.__lockLocalization__, onvalue=True, offvalue=False)
        self.__lockLocalizationCheck__.pack(side="top", fill="x", anchor="n")
        self.__extractRpaArchives__ = ttk.BooleanVar()
        self.__extractRpaArchivesCheck__ = ttk.Checkbutton(self.__frame__, style="Roundtoggle.Toolbutton", padding=5, text=settings.locale.extractRPAArhives, variable=self.__extractRpaArchives__, onvalue=True, offvalue=False)
        self.__extractRpaArchivesCheck__.pack(side="top", fill="x", anchor="n")
        self.__extractRpaArchives__.set(True)

        self.__ignoredRpaFilesFrame__ = ttk.Frame(self.__frame__)
        self.__ignoredRpaFilesFrame__.pack(side="top", fill="x", anchor="n")
        self.__ignoredRpaFile__ = ttk.StringVar()
        self.__ignoredRpaFilesCombobox__ = ttk.Combobox(self.__ignoredRpaFilesFrame__, textvariable=self.__ignoredRpaFile__)
        _rpaFiles = [path.basename(fname) for fname in listdir(self.gamedir) if fname.endswith(".rpa")]
        self.__ignoredRpaFilesCombobox__.pack(side="left", fill="x", anchor="w", expand=True)
        self.__ignoredRpaFilesCombobox__["values"] = _rpaFiles
        self.__ignoredRpaFilesCombobox__["state"] = "readonly"
        if len(_rpaFiles) > 0:
            self.__ignoredRpaFile__.set(_rpaFiles[0])
        self.__ignoredRpaFileText__ = ttk.StringVar()
        self.__ignoredRpaFileListLabel__ = ttk.Label(self.__frame__, textvariable=self.__ignoredRpaFileText__, wraplength=wrap_length)
        self.__ignoredRpaFileListLabel__.pack(side="top", anchor="center")
        
        self.__ignoredRpaFilesRemoveButton__ = ttk.Button(self.__ignoredRpaFilesFrame__, bootstyle=DANGER, text=settings.locale.remove, command=self.__remove_IgnoredRPAFile)
        self.__ignoredRpaFilesRemoveButton__.pack(side="right")
        self.__ignoredRpaFilesMargin1__ = ttk.Frame(self.__ignoredRpaFilesFrame__, width=2)
        self.__ignoredRpaFilesMargin1__.pack(side="right")
        self.__ignoredRpaFilesAddButton__ = ttk.Button(self.__ignoredRpaFilesFrame__, bootstyle=SUCCESS, text=settings.locale.add, command=self.__add_IgnoredRPAFile)
        self.__ignoredRpaFilesAddButton__.pack(side="right")
        self.__ignoredRpaFilesMargin2__ = ttk.Frame(self.__ignoredRpaFilesFrame__, width=2)
        self.__ignoredRpaFilesMargin2__.pack(side="right")

        self.__decompileRpycFiles__ = ttk.BooleanVar()
        self.__decompileRpycFilesCheck__ = ttk.Checkbutton(self.__frame__, style="Roundtoggle.Toolbutton", padding=5, text=settings.locale.decompileRPYCFiles, variable=self.__decompileRpycFiles__, onvalue=True, offvalue=False)
        self.__decompileRpycFilesCheck__.pack(side="top", fill="x", anchor="n")
        self.__decompileRpycFiles__.set(True)

        self.__optimizeTexts__ = ttk.BooleanVar()
        self.__optimizeTextsCheck__ = ttk.Checkbutton(self.__frame__, style="Roundtoggle.Toolbutton", padding=5, text=settings.locale.optimizeTexts, variable=self.__optimizeTexts__, onvalue=True, offvalue=False)
        self.__optimizeTextsCheck__.pack(side="top", fill="x", anchor="n")

        self.__forceRegenerateTranslation__ = ttk.BooleanVar()
        self.__forceRegenerateTranslationCheck__ = ttk.Checkbutton(self.__frame__, style="Roundtoggle.Toolbutton", padding=5, text=settings.locale.forceRegenerateTranslation, variable=self.__forceRegenerateTranslation__, onvalue=True, offvalue=False)
        self.__forceRegenerateTranslationCheck__.pack(side="top", fill="x", anchor="n")
        
        self.__translateWithGoogleTranslate__ = ttk.BooleanVar()
        self.__translateWithGoogleTranslateCheck__ = ttk.Checkbutton(self.__frame__, style="Roundtoggle.Toolbutton", padding=5, text=settings.locale.translateWithGoogle, variable=self.__translateWithGoogleTranslate__, onvalue=True, offvalue=False)
        self.__translateWithGoogleTranslateCheck__.pack(side="top", fill="x")
        self.__googleTranslateFrame__ = ttk.Frame(self.__frame__)
        self.__googleTranslateFrame__.pack(side="top", anchor="c")
        self.__googleTranslateLanguageLabel__ = ttk.Label(self.__googleTranslateFrame__, text=settings.locale.translateToDot)
        self.__googleTranslateLanguageLabel__.pack(side="left")
        self.__googleTranslateLanguage__ = ttk.StringVar()
        self.__googleTranslateLanguageCombobox__ = ttk.Combobox(self.__googleTranslateFrame__, textvariable=self.__googleTranslateLanguage__)
        self.__googleTranslateLanguageCombobox__["values"] = [key.capitalize() for key, value in googletrans.LANGCODES.items()]
        self.__googleTranslateLanguageCombobox__.pack(side="left")
        self.__googleTranslateLanguageCombobox__["state"] = "disabled"

        self.__progressText__ = ScrolledText(self.__frame__, wrap=WORD, state="disabled", height=10)
        self.__progressText__.pack(side="top", fill="x")
        self.__progressOrj__ = ""
        self.__update_props()
        settings.onUpdate(Settings.LOCALE, self.update_widget_texts)
    # element properties
    @property
    def root(self) -> ttk.Window:
        return self.__root__
    @property
    def filename(self) -> str:
        return self.__filename__
    @property
    def dirname(self) -> str:
        return path.dirname(self.filename)
    @property
    def gamedir(self) -> str:
        return path.join(self.dirname, "game")
    @property
    def tldir(self) -> str:
        return path.join(self.gamedir, "tl")
    @property
    def tlfilesdir(self) -> str:
        return path.join(self.gamedir, "tl", self.languageFolderName)
    @property
    def unrenfile(self) -> str:
        return path.join(self.dirname, "unren.bat")
    @property
    def languageName(self) -> str:
        return self.__languageName__.get()
    @property
    def languageFolderName(self) -> str:
        return self.__languageFolderName__.get()
    @property
    def extractRpaArchives(self) -> bool:
        return self.__extractRpaArchives__.get()
    @property
    def ignoredRpaFile(self):
        return self.__ignoredRpaFile__.get()
    @property
    def decompileRpycFiles(self) -> bool:
        return self.__decompileRpycFiles__.get()
    @property
    def optimizeTexts(self)-> bool:
        return self.__optimizeTexts__.get()
    @property
    def forceRegenerateTranslation(self) -> bool:
        return self.__forceRegenerateTranslation__.get()
    @property
    def lockLocalization(self) -> bool:
        return self.__lockLocalization__.get()
    @property
    def translatewithGoogleTranslate(self) -> bool:
        return self.__translateWithGoogleTranslate__.get()
    @property
    def googleTranslateLanguage(self) -> str:
        return self.__googleTranslateLanguage__.get()
    @property
    def progressOrj(self) -> str:
        return self.__progressOrj__
    @progressOrj.setter
    def progressOrj(self, value: str) -> str:
        self.__progressOrj__ += "\n"+value
    @progressOrj.deleter
    def progressOrj(self) -> str:
        self.__progressOrj__ = ""
    @property
    def progress(self) -> str:
        return self.__progressText__.get(1.0, END)
    @progress.setter
    def progress(self, value: str):
        self.__progressText__["state"] = "normal"
        self.__progressText__.insert(END, "\n"+value)
        self.__progressText__.see(END)
        self.__progressText__["state"] = "disabled"
    @property
    def commentline(self) -> str:
        return "# Generated by \"Game Translator by Rodanel\""
    @property
    def cancelled(self) -> bool:
        return self.__cancelled__
    @cancelled.setter
    def cancelled(self, value:bool):
        self.__cancelled__ = value
    
    def update_widget_texts(self):
        self.__titleLabel__["text"] = settings.locale.renpyGameTranslation
        self.__gamePathLabel__["text"] = settings.locale.gameName(gamePath=self.dirname)
        self.__languageNameLabel__["text"] = settings.locale.languageNameDot
        self.__languageFolderNameLabel__["text"] = settings.locale.languageFolderNameDot
        self.__lockLocalizationCheck__["text"] = settings.locale.lockTranslation
        self.__extractRpaArchivesCheck__["text"] = settings.locale.extractRPAArhives
        self.__ignoredRpaFilesRemoveButton__["text"] = settings.locale.remove
        self.__ignoredRpaFilesAddButton__["text"] = settings.locale.add
        self.__decompileRpycFilesCheck__["text"] = settings.locale.decompileRPYCFiles
        self.__optimizeTextsCheck__["text"] = settings.locale.optimizeTexts
        self.__forceRegenerateTranslationCheck__["text"] = settings.locale.forceRegenerateTranslation
        self.__translateWithGoogleTranslateCheck__["text"] = settings.locale.translateWithGoogle
        self.__googleTranslateLanguageLabel__["text"] = settings.locale.translateToDot
        self.__restore_ignoredRpaFiles()

    def __save_languageName(self, *args):
        self.__save_setting(Settings.LANGUAGE_NAME, self.__languageName__)
    def __save_languageFolderName(self, *args):
        self.__save_setting(Settings.LANGUAGE_FOLDER_NAME, self.__languageFolderName__)
    def __save_lockLocalization(self, *args):
        self.__save_setting(Settings.LOCK_LOCALIZATION, self.__lockLocalization__)
    def __save_extractRpaArchives(self, *args):
        self.__save_setting(Settings.EXTRACT_RPA, self.__extractRpaArchives__)
        self.__update_ignoreRpafilesState()
    def __update_ignoreRpafilesState(self, disabled:bool= False):
        if disabled:
            self.__ignoredRpaFilesCombobox__["state"] = "disabled"
            self.__ignoredRpaFilesAddButton__["state"] = "disabled"
            self.__ignoredRpaFilesRemoveButton__["state"] = "disabled"
            self.__ignoredRpaFileListLabel__["state"] = "disabled"
        else:
            self.__ignoredRpaFilesCombobox__["state"] = "readonly" if self.extractRpaArchives else "disabled"
            self.__ignoredRpaFilesAddButton__["state"] = "normal" if self.extractRpaArchives else "disabled"
            self.__ignoredRpaFilesRemoveButton__["state"] = "normal" if self.extractRpaArchives else "disabled"
            self.__ignoredRpaFileListLabel__["state"] = "normal" if self.extractRpaArchives else "disabled"
    def __restore_ignoredRpaFiles(self):
        _files = self.__get_ignored_files()
        _rpaFilesText = settings.locale.ignoredRPAArchivesSeperator.join(_files) if len(_files) > 0 else settings.locale.noFileAdded
        self.__ignoredRpaFileText__.set(settings.locale.ignoredRPAArchives(archiveFileListSeperated=_rpaFilesText))
    def __add_IgnoredRPAFile(self):
        if len(self.ignoredRpaFile) > 0:
            _files = self.__get_ignored_files()
            if self.ignoredRpaFile not in _files:
                _files.append(self.ignoredRpaFile)
                settings.updateGame(GameType.RENPY, self.dirname, {Settings.IGNORED_RPA_FILES: _files})
                self.__restore_ignoredRpaFiles()
    def __remove_IgnoredRPAFile(self):
        if len(self.ignoredRpaFile) > 0:
            _files = self.__get_ignored_files()
            if self.ignoredRpaFile in _files:
                _files.remove(self.ignoredRpaFile)
                settings.updateGame(GameType.RENPY, self.dirname, {Settings.IGNORED_RPA_FILES: _files})
                self.__restore_ignoredRpaFiles()
    def __get_ignored_files(self):
        _files = []
        try:
            defaultSettings = Settings.getDefault(GameType.RENPY)
            gameSettings = settings.data[str(GameType.RENPY)][self.dirname]
            _files = gameSettings[Settings.IGNORED_RPA_FILES] if Settings.IGNORED_RPA_FILES in gameSettings else defaultSettings[Settings.IGNORED_RPA_FILES]
        except:
            pass
        return _files
    def __save_decompileRpycFiles(self, *args):
        self.__save_setting(Settings.DECOMPİLE_RPYC, self.__decompileRpycFiles__)
    def __save_optimizeTexts(self, *args):
        self.__save_setting(Settings.OPTIMIZE_TEXTS, self.__optimizeTexts__)
    def __save_forceRegenerateTranslation(self, *args):
        self.__save_setting(Settings.FORCE_REGENERATE_TRANSLATION_FILES, self.__forceRegenerateTranslation__)
    def __save_translateWithGoogleTranslate(self, *args):
        self.__save_setting(Settings.TRANSLATE_WITH_GOOGLE_TRANSLATE, self.__translateWithGoogleTranslate__)
        self.__update_googleTranslateLanguageState()
    def __save_googleTranslateLanguage(self, *args):
        self.__save_setting(Settings.GOOGLE_TRANSLATE_LANGUAGE, self.__googleTranslateLanguage__)
    def __update_googleTranslateLanguageState(self, disabled:bool= False):
        if disabled:
            self.__googleTranslateLanguageLabel__["state"] = "disabled"
            self.__googleTranslateLanguageCombobox__["state"] = "disabled"
        else:
            self.__googleTranslateLanguageLabel__["state"] = "normal" if self.translatewithGoogleTranslate else "disabled"
            self.__googleTranslateLanguageCombobox__["state"] = "readonly" if self.translatewithGoogleTranslate else "disabled"
    def __disable_all_controls(self, disabled: bool = True):
        self.__languageNameLabel__["state"] = "disabled" if disabled else "normal"
        self.__languageNameEntry__["state"] = "disabled" if disabled else "normal"
        self.__languageFolderNameLabel__["state"] = "disabled" if disabled else "normal"
        self.__languageFolderNameEntry__["state"] = "disabled" if disabled else "normal"
        self.__lockLocalizationCheck__["state"] = "disabled" if disabled else "normal"
        self.__extractRpaArchivesCheck__["state"] = "disabled" if disabled else "normal"
        self.__update_ignoreRpafilesState(disabled)
        self.__decompileRpycFilesCheck__["state"] = "disabled" if disabled else "normal"
        self.__optimizeTextsCheck__["state"] = "disabled" if disabled else "normal"
        self.__forceRegenerateTranslationCheck__["state"] = "disabled" if disabled else "normal"
        self.__translateWithGoogleTranslateCheck__["state"] = "disabled" if disabled else "normal"
        self.__update_googleTranslateLanguageState(disabled)

    def __save_setting(self, propType, prop):
        settings.updateGame(GameType.RENPY, self.dirname, {propType: prop.get()})
    def __restore_setting(self, propType, prop):
        try:
            defaultSettings = Settings.getDefault(GameType.RENPY)
            gameSettings = settings.data[str(GameType.RENPY)][self.dirname]
            prop.set(gameSettings[propType] if propType in gameSettings else defaultSettings[propType])
        except Exception as e:
            print("Could not restore setting: "+propType)
            print(traceback.format_exc())

    def __update_props(self):
        self.__restore_setting(Settings.LANGUAGE_NAME, self.__languageName__)
        self.__languageName__.trace_add("write", self.__save_languageName)
        
        self.__restore_setting(Settings.LANGUAGE_FOLDER_NAME, self.__languageFolderName__)
        self.__languageFolderName__.trace_add("write", self.__save_languageFolderName)

        self.__restore_setting(Settings.LOCK_LOCALIZATION, self.__lockLocalization__)
        self.__lockLocalization__.trace_add("write", self.__save_lockLocalization)

        self.__restore_setting(Settings.EXTRACT_RPA, self.__extractRpaArchives__)
        self.__extractRpaArchives__.trace_add("write", self.__save_extractRpaArchives)
        
        self.__restore_ignoredRpaFiles()
        self.__update_ignoreRpafilesState()

        self.__restore_setting(Settings.DECOMPİLE_RPYC, self.__decompileRpycFiles__)
        self.__decompileRpycFiles__.trace_add("write", self.__save_decompileRpycFiles)

        self.__restore_setting(Settings.OPTIMIZE_TEXTS, self.__optimizeTexts__)
        self.__optimizeTexts__.trace_add("write", self.__save_optimizeTexts)

        self.__restore_setting(Settings.FORCE_REGENERATE_TRANSLATION_FILES, self.__forceRegenerateTranslation__)
        self.__forceRegenerateTranslation__.trace_add("write", self.__save_forceRegenerateTranslation)

        self.__restore_setting(Settings.TRANSLATE_WITH_GOOGLE_TRANSLATE, self.__translateWithGoogleTranslate__)
        self.__translateWithGoogleTranslate__.trace_add("write", self.__save_translateWithGoogleTranslate)

        self.__restore_setting(Settings.GOOGLE_TRANSLATE_LANGUAGE, self.__googleTranslateLanguage__)
        self.__googleTranslateLanguage__.trace_add("write", self.__save_googleTranslateLanguage)
        self.__update_googleTranslateLanguageState()

    def clearProgress(self):
        self.__progressText__["state"] = "normal"
        self.__progressText__.delete(1.0, END)
        del self.progressOrj
        self.__progressText__["state"] = "disabled"

    def save_progress(self):
        now = datetime.now()
        logsdir = path.join(path.dirname(self.filename), "game_translator-logs")
        if not path.isdir(logsdir):
            mkdir(logsdir)
        log_file_path = path.join(logsdir, "game_translator-log-"+now.strftime("%m-%d-%Y, %H-%M-%S")+".txt")
        log_file = open(log_file_path, "x")
        log_file.write("Game Translator by Rodanel Logs\nDate: "+now.strftime("%m/%d/%Y, %H:%M:%S")+"\n\n"+self.progressOrj)
        log_file.close()
        self.progress = ""
        self.progress = settings.locale.logfileEndDescription(filePath=log_file_path)
    def clear_temp_rpyc_decompilers(self):
        if path.exists(self.unrenfile):
            remove(self.unrenfile)
        cache_path = path.join(self.dirname, "__pycache__")
        if path.exists(cache_path):
            shutil.rmtree(cache_path)
        decompiler_path = path.join(self.dirname, "decompiler")
        if path.exists(decompiler_path):
            shutil.rmtree(decompiler_path)
        _decomp_cab = path.join(self.dirname, "_decomp.cab")
        if path.exists(_decomp_cab):
            remove(_decomp_cab)
        _decomp_cab_tmp = path.join(self.dirname, "_decomp.cab.tmp")
        if path.exists(_decomp_cab_tmp):
            remove(_decomp_cab_tmp)
        deobfuscate_py = path.join(self.dirname, "deobfuscate.py")
        if path.exists(deobfuscate_py):
            remove(deobfuscate_py)
        deobfuscate_pyo = path.join(self.dirname, "deobfuscate.pyo")
        if path.exists(deobfuscate_pyo):
            remove(deobfuscate_pyo)
        unren_log = path.join(self.dirname, "unren.log")
        if path.exists(unren_log):
            remove(unren_log)
        unrpyc_py = path.join(self.dirname, "unrpyc.py")
        if path.exists(unrpyc_py):
            remove(unrpyc_py)
        unrpyc_pyo = path.join(self.dirname, "unrpyc.pyo")
        if path.exists(unrpyc_pyo):
            remove(unrpyc_pyo)
    def generate_random_rpy_name(self, length:int):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))+".rpy"
    
    def __extract_rpa_archives(self):
        if self.cancelled:
            return True
        _ignoredFiles = self.__get_ignored_files()
        if self.extractRpaArchives:
            for fname in listdir(self.gamedir):
                if self.cancelled:
                    return True
                fullpath = path.join(self.gamedir, fname)
                if fname.endswith(".rpa"):
                    if path.basename(fname) not in _ignoredFiles:
                        try:
                            self.progressOrj = settings.locale.base.extractingFile(fileName=fname)
                            self.progress = settings.locale.extractingFile(fileName=fname)
                            print("Exracting "+fname+"...")
                            self.__rpaeditor__ = RpaEditor(fullpath, _extract=True, _version=2)
                            self.__rpaeditor__.start()
                            if self.cancelled:
                                return True
                            self.progressOrj = settings.locale.base.extractedFileSuccess(fileName=fname)
                            self.progress = settings.locale.extractedFileSuccess(fileName=fname)
                        except:
                            error_text = traceback.format_exc()
                            print(error_text)
                            self.progressOrj = settings.locale.base.extractFileError(filePath=fname, error=error_text)
                            self.progress = settings.locale.extractFileError(filePath=fname, error=error_text)
                            messagebox.showerror(settings.locale.extractFileErrorTitle, message=settings.locale.extractFileError(filePath=fname))               
                            return False
                    else:
                        self.progressOrj = settings.locale.base.ignoredFileWarning(fileName=fname)
                        self.progress = settings.locale.ignoredFileWarning(fileName=fname) 
        return True

    def __fix_decompile_rpyc_files_line(self, text, translate:bool=True):
        _loc = settings.locale
        if not translate:
            _loc = settings.locale.base
        if text == "No script files to decompile.":
            return _loc.noScriptFiles
        elif text == "Searching for rpyc files...":
            return _loc.searchingForRpycFiles
        else:
            p1 = re.compile('Decompiling (.*) to (.*)...')
            result1 = p1.search(text)
            if result1 is not None:
                return _loc.decompilingRpycTo(rpycFilePath=result1.group(1), rpyFilePath=result1.group(2))
            else:
                p2 = re.compile('Error while decompiling (.*):',)
                result2 = p2.search(text)
                if result2 is not None:
                    return _loc.decompilingRpycError(filePath=result2.group(1))
                else:
                    p3 = re.compile('File not found: (.*)')
                    result3 = p3.search(text)
                    if result3 is not None:
                        return _loc.fileNotFound(filePath=result3.group(1))
                    else:
                        p4 = re.compile('Decompilation of (.*) script file(.*)successful')
                        result4 = p4.search(text)
                        if result4 is not None:
                            return _loc.decompileRpycSuccess(fileCount=result4.group(1))
                        else:
                            p5 = re.compile('Decompilation of (.*) file(.*)failed')
                            result5 = p5.search(text)
                            if result5 is not None:
                                return _loc.decompileRpycFailed(fileCount=result5.group(1), isMultipleFiles=True if result5.group(2) == "s " else False)
                            else:
                                p6 = re.compile('Decompilation of (.*) file(.*)successful, but decompilation of (.*) file(.*)failed')
                                result6 = p6.search(text)
                                if result6 is not None:
                                    return _loc.decompileRpycSuccessAndFail(successFileCount=result6.group(1), failFileCount=result6.group(3))
                                else:
                                    p7 = re.compile('(.*) already exists - skipped')
                                    result7 = p7.search(text)
                                    if result7 is not None:
                                        if translate:
                                            return _loc.decompilingRpycFileSkipped(rpycFilePath=result7.group(1))
                                    else:
                                        p8 = re.compile('Working in: (.*)')
                                        result8 = p8.search(text)
                                        if result8 is not None:
                                            return _loc.workingIn(folderPath=result8.group(1))
        return text
    def __decompile_rpyc_files(self):
        if self.cancelled:
            return True
        if self.decompileRpycFiles:
            showErrorInProgress = True
            try:
                self.progressOrj = settings.locale.base.decompilingRpyc
                self.progress = settings.locale.decompilingRpyc
                unren_bat_file = open(self.unrenfile, "x")
                unren_bat_file.write(unren_content)
                unren_bat_file.close()
                self.__decompileRpycProcess__ = subprocess.Popen(self.unrenfile+ " decompile", cwd=self.dirname, stdout=subprocess.PIPE, creationflags=CREATE_NO_WINDOW)
                while True:
                    if self.cancelled:
                        return True
                    line = self.__decompileRpycProcess__.stdout.readline()
                    if not line:
                        break
                    else:
                        lineResp = self.__fix_decompile_rpyc_files_line(fix_console(line), translate=False)
                        if "Powershell is required, unable to continue" in lineResp:
                            self.progressOrj = settings.locale.base.requiresPowershell
                            self.progress = settings.locale.requiresPowershell
                            showErrorInProgress = False
                            raise Exception(settings.locale.requiresPowershell)
                        else:
                            self.progressOrj = lineResp
                            self.progress = self.__fix_decompile_rpyc_files_line(fix_console(line))
                self.progressOrj = settings.locale.base.decompilingRpycCompleted
                self.progress = settings.locale.decompilingRpycCompleted
                self.clear_temp_rpyc_decompilers()
                time.sleep(3)
                self.progressOrj = settings.locale.base.removedTmpFiles
                self.progress = settings.locale.removedTmpFiles
            except:
                self.clear_temp_rpyc_decompilers()
                error_text = traceback.format_exc()
                print(error_text)
                if showErrorInProgress:
                    self.progressOrj = settings.locale.base.decompileRpycError(error=error_text)
                    self.progress = settings.locale.decompileRpycError(error=error_text)
                messagebox.showerror(settings.locale.decompileRpycErrorTitle, message=settings.locale.decompileRpycError())
                return False
        return True
    
    def __optimize_texts(self):
        if self.cancelled:
            return True
        if self.optimizeTexts:
            try:
                self.progressOrj = settings.locale.base.startedOptimizingTexts
                self.progress = settings.locale.startedOptimizingTexts
                exclude = set(["tl"])
                for _path, _subdirs, _files in walk(self.gamedir, topdown=True):
                    if self.cancelled:
                        return True
                    _subdirs[:] = [d for d in _subdirs if d not in exclude]
                    for _name in _files:
                        if self.cancelled:
                            return True
                        if _name.endswith(".rpy"):
                            reallocation = path.join(_path, _name)
                            self.progressOrj = settings.locale.base.optimizingFile(filePath=reallocation)
                            self.progress = settings.locale.optimizingFile(filePath=reallocation)
                            with open(reallocation, "r") as rpyFile:
                                rpyText = str(rpyFile.read())
                            rpyFile.closed
                            p = re.compile(r'text "([^"]*)"')
                            result = p.findall(rpyText)
                            p2 = re.compile(r'textbutton "([^"]*)"')
                            result2 = p2.findall(rpyText)
                            result.extend(result2)
                            for res in result:
                                rpyText = rpyText.replace("text \""+res+"\"","text _(\""+res+"\")").replace("textbutton \""+res+"\"","textbutton _(\""+res+"\")")
                            if self.cancelled:
                                return True
                            if len(result) > 0:
                                with open(reallocation, "w") as rpyFile2:
                                    rpyFile2.write(rpyText)
                                rpyFile2.closed
                            self.progressOrj = settings.locale.base.optimizedTextAndButtons(count=len(result))
                            self.progress = settings.locale.optimizedTextAndButtons(count=len(result))
            except:         
                error_text = traceback.format_exc()
                print(error_text)
                self.progressOrj = settings.locale.base.optimizeTextsErrorDesc(error=error_text)
                self.progress = settings.locale.optimizeTextsErrorDesc(error=error_text)
                messagebox.showerror(settings.locale.errorTitle, message=settings.locale.optimizeTextsErrorDesc())
                return False
        return True

    def __generate_translation_files(self):
        if self.cancelled:
            return True
        try:
            if path.exists(self.tlfilesdir) and not self.forceRegenerateTranslation:
                self.progressOrj = settings.locale.base.translationSkipped
                self.progress = settings.locale.translationSkipped
            else:
                if path.exists(self.tlfilesdir) and self.forceRegenerateTranslation:
                    self.progressOrj = settings.locale.base.regeneratingTranslation
                    self.progress = settings.locale.regeneratingTranslation
                else:
                    self.progressOrj = settings.locale.base.generatingTranslation
                    self.progress = settings.locale.generatingTranslation
                executable_path = path.dirname(fsdecode(self.filename))
                game_extension = ".exe" if self.filename.endswith(".exe") else ""
                executables = [ "python"+game_extension]
                executables.append(self.filename)
                for i in executables:
                    executable = path.join(executable_path, i)
                    if path.exists(executable):
                        break
                else:
                    raise Exception("Python interpreter not found: %r", executables)
                #cmd = [ executable, "-EO", sys.argv[0] ]
                cmd = [ executable]
                args = [ "translate", self.languageFolderName ]
                cmd.append(self.dirname)
                cmd.extend(args)

                environ = dict(myenv)
                environ.update({})
                if hasattr(sys, "renpy_executable"):
                    environ = { k : v for k, v in environ.items() if not k.startswith("PYTHON") }
                encoded_environ = { }

                for k, v in environ.items():
                    if v is None:
                        continue

                    encoded_environ[str(k)] = str(v)

                # Launch the project.
                cmd = [ str(i) for i in cmd ]
                if self.cancelled:
                    return True
                self.__generateTranslationProcess__ = subprocess.Popen(cmd, stdout=subprocess.PIPE, creationflags=CREATE_NO_WINDOW,env=encoded_environ)
                generate_error_occurred = False
                while True:
                    if self.cancelled:
                        return True
                    line = self.__generateTranslationProcess__.stdout.readline()
                    if not line:
                        break
                    else:
                        if len(line.strip()) > 0 and not generate_error_occurred:
                            generate_error_occurred = True
                        self.progressOrj = fix_console(line)
                        self.progress = fix_console(line)
                if generate_error_occurred:
                    raise Exception("")
                else:
                    self.progressOrj = settings.locale.base.generatedTranslation
                    self.progress = settings.locale.generatedTranslation
                    return True
        except:
            error_text = traceback.format_exc()
            print(error_text)
            self.progressOrj = settings.locale.base.generatingTranslationError(error=error_text)
            self.progress = settings.locale.generatingTranslationError(error=error_text)
            messagebox.showerror(settings.locale.generatingTranslationErrorTitle, message=settings.locale.generatingTranslationError())
            return False
        return True
    def __google_translate(self):
        if self.cancelled:
            return True
        try:
            if self.translatewithGoogleTranslate:
                translated_comment = "# translated"
                if path.exists(self.tlfilesdir):
                    for _path, _subdirs, _files in walk(self.tlfilesdir):
                        if self.cancelled:
                            return True
                        for _name in _files:
                            if self.cancelled:
                                return True
                            reallocation = path.join(_path, _name)
                            if path.isfile(reallocation) and reallocation.endswith(".rpy"):
                                self.progressOrj = settings.locale.base.translating(filePath=reallocation)
                                self.progress = settings.locale.translating(filePath=reallocation)
                                with open(reallocation, "r+") as tlfile:
                                    file_lines = tlfile.readlines()
                                    if file_lines[len(file_lines)-1].strip().startswith(translated_comment):
                                        self.progressOrj = settings.locale.base.translatingSkipped(filePath=reallocation)
                                        self.progress = settings.locale.translatingSkipped(filePath=reallocation)
                                    else:
                                        translatable_texts = {}
                                        for file_line_i in range(len(file_lines)):
                                            if self.cancelled:
                                                tlfile.closed
                                                return True
                                            file_line_text = str(file_lines[file_line_i])
                                            file_line_stripped = file_line_text.strip()
                                            if not file_line_stripped.startswith("#") and not file_line_stripped.startswith("translate ") and not file_line_stripped.startswith("old") and not len(file_line_stripped) == 0:
                                                p = re.compile('\\"(.*)\\"',)
                                                result = p.search(file_line_text)
                                                if result is not None:
                                                    translate_text = result.group(1)
                                                    variable_map = {}
                                                    no_translate_start = "<span class=\"notranslate\">"
                                                    no_translate_end = "</span>"
                                                    square_brackets = re.findall(r'\[.+?\]', translate_text)
                                                    for i in range(len(square_brackets)):
                                                        replaced_variable = no_translate_start+"["+str(i)+"]"+no_translate_end
                                                        variable_map[replaced_variable] = square_brackets[i]
                                                        translate_text = translate_text.replace(square_brackets[i], replaced_variable)
                                                    curly_brackets = re.findall(r'\{.+?\}', translate_text)
                                                    for i in range(len(curly_brackets)):
                                                        replaced_variable = no_translate_start+"{"+str(i)+"}"+no_translate_end
                                                        variable_map[replaced_variable] = curly_brackets[i]
                                                        translate_text = translate_text.replace(curly_brackets[i], replaced_variable)
                                                    translatable_texts[file_line_i] = {}
                                                    translatable_texts[file_line_i]["original"] = result.group(1)
                                                    translatable_texts[file_line_i]["text"] = translate_text
                                                    translatable_texts[file_line_i]["map"] = variable_map
                                        if len(translatable_texts.keys()) > 0:
                                            self.progressOrj = settings.locale.base.connectingGoogleTrans
                                            self.progress = settings.locale.connectingGoogleTrans
                                            start_time = time.time()
                                            translated = translator.translate([value["text"] for key,value in translatable_texts.items()], dest=googletrans.LANGCODES[self.googleTranslateLanguage.lower()])
                                            end_time = time.time()
                                            total_seconds = int(end_time - start_time)
                                            self.progressOrj = settings.locale.base.fileTranslatedInSeconds(seconds=total_seconds)
                                            self.progress = settings.locale.fileTranslatedInSeconds(seconds=total_seconds)
                                            for tr_i in range(len(translated)):
                                                if self.cancelled:
                                                    tlfile.closed
                                                    return True
                                                original_index = list(translatable_texts)[tr_i]
                                                original_value = list(translatable_texts.values())[tr_i]
                                                translated_text = translated[tr_i].text
                                                for key, value in original_value["map"].items():
                                                    translated_text = translated_text.replace(key, value)
                                                file_lines[original_index] = file_lines[original_index].replace(original_value["original"], translated_text.replace("\"", "\\\"").replace("\\\\\"","\\\"").replace("\n", "\\n"))
                                            with open(reallocation, "w") as tlfile2:
                                                tlfile2.write("".join(file_lines)+"\n"+translated_comment)
                                            tlfile2.closed
                                            self.progressOrj = settings.locale.base.translatingFileSuccess(filePath=reallocation)
                                            self.progress = settings.locale.translatingFileSuccess(filePath=reallocation)
                                tlfile.closed
                                    
                    self.progressOrj = settings.locale.base.translatingSuccess
                    self.progress = settings.locale.translatingSuccess
                else:
                    self.progressOrj =  settings.locale.base.translationFolderNotFound(folderPath=self.tlfilesdir)
                    self.progress = settings.locale.translationFolderNotFound(folderPath=self.tlfilesdir)
                    return False
        except:
            error_text = traceback.format_exc()
            print(error_text)
            self.progressOrj = settings.locale.base.translationFailed(error=error_text)
            self.progress = settings.locale.translationFailed(error=error_text)
            messagebox.showerror(settings.locale.translationFailedTitle, message=settings.locale.translationFailed()) 
            return False
        return True
    def __generate_translation_lock_file(self):
        if self.cancelled:
            return True
        if self.lockLocalization:
            try:
                self.progressOrj = settings.locale.base.lockingTranslation(languageName=self.languageName, languageFolderName=self.languageFolderName)
                self.progress = settings.locale.lockingTranslation(languageName=self.languageName, languageFolderName=self.languageFolderName)
                self.progressOrj = settings.locale.base.lookingExistedLockFile
                self.progress = settings.locale.lookingExistedLockFile
                lockfilefound = None
                for foundlockfile in listdir(self.gamedir):
                    if self.cancelled:
                        return True
                    lockfilerealLocation = path.join(self.gamedir, foundlockfile)
                    if path.isfile(lockfilerealLocation) and lockfilerealLocation.endswith(".rpy"):
                        with open(lockfilerealLocation, "r") as extlocktlfile:
                            extlocktlfilecontent = fsdecode(extlocktlfile.read())
                        extlocktlfile.closed
                        if self.commentline in extlocktlfilecontent:
                            remove(lockfilerealLocation)
                            rpycLocation = lockfilerealLocation[:-4]+".rpyc"
                            if path.exists(rpycLocation):
                                remove(rpycLocation)
                            lockfilefound = lockfilerealLocation
                            break
                if lockfilefound is not None:
                    self.progressOrj = settings.locale.base.lockFileFoundLoc(filePath=lockfilerealLocation)
                    self.progress = settings.locale.lockFileFoundLoc(filePath=lockfilerealLocation)
                else:
                    self.progressOrj = settings.locale.base.lockFileNotFound
                    self.progress = settings.locale.lockFileNotFound
                if self.cancelled:
                    return True
                locktlfile = path.join(self.gamedir, self.generate_random_rpy_name(6))
                lock_tl_file = open(locktlfile, "x")
                lock_tl_file.write(self.commentline+"\ninit python:\n    config.language = \""+self.languageFolderName+"\"")
                lock_tl_file.close()
                self.progressOrj = settings.locale.base.lockFileCreated(languageName=self.languageName, languageFolderName=self.languageFolderName, lockFileName=locktlfile)
                self.progress = settings.locale.lockFileCreated(languageName=self.languageName, languageFolderName=self.languageFolderName, lockFileName=locktlfile)
            except:
                error_text = traceback.format_exc()
                print(error_text)
                self.progressOrj = settings.locale.base.lockFileFailed(error=error_text)
                self.progress = settings.locale.lockFileFailed(error=error_text)
                messagebox.showerror(settings.locale.lockFileFailedTitle, message=settings.locale.lockFileFailed()) 
                return False
        return True
    def generate_translation(self):
        self.clear_temp_rpyc_decompilers()
        if len(self.languageFolderName) >= 3 and re.match('^[abcdefghijklmnoprqstuwvyzx]+$',self.languageFolderName):
            if len(self.languageName) > 0:
                if (self.translatewithGoogleTranslate and len(self.googleTranslateLanguage) > 0) or not self.translatewithGoogleTranslate:
                    self.cancelled = False
                    self.clearProgress()
                    self.__disable_all_controls(True)
                    #self.start_loading()
                    error_occurred = False
                    generated_translation_files = False
                    if self.__extract_rpa_archives():
                        if self.__decompile_rpyc_files():
                            if self.__optimize_texts():
                                if self.__generate_translation_files():
                                    generated_translation_files = True
                                    if self.__google_translate():
                                        if self.__generate_translation_lock_file():
                                            pass
                                        else:
                                            error_occurred = True
                                    else:
                                        error_occurred = True
                                else:
                                    error_occurred = True
                            else:
                                error_occurred = True
                        else:
                            error_occurred = True
                    else:
                        error_occurred = True
                    if self.cancelled:
                        self.progressOrj = settings.locale.base.translationCancelledByUser
                        self.progress = settings.locale.translationCancelledByUser
                    #self.stop_loading()
                    self.clear_temp_rpyc_decompilers()
                    self.__disable_all_controls(False)
                    all_skipped = False
                    if not self.extractRpaArchives and not self.decompileRpycFiles and (path.exists(self.tlfilesdir) and not self.forceRegenerateTranslation) and not self.translatewithGoogleTranslate and not self.lockLocalization:
                        all_skipped = True
                    if not all_skipped:
                        if not self.lockLocalization and not self.cancelled and generated_translation_files and not error_occurred:
                            self.progressOrj = self.progress = "\nvbox:"
                            self.progressOrj = self.progress = "    style_prefix \"radio\""
                            self.progressOrj = self.progress = "    label _(\"Language\")"
                            self.progressOrj = self.progress = "    textbutton \"English\" action Language(None)"
                            for langdir in listdir(self.tldir):
                                if langdir != "None":
                                    languageNameTemp = langdir
                                    if self.languageFolderName == langdir:
                                        languageNameTemp = self.languageName
                                    self.progressOrj = self.progress = "    textbutton \""+languageNameTemp+"\" action Language(\""+langdir+"\")"
                            self.progressOrj = self.progress = settings.locale.languageSettingsDesc
                        self.save_progress()
                        if not self.cancelled and not error_occurred:
                            messagebox.showinfo(settings.locale.translationCompletedTitle, settings.locale.translationCompleted)
                else:
                    self.progress = settings.locale.googleTransCanNotBeEmpty
            else:
                self.progress = settings.locale.languageNameInvalid
        else:
            self.progress = settings.locale.languageFolderNameInvalid
        return
    # hide renpy panel    
    def destroy(self):
        self.cancel()
        if self.__frame__ is not None:
            self.__frame__.pack_forget()
            self.__frame__.destroy()
        self.__frame__ = None
        self = None
    def cancel(self):
        self.progress = settings.locale.cancellingTranslation
        self.progress = ""
        self.cancelled = True
        if self.__rpaeditor__ is not None:
            self.__rpaeditor__.cancel()
        if self.__decompileRpycProcess__ is not None:
            try:
                #os.killpg(os.getpgid(self.__decompileRpycProcess__.pid), signal.SIGTERM)
                os.kill(self.__decompileRpycProcess__.pid, signal.CTRL_C_EVENT)
                self.__decompileRpycProcess__ = None
            except:
                print(traceback.format_exc())
    def get_zip_name(self, _dirname, _exname,n:int=0):
        _exnamenew = _exname + "-tl"
        distdir =  path.join(_dirname, "dist")
        arhivepath = path.join(distdir, _exnamenew+".zip" if n==0 else _exnamenew+"("+str(n)+").zip")
        if path.exists(arhivepath):
            return self.get_zip_name(_dirname, _exname, n+1)
        else:
            return arhivepath
    def archive(self):
        try:
            self.clearProgress()
            bname = path.basename(self.filename)
            gname = path.splitext(bname)[0]
            archivepath = self.get_zip_name(self.dirname, gname)
            dname = path.dirname(archivepath)
            self.progressOrj = settings.locale.base.zipStarted(archivePath=archivepath)
            self.progress = settings.locale.zipStarted(archivePath=archivepath)
            if not path.isdir(dname):
                mkdir(dname)
            zipobj = zipfile.ZipFile(archivepath, 'w', zipfile.ZIP_DEFLATED)
            rootlen = len(self.gamedir) + 1
            for base, dirs, files in walk(self.gamedir):
                for file in files:
                    fn = path.join(base, file)
                    if fn.endswith(".rpy") or fn.endswith(".rpyc") or fn.startswith(self.tldir):
                        zipobj.write(fn, path.join("game", fn[rootlen:]))
                        self.progressOrj = settings.locale.base.addedFileToArchive(filePath=fn)
                        self.progress = settings.locale.addedFileToArchive(filePath=fn)
            self.progressOrj = ""
            self.progressOrj = settings.locale.base.createdArchiveSuccess(archivePath=archivepath)
            self.progress = settings.locale.createdArchiveSuccess(archivePath=archivepath)
        except:
            error_text = traceback.format_exc()
            print(error_text)
            self.progressOrj = settings.locale.base.creatingArchiveError(error=error_text)
            self.progress = settings.locale.creatingArchiveError(error=error_text)
            messagebox.showerror(settings.locale.creatingArchiveErrorTitle, message=settings.locale.creatingArchiveError())
            self.save_progress()
    def launch(self):
        try:
            subprocess.call([self.filename])
        except:
            error_text = traceback.format_exc()
            print(error_text)
            self.progressOrj = settings.locale.base.launchTheGameError(error=error_text)
            self.progress = settings.locale.launchTheGameError(error=error_text)
            messagebox.showerror(settings.locale.creatingArchiveErrorTitle, message=settings.locale.launchTheGameError())
            self.save_progress()
