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
    
        self.__languageCodeFrame__ = Frame(self.__frame__)
        self.__languageCodeFrame__.pack(side="top", fill="x", anchor="n")
        self.__languageCodeLabel__ = Label(self.__languageCodeFrame__, text="Language Code (only english characters):")
        self.__languageCodeLabel__.pack(side="left", anchor="e")
        self.__languageCode__ = StringVar()
        self.__languageCodeEntry__ = Entry(self.__languageCodeFrame__, textvariable=self.__languageCode__, width=tb_width)
        self.__languageCodeEntry__.pack(side="right")
        
        self.__lockLocalization__ = BooleanVar()
        self.__lockLocalizationCheck__ = Checkbutton(self.__frame__, text= "Lock translation. (Locks the game to this language. No need to update screens.rpy file for adding language options if checked.)", variable=self.__lockLocalization__, onvalue=True, offvalue=False, wraplength=wrap_length)
        self.__lockLocalizationCheck__.pack(side="top", fill="x", anchor="n")
        self.__extractRpaArchives__ = BooleanVar()
        self.__extractRpaArchivesCheck__ = Checkbutton(self.__frame__, text= "Extract RPA archives.", variable=self.__extractRpaArchives__, onvalue=True, offvalue=False)
        self.__extractRpaArchivesCheck__.pack(side="top", fill="x", anchor="n")

        self.__decompileRpycFiles__ = BooleanVar()
        self.__decompileRpycFilesCheck__ = Checkbutton(self.__frame__, text= "Decompile RPYC files.", variable=self.__decompileRpycFiles__, onvalue=True, offvalue=False)
        self.__decompileRpycFilesCheck__.pack(side="top", fill="x", anchor="n")

        self.__translateDescription__ = Label(self.__frame__, text="WARNING: Your languge code should be supported Google Translate language code for translating from Google Translate.")
        self.__translateDescription__.pack(side="top", fill="x")
        self.__translateButton__ = Button(self.__frame__, text="Auto Translate with Google Translate", background=enabledButtonColor, foreground="white", disabledforeground="white", state="disabled", command=lambda:self.google_translate_start())
        self.__translateButton__.pack(side="top", fill="x")

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
    def languageName(self) -> str:
        return self.__languageName__.get()
    @property
    def languageCode(self) -> str:
        return self.__languageCode__.get()
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
    def progress(self) -> str:
        return self.__progressText__.get(1.0, END)
    @progress.setter
    def progress(self, value: str):
        self.__progressText__["state"] = "normal"
        self.__progressText__.insert(END, "\n"+value)
        self.__progressText__.see(END)
        self.__progressText__["state"] = "disabled"
    @property
    def translateButton(self) -> Button:
        return self.__translateButton__

    def google_translate_start(self):
        start_translation_thread = threading.Thread(target=self.google_translate)
        start_translation_thread.daemon = True
        start_translation_thread.start()
    def google_translate(self):
        try:
            tldir = path.join(path.dirname(self.filename), "game", "tl", self.__languageCode__.get())
            if len(self.__languageCode__.get()) > 0 and path.exists(tldir):
                self.clearProgress()
                for _path, _subdirs, _files in walk(tldir):
                    for _name in _files:
                        reallocation = path.join(_path, _name)
                        if path.isfile(reallocation) and reallocation.endswith(".rpy"):
                            self.progress = "Translating \""+reallocation+"\"..."
                            newtexts = ""
                            with open(reallocation, "r+") as tlfile:
                                lines = tlfile.readlines()
                                for line in lines:
                                    line = str(line)
                                    if not line.startswith("#") and not line.startswith("    #") and not line.startswith("translate ") and not line.startswith("   old") and not len(line.strip()) == 0:
                                        print("Old line: " + line)
                                        p = re.compile('\\"(.*)\\"',)
                                        result = p.search(line)
                                        if result is not None:
                                            translated = translator.translate(result.group(1), dest = self.languageCode)
                                            print(translated.text)
                                            line = line.replace("\""+result.group(1)+"\"", "\""+translated.text+"\"")
                                            
                                        print("New line: " + line)
                                    newtexts += line
                            tlfile.closed
                            with open(reallocation, "w") as tlfile2:
                                tlfile2.write(newtexts)
                            tlfile2.closed
                            self.progress = "Translated the file.." 
                self.progress = "Translation completed! Please launch the game and check if has any error."
            else:
                self.progress =  "Translation folder \""+tldir+"\" not found" 
        except Exception as e:
            self.progress = "Translation failed! Error: \n\n"+str(e)
        self.save_progress()
    def update_google_translate_button_state(self):
        if len(self.__languageCode__.get()) > 0 and path.exists(path.join(path.dirname(self.filename), "game", "tl", self.__languageCode__.get())):
            toggle_button_state(self.__translateButton__, "normal") 
        else:
            toggle_button_state(self.__translateButton__, "disabled") 
    def __save_languageName(self, *args):
        self.__save_setting(Settings.LANGUAGE_NAME, self.__languageName__)
    def __save_languageCode(self, *args):
        self.update_google_translate_button_state()
        self.__save_setting(Settings.LANGUAGE_CODE, self.__languageCode__)
    def __save_lockLocalization(self, *args):
        self.__save_setting(Settings.LOCK_LOCALIZATION, self.__lockLocalization__)
    def __save_extractRpaArchives(self, *args):
        self.__save_setting(Settings.EXTRACT_RPA, self.__extractRpaArchives__)
    def __save_decompileRpycFiles(self, *args):
        self.__save_setting(Settings.DECOMPİLE_RPYC, self.__decompileRpycFiles__)

    def __save_setting(self, propType, prop):
        settings.updateGame(GameType.RENPY, self.filename, {propType: prop.get()})
    def __restore_setting(self, propType, prop):
        defaultSettings = Settings.getDefault(GameType.RENPY)
        gameSettings = settings.data[str(GameType.RENPY)][self.filename]
        prop.set(gameSettings[propType] if propType in gameSettings else defaultSettings[propType])

    def __update_props(self):
        self.__restore_setting(Settings.LANGUAGE_NAME, self.__languageName__)
        self.__languageName__.trace_add("write", self.__save_languageName)
        
        self.__restore_setting(Settings.LANGUAGE_CODE, self.__languageCode__)
        self.__languageCode__.trace_add("write", self.__save_languageCode)
        self.update_google_translate_button_state()

        self.__restore_setting(Settings.LOCK_LOCALIZATION, self.__lockLocalization__)
        self.__lockLocalization__.trace_add("write", self.__save_lockLocalization)

        self.__restore_setting(Settings.EXTRACT_RPA, self.__extractRpaArchives__)
        self.__extractRpaArchives__.trace_add("write", self.__save_extractRpaArchives)

        self.__restore_setting(Settings.DECOMPİLE_RPYC, self.__decompileRpycFiles__)
        self.__decompileRpycFiles__.trace_add("write", self.__save_decompileRpycFiles)

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

