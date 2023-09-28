from os import path, listdir, remove, rmdir, environ as myenv, mkdir, walk
import re
import subprocess
import time
from datetime import datetime
import sys
import random
import string
from googletrans import Translator
import threading
from tkinter import Tk, StringVar, BooleanVar, Frame, Label, Entry, Checkbutton, messagebox, scrolledtext, END, WORD, Button

from src.games.detect_game import GameType
from src.games.renpy.rpa import RpaEditor
from src.games.renpy.unrpyc import unren_content
from src.style.frame import set_frame_attrs
from src.settings import settings, Settings
from src.style.buttons import enabledButtonColor, toggle_button_state

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

    def __init__(self, root: Tk, filename:str):
        self.__root__ = root
        self.__frame__ = None
        self.__filename__ = filename
        self.__frame__ = set_frame_attrs(self.__frame__, root)
        wrap_length = 500
        tb_width = 40
        self.__titleLabel__ = Label(self.__frame__, text="Renpy Game Translation", wraplength=wrap_length)
        self.__titleLabel__.pack(side="top", fill="x", anchor="n")
        self.__gamePathLabel__ = Label(self.__frame__, text="Game: "+self.__filename__, wraplength=wrap_length)
        self.__gamePathLabel__.pack(side="top", fill="x", anchor="n")
    
        self.__languageNameFrame__ = Frame(self.__frame__)
        self.__languageNameFrame__.pack(side="top", fill="x", anchor="n")
        self.__languageNameLabel__ = Label(self.__languageNameFrame__, text="Language name:")
        self.__languageNameLabel__.pack(side="left", anchor="e")
        self.__languageName__ = StringVar()
        self.__languageNameEntry__ = Entry(self.__languageNameFrame__, textvariable=self.__languageName__, width=tb_width)
        self.__languageNameEntry__.pack(side="right")
    
        self.__languageFolderNameFrame__ = Frame(self.__frame__)
        self.__languageFolderNameFrame__.pack(side="top", fill="x", anchor="n")
        self.__languageFolderNameLabel__ = Label(self.__languageFolderNameFrame__, text="Language Folder Name:")
        self.__languageFolderNameLabel__.pack(side="left", anchor="e")
        self.__languageFolderName__ = StringVar()
        self.__languageFolderNameEntry__ = Entry(self.__languageFolderNameFrame__, textvariable=self.__languageFolderName__, width=tb_width)
        self.__languageFolderNameEntry__.pack(side="right")
        
        self.__lockLocalization__ = BooleanVar()
        self.__lockLocalizationCheck__ = Checkbutton(self.__frame__, text= "Lock translation. (Locks the game to this language. No need to update screens.rpy file for adding language options if checked.)", variable=self.__lockLocalization__, onvalue=True, offvalue=False, wraplength=wrap_length)
        self.__lockLocalizationCheck__.pack(side="top", fill="x", anchor="n")
        self.__extractRpaArchives__ = BooleanVar()
        self.__extractRpaArchivesCheck__ = Checkbutton(self.__frame__, text= "Extract RPA archives.", variable=self.__extractRpaArchives__, onvalue=True, offvalue=False)
        self.__extractRpaArchivesCheck__.pack(side="top", fill="x", anchor="n")
        self.__extractRpaArchivesCheck__.select()
        self.__decompileRpycFiles__ = BooleanVar()
        self.__decompileRpycFilesCheck__ = Checkbutton(self.__frame__, text= "Decompile RPYC files.", variable=self.__decompileRpycFiles__, onvalue=True, offvalue=False)
        self.__decompileRpycFilesCheck__.pack(side="top", fill="x", anchor="n")
        self.__decompileRpycFilesCheck__.select()
        
        self.__translateWithGoogleTranslate__ = BooleanVar()
        self.__translateWithGoogleTranslateCheck__ = Checkbutton(self.__frame__, text= "Translate with Google Translate.", variable=self.__translateWithGoogleTranslate__, onvalue=True, offvalue=False)
        self.__translateWithGoogleTranslateCheck__.pack(side="top", fill="x")
        self.__googleTranslateFrame__ = Frame(self.__frame__)
        self.__googleTranslateFrame__.pack(side="top", fill="x", anchor="n")
        self.__googleTranslateLanguageCodeLabel__ = Label(self.__googleTranslateFrame__, text="Google Translate Language Code:")
        self.__googleTranslateLanguageCodeLabel__.pack(side="left", anchor="e")
        self.__googleTranslateLanguageCode__ = StringVar()
        self.__googleTranslateLanguageCodeEntry__ = Entry(self.__googleTranslateFrame__, textvariable=self.__googleTranslateLanguageCode__, width=tb_width)
        self.__googleTranslateLanguageCodeEntry__.pack(side="right")
        self.__googleTranslateLanguageCodeEntry__["state"] = "disabled"

        self.__progressText__ = scrolledtext.ScrolledText(self.__frame__, wrap=WORD, state="disabled")
        self.__progressText__.pack(side="top", fill="both", expand=True)
        self.__update_props()
    # element properties
    @property
    def root(self) -> Tk:
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
    def decompileRpycFiles(self) -> bool:
        return self.__decompileRpycFiles__.get()
    @property
    def lockLocalization(self) -> bool:
        return self.__lockLocalization__.get()
    @property
    def translatewithGoogleTranslate(self) -> bool:
        return self.__translateWithGoogleTranslate__.get()
    @property
    def googleTranslateLanguageCode(self) -> bool:
        return self.__googleTranslateLanguageCode__.get()
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
    
    def __save_languageName(self, *args):
        self.__save_setting(Settings.LANGUAGE_NAME, self.__languageName__)
    def __save_languageFolderName(self, *args):
        self.__save_setting(Settings.LANGUAGE_FOLDER_NAME, self.__languageFolderName__)
    def __save_lockLocalization(self, *args):
        self.__save_setting(Settings.LOCK_LOCALIZATION, self.__lockLocalization__)
    def __save_extractRpaArchives(self, *args):
        self.__save_setting(Settings.EXTRACT_RPA, self.__extractRpaArchives__)
    def __save_decompileRpycFiles(self, *args):
        self.__save_setting(Settings.DECOMPİLE_RPYC, self.__decompileRpycFiles__)
    def __save_translateWithGoogleTranslate(self, *args):
        self.__save_setting(Settings.TRANSLATE_WITH_GOOGLE_TRANSLATE, self.__translateWithGoogleTranslate__)
        self.__update_googleTranslateLanguageCodeState()
    def __save_googleTranslateLanguageCode(self, *args):
        self.__save_setting(Settings.GOOGLE_TRANSLATE_LANGUAGE_CODE, self.__googleTranslateLanguageCode__)
    def __update_googleTranslateLanguageCodeState(self):
        if self.translatewithGoogleTranslate:
            self.__googleTranslateLanguageCodeEntry__["state"] = "normal"
        else:
            self.__googleTranslateLanguageCodeEntry__["state"] = "disabled"
    def __disable_all_controls(self, disabled: bool = True):
        self.__languageNameEntry__["state"] = "disabled" if disabled else "normal"
        self.__languageFolderNameEntry__["state"] = "disabled" if disabled else "normal"
        self.__lockLocalizationCheck__["state"] = "disabled" if disabled else "normal"
        self.__extractRpaArchivesCheck__["state"] = "disabled" if disabled else "normal"
        self.__decompileRpycFilesCheck__["state"] = "disabled" if disabled else "normal"
        self.__translateWithGoogleTranslateCheck__["state"] = "disabled" if disabled else "normal"
        if disabled:
            self.__googleTranslateLanguageCodeEntry__["state"] = "disabled"
        else:
            self.__update_googleTranslateLanguageCodeState()
        print("")

    def __save_setting(self, propType, prop):
        settings.updateGame(GameType.RENPY, self.filename, {propType: prop.get()})
    def __restore_setting(self, propType, prop):
        try:
            defaultSettings = Settings.getDefault(GameType.RENPY)
            gameSettings = settings.data[str(GameType.RENPY)][self.filename]
            prop.set(gameSettings[propType] if propType in gameSettings else defaultSettings[propType])
        except Exception as e:
            print("Could not restore setting: "+propType)
            print("Error: "+str(e))

    def __update_props(self):
        self.__restore_setting(Settings.LANGUAGE_NAME, self.__languageName__)
        self.__languageName__.trace_add("write", self.__save_languageName)
        
        self.__restore_setting(Settings.LANGUAGE_FOLDER_NAME, self.__languageFolderName__)
        self.__languageFolderName__.trace_add("write", self.__save_languageFolderName)

        self.__restore_setting(Settings.LOCK_LOCALIZATION, self.__lockLocalization__)
        self.__lockLocalization__.trace_add("write", self.__save_lockLocalization)

        self.__restore_setting(Settings.EXTRACT_RPA, self.__extractRpaArchives__)
        self.__extractRpaArchives__.trace_add("write", self.__save_extractRpaArchives)

        self.__restore_setting(Settings.DECOMPİLE_RPYC, self.__decompileRpycFiles__)
        self.__decompileRpycFiles__.trace_add("write", self.__save_decompileRpycFiles)

        self.__restore_setting(Settings.TRANSLATE_WITH_GOOGLE_TRANSLATE, self.__translateWithGoogleTranslate__)
        self.__translateWithGoogleTranslate__.trace_add("write", self.__save_translateWithGoogleTranslate)

        self.__restore_setting(Settings.GOOGLE_TRANSLATE_LANGUAGE_CODE, self.__googleTranslateLanguageCode__)
        self.__googleTranslateLanguageCode__.trace_add("write", self.__save_googleTranslateLanguageCode)
        self.__update_googleTranslateLanguageCodeState()

    def clearProgress(self):
        self.__progressText__["state"] = "normal"
        self.__progressText__.delete(1.0, END)
        self.__progressText__["state"] = "disabled"
    
    def save_progress(self):
        now = datetime.now()
        logsdir = path.join(path.dirname(self.filename), "game_translator-logs")
        if not path.isdir(logsdir):
            mkdir(logsdir)
        log_file_path = path.join(logsdir, "game_translator-log-"+now.strftime("%m-%d-%Y, %H-%M-%S")+".txt")
        log_file = open(log_file_path, "x")
        log_file.write("Game Translator by Rodanel Logs\nDate: "+now.strftime("%m/%d/%Y, %H:%M:%S")+"\n\n"+self.progress)
        log_file.close()
        self.progress = "\nYou can find this log file in "+log_file_path+" later."
    def clear_temp_rpyc_decompilers(self):
        if path.exists(self.unrenfile):
            remove(self.unrenfile)
        decompiler_path = path.join(self.dirname, "decompiler")
        if path.exists(decompiler_path):
            for decompiler_file in listdir(decompiler_path):
                remove(path.join(decompiler_path, decompiler_file))
        if path.exists(decompiler_path):
            rmdir(decompiler_path)
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
        if self.extractRpaArchives:
            for fname in listdir(self.gamedir):
                fullpath = path.join(self.gamedir, fname)
                if fname.endswith(".rpa"):
                    try:
                        self.progress = "Extracting "+fname+"..."
                        print("Exracting "+fname+"...")
                        RpaEditor(fullpath, _extract=True, _version=2)
                        self.progress = "Extracted "+fname+" successfully!"
                    except Exception as e:
                        error_text = "Could not extract \""+fname+"\" archive.\n\nError: "+str(e)
                        self.progress = error_text
                        messagebox.showerror("Could not extract archive", message=error_text)               
                        return False
        else:
            self.progress = "Extracting rpa archives skipped."
        return True

    def __decompile_rpyc_files(self):
        if self.decompileRpycFiles:
            try:
                self.progress = "Starting decompiling rpyc files..."
                self.clear_temp_rpyc_decompilers()
                unren_bat_file = open(self.unrenfile, "x")
                unren_bat_file.write(unren_content)
                unren_bat_file.close()
                spRpyc = subprocess.Popen(self.unrenfile+ " decompile", cwd=self.dirname, stdout=subprocess.PIPE, bufsize=1, creationflags=CREATE_NO_WINDOW)
                while True:
                    line = spRpyc.stdout.readline()
                    if not line:
                        break
                    else:
                        self.progress = fix_console(line)
                self.progress = "Decompiling rpyc files completed. Removing temp files."
                self.clear_temp_rpyc_decompilers()
                time.sleep(3)
                self.progress = "Temp files removed successfully!"
            except Exception as e:
                error_text = "Could not decompile rpyc files.\n\nError: "+str(e)
                self.progress = error_text
                messagebox.showerror("Could not decompile", message=error_text)
                return False
        else:
            self.progress = "Decompiling rpyc files skipped."
        return True
    
    def __generate_translation_files(self):
        try:
            self.progress = "Genarating translation files..."
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
            cmd = [ executable, "-EO", sys.argv[0] ]
            args = [ "translate", self.languageFolderName ]
            cmd.append(self.dirname)
            cmd.extend(args)

            environ = dict(myenv)
            environ.update({})

            encoded_environ = { }

            for k, v in environ.items():
                if v is None:
                    continue

                encoded_environ[str(k)] = str(v)

            # Launch the project.
            cmd = [ str(i) for i in cmd ]

            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=1, creationflags=CREATE_NO_WINDOW,env=encoded_environ)
            while True:
                line = p.stdout.readline()
                if not line:
                    break
                else:
                    self.progress = fix_console(line)
            self.progress = "Genarated translation files successfully."
        except Exception as e:
            error_text = "Could not create translation files.\n\nError: "+str(e)
            self.progress = error_text
            messagebox.showerror("Could not create translation files.", message=error_text)
            return False
        return True
    def __google_translate(self):
        try:
            translated_comment = " # translated"
            if self.translatewithGoogleTranslate:
                if len(self.googleTranslateLanguageCode) > 0:
                    if path.exists(self.tlfilesdir):
                        for _path, _subdirs, _files in walk(self.tlfilesdir):
                            for _name in _files:
                                reallocation = path.join(_path, _name)
                                if path.isfile(reallocation) and reallocation.endswith(".rpy"):
                                    self.progress = "Translating \""+reallocation+"\"..."
                                    newtexts = ""
                                    with open(reallocation, "r+") as tlfile:
                                        file_lines = tlfile.readlines()
                                        for file_line in file_lines:
                                            file_line = str(file_line)
                                            file_line_stripped = file_line.strip()
                                            if not file_line_stripped.startswith("#") and not file_line.startswith("translate ") and not file_line_stripped.startswith("old") and not len(file_line_stripped) == 0 and not file_line_stripped.endswith(translated_comment):
                                                p = re.compile('\\"(.*)\\"',)
                                                result = p.search(file_line)
                                                if result is not None:
                                                    translate_text = result.group(1)
                                                    print("Original: "+translate_text)
                                                    m = re.findall(r'\[.+?\]', translate_text)
                                                    variable_map = {}
                                                    for i in range(len(m)):
                                                        variable_map["["+str(i)+"]"] = m[i]
                                                        translate_text = translate_text.replace(m[i], "["+str(i)+"]")
                                                    translated = translator.translate(translate_text, dest = self.googleTranslateLanguageCode)
                                                    translated_text = translated.text
                                                    print("Translated: "+ translated_text)
                                                    for key, value in variable_map.items():
                                                        translated_text = translated_text.replace(key, value)
                                                    print("Restored: "+ translated_text)
                                                    file_line = file_line.replace("\""+result.group(1)+"\"", "\""+translated_text+"\""+translated_comment)
                                            newtexts += file_line
                                    tlfile.closed
                                    with open(reallocation, "w") as tlfile2:
                                        tlfile2.write(newtexts)
                                    tlfile2.closed
                                    self.progress = "Translation of \""+reallocation+"\" successfull!" 
                        self.progress = "Translation completed! Please launch the game and check if has any error."
                    else:
                        self.progress =  "Translation folder \""+self.tlfilesdir+"\" not found!"
                        return False
                else:
                    self.progress = "Google Translate Language Code can not be empty!"
                    return False
            else:
                return True
        except Exception as e:
            error_text = "Translation failed!\n\nError: "+str(e)
            self.progress = error_text
            messagebox.showerror("Translation Failed!", message=error_text) 
            return False
        return True
    def __generate_translation_lock_file(self):
        if self.lockLocalization:
            try:
                self.progress = "Language locking to "+self.languageName+" ("+self.languageFolderName+")..."
                self.progress = "Looking for existed lock file."
                lockfilefound = None
                for foundlockfile in listdir(self.gamedir):
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
                    self.progress = "Lock file found in \""+lockfilerealLocation+"\" and removed."
                    self.progress = "Creating new one..."
                else:
                    self.progress = "Lock file not found, creating one..."
                locktlfile = path.join(self.gamedir, self.generate_random_rpy_name(6))
                lock_tl_file = open(locktlfile, "x")
                lock_tl_file.write(self.commentline+"\ninit python:\n    config.language = \""+self.languageFolderName+"\"")
                lock_tl_file.close()
                self.progress = "Language locked to "+self.languageName+" ("+self.languageFolderName+"). For unlocking just delete \""+locktlfile+"\" file."
            except Exception as e:
                error_text = "Could not create translation lock file.\n\nError: "+str(e)
                self.progress = error_text
                messagebox.showerror("Could not create translation lock file.", message=error_text) 
                return False
        else:
            self.progress = "\nvbox:"
            self.progress = "    style_prefix \"radio\""
            self.progress = "    label _(\"Language\")"
            self.progress = "    textbutton \"English\" action Language(None)"
            for langdir in listdir(self.tldir):
                if langdir != "None":
                    languageNameTemp = langdir
                    if self.languageFolderName == langdir:
                        languageNameTemp = self.languageName
                    self.progress = "    textbutton \""+languageNameTemp+"\" action Language(\""+langdir+"\")"
            self.progress = "\nAdd this code to \"screen preferences():\" in screens.rpy. Replace English with game's orijinal language."
        return True
    def generate_translation(self):
        if len(self.languageFolderName) >= 3 and re.match('^[abcdefghijklmnoprqstuwvyzx]+$',self.languageFolderName):
            if len(self.languageName) > 0:
                self.clearProgress()
                self.__disable_all_controls(True)
                #self.start_loading()
                if self.__extract_rpa_archives():
                    if self.__decompile_rpyc_files():
                        if self.__generate_translation_files():
                            if self.__google_translate():
                                if self.__generate_translation_lock_file():
                                    pass
                #self.stop_loading()
                self.__disable_all_controls(False)
                self.save_progress()
            else:
                self.progress = "Language name can not be empty."
        else:
            self.progress = "Language folder name should be at least 3 characters and contain only lowercase english characters."
        return
    # hide renpy panel    
    def destroy(self):
        if self.__frame__ is not None:
            self.__frame__.pack_forget()
            self.__frame__.destroy()
        self.__frame__ = None
        self = None