def generate_random_rpy(length:int):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))+".rpy"

def translate(renpyFrame: RenpyFrame):
    print(renpyFrame.filename+ " will be translated to "+renpyFrame.languageName+" ("+renpyFrame.languageCode+")!")
    dirname = path.dirname(renpyFrame.filename)
    gamedir = path.join(dirname, "game")
    tldir = path.join(gamedir, "tl")
    commentline = "# Generated by \"Game Translator by Rodanel\""
    if len(renpyFrame.languageCode) > 0 and re.match('^[abcdefghijklmnoprqstuwvyzx]+$',renpyFrame.languageCode):
        if len(renpyFrame.languageCode) > 0:
            renpyFrame.clearProgress()
            exception_occurred = False
            if renpyFrame.extractRpaArchives:
                for fname in listdir(gamedir):
                    fullpath = path.join(gamedir, fname)
                    if fname.endswith(".rpa"):
                        #renpyFrame.start_loading()
                        try:
                            renpyFrame.progress = "Extracting "+fname+"..."
                            print("Exracting "+fname+"...")
                            RpaEditor(fullpath, _extract=True, _version=2)
                            renpyFrame.progress = "Extracted "+fname+" successfully!"
                        except Exception as e:
                            exception_occurred = True
                            error_text = "Could not extract \""+fname+"\" archive.\n\nError: "+str(e)
                            renpyFrame.progress = error_text
                            messagebox.showerror("Could not extract archive", message=error_text)                    
                            break
            else:
                renpyFrame.progress = "Extracting rpa archives skipped."
            if not exception_occurred:
                if renpyFrame.decompileRpycFiles:
                    try:
                        renpyFrame.progress = "Starting decompiling rpyc files..."
                        bat_path = path.join(dirname, "unren.bat")
                        clear_temp_rpyc_decompilers(dirname, bat_path)
                        unren_bat_file = open(bat_path, "x")
                        unren_bat_file.write(unren_content)
                        unren_bat_file.close()
                        spRpyc = subprocess.Popen(bat_path+ " decompile", cwd=dirname, stdout=subprocess.PIPE, bufsize=1, creationflags=CREATE_NO_WINDOW)
                        while True:
                            line = spRpyc.stdout.readline()
                            if not line:
                                break
                            else:
                                renpyFrame.progress = fix_console(line)
                        renpyFrame.progress = "Decompiling rpyc files completed. Removing temp files."
                        clear_temp_rpyc_decompilers(dirname, bat_path)
                        time.sleep(3)
                        renpyFrame.progress = "Temp files removed successfully!"
                    except Exception as e:
                        exception_occurred = True
                        error_text = "Could not decompile rpyc files.\n\nError: "+str(e)
                        renpyFrame.progress = error_text
                        messagebox.showerror("Could not decompile", message=error_text)
                else:
                    renpyFrame.progress = "Decompiling rpyc files skipped."
            if not exception_occurred:
                renpyFrame.progress = "Genarating translation files started..."
                executable_path = path.dirname(fsdecode(renpyFrame.filename))
                game_extension = ".exe" if renpyFrame.filename.endswith(".exe") else ""
                executables = [ "python"+game_extension]
                executables.append(renpyFrame.filename)
                for i in executables:
                    executable = path.join(executable_path, i)
                    if path.exists(executable):
                        break
                else:
                    raise Exception("Python interpreter not found: %r", executables)
                cmd = [ executable, "-EO", sys.argv[0] ]
                args = [ "translate", renpyFrame.languageCode ]
                cmd.append(dirname)
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
                        renpyFrame.progress = fix_console(line)
                renpyFrame.progress = "Genarated translation files successfully."
            if renpyFrame.lockLocalization:
                renpyFrame.progress = "Language locking to "+renpyFrame.languageName+" ("+renpyFrame.languageCode+")..."
                renpyFrame.progress = "Looking for existed lock file."
                lockfilefound = None
                for foundlockfile in listdir(gamedir):
                    lockfilerealLocation = path.join(gamedir, foundlockfile)
                    if path.isfile(lockfilerealLocation) and lockfilerealLocation.endswith(".rpy"):
                        with open(lockfilerealLocation, "r") as extlocktlfile:
                            extlocktlfilecontent = fsdecode(extlocktlfile.read())
                        extlocktlfile.closed
                        if commentline in extlocktlfilecontent:
                            remove(lockfilerealLocation)
                            lockfilefound = lockfilerealLocation
                            break
                if lockfilefound is not None:
                    renpyFrame.progress = "Lock file found in \""+lockfilerealLocation+"\" and removed."
                    renpyFrame.progress = "Creating new one..."
                else:
                    renpyFrame.progress = "Lock file not found, creating one..."
                locktlfile = path.join(gamedir, generate_random_rpy(6))
                lock_tl_file = open(locktlfile, "x")
                lock_tl_file.write(commentline+"\ninit python:\n    config.language = \""+renpyFrame.languageCode+"\"")
                lock_tl_file.close()
                renpyFrame.progress = "Language locked to "+renpyFrame.languageName+" ("+renpyFrame.languageCode+"). For unlocking just delete \""+locktlfile+"\" file."
            else:
                renpyFrame.progress = "\nvbox:"
                renpyFrame.progress = "    style_prefix \"radio\""
                renpyFrame.progress = "    label _(\"Language\")"
                renpyFrame.progress = "    textbutton \"English\" action Language(None)"
                for langdir in listdir(tldir):
                    if langdir != "None":
                        languageNameTemp = langdir
                        if renpyFrame.languageCode == langdir:
                            languageNameTemp = renpyFrame.languageName
                        renpyFrame.progress = "    textbutton \""+languageNameTemp+"\" action Language(\""+langdir+"\")"
                renpyFrame.progress = "\nAdd this code to \"screen preferences():\" in screens.rpy. Replace English with game's orijinal language."
            #renpyFrame.stop_loading()
            renpyFrame.save_progress()
            renpyFrame.progress = "\nClick \""+renpyFrame.translateButton["text"]+"\" button to auto translate."
        else:
            renpyFrame.progress = "Language name can not be empty."
    else:
        renpyFrame.progress = "Language code should be contain only english lowercase characters."
    return