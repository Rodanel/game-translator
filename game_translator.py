import tkinter as tk
from tkinter import filedialog, messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from os import getcwd
import threading
import traceback
from src.style.frame import set_frame_attrs
from src.games import renpy
from src.games.detect_game import detect_game, GameType
from src.utils.settings import settings, Settings

# initialize window
root = tk.Tk()

# set title
root.title("Game Translator by Rodanel")
#window_icon = PhotoImage(file = 'assets/icon.jpg')
#root.iconphoto(False, window_icon)
root.iconbitmap(default='assets/favicon.ico')
# set size
window_width = 500
window_height = 500

# get the screen dimension
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# find the center point
center_x = int(screen_width / 2 - window_width / 2)
center_y = int(screen_height / 2 - window_height / 2)

# initialize size
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
root.resizable(False, False)
root.minsize(window_width, window_height)

#Settings

settingsButton = ttk.Button(root, text=settings.language.settings, bootstyle=(INFO, OUTLINE), command=lambda:settings.window(root))
settingsButton.pack(side=TOP, anchor=E)

# set icon
# root.iconbitmap('./assets/icon.ico')

# empty panel
emptyFrame = None
emptyLabel = None

# renpy panel
renpyFrame = None

# globals
filename = ttk.StringVar()
gameType = GameType.EMPTY

# select game excutable
def browse_game():
    global filename, gameType
    filename = filedialog.askopenfilename(initialdir=getcwd(), title=settings.language.selectGameExecutable, filetypes= [(settings.language.exeFile, "*.exe")])
    gameType = detect_game(filename)
    if gameType == GameType.RENPY:
        messagebox.showinfo(title=settings.language.detectedRenpyTitle, message=settings.language.detectedRenpyDesc)
    elif gameType == GameType.NONE:
        messagebox.showwarning(title=settings.language.unsupportedGameTitle, message=settings.language.unsupportedGame(filePath=filename))
    if gameType != GameType.NONE and gameType != GameType.EMPTY:
        settings.addDefaultGameSettingsIFNotExists(gameType, filename)
        startButton["state"] = "normal"
        zipButton["state"] = "normal"
    else:
        startButton["state"] = "disabled"
    showFrame()

started = False
# start translation
def translate():
    global filename, gameType, started
    settings.close_window()
    if started:
        if gameType == GameType.RENPY and renpyFrame is not None:
            started = False
            try:
                startButton["state"] = "disabled"
                renpyFrame.cancel()
            except:
                print(traceback.format_exc())
            finally:
                startButton["state"] = "normal"
                settingsButton["state"] = "normal"
                zipButton["state"] = "normal"
    else:
        if gameType == GameType.RENPY and renpyFrame is not None:
            try:
                startButton["text"] = settings.language.cancelButton
                started = True
                browseButton["state"] = "disabled"
                settingsButton["state"] = "disabled"
                zipButton["state"] = "disabled"
                renpyFrame.generate_translation()
            except Exception as e:
                messagebox.showerror(title=settings.language.errorTitle, message=str(e))
            finally:
                startButton["text"] = settings.language.startButton
                browseButton["state"] = "normal"
                startButton["state"] = "normal"
                settingsButton["state"] = "normal"
                zipButton["state"] = "normal"

            started = False
        elif gameType == GameType.NONE:
            messagebox.showwarning(title=settings.language.unsupportedGameTitle, message=settings.language.unsupportedGameTitle(filePath=filename))
def start_translation():
    start_translation_thread = threading.Thread(target=translate)
    start_translation_thread.daemon = True
    start_translation_thread.start()

def zip_game():
    if gameType == GameType.RENPY and renpyFrame is not None:
        try:
            browseButton["state"] = "disabled"
            startButton["state"] = "disabled"
            zipButton["state"] = "disabled"
            renpyFrame.archive()
        except:
            print(traceback.format_exc())
        finally:
            browseButton["state"] = "normal"
            startButton["state"] = "normal"
            zipButton["state"] = "normal"
    pass

def start_zipping():
    start_zipping_thread = threading.Thread(target=zip_game)
    start_zipping_thread.daemon = True
    start_zipping_thread.start()
# buttons


browseButton = ttk.Button(root, text=settings.language.browseButton, bootstyle=SUCCESS, command=browse_game)
browseButton.pack(side=BOTTOM, fill=X)

margin1 = ttk.Frame(root, height=5)
margin1.pack(side=BOTTOM, fill=X)

zipButton = ttk.Button(root, text=settings.language.zipButton, bootstyle=SUCCESS, command=lambda:start_zipping())
zipButton.pack(side=BOTTOM, fill=X)
zipButton["state"] = "disabled"

margin2 = ttk.Frame(root, height=5)
margin2.pack(side=BOTTOM, fill=X)

startButton = ttk.Button(root, text=settings.language.startButton, bootstyle=SUCCESS, command=lambda:start_translation())
startButton.pack(side=BOTTOM, fill=X)

startButton["state"] = "disabled"

def updateButtons():
    browseButton["text"] = settings.language.browseButton
    startButton["text"] = settings.language.startButton
    zipButton["text"] = settings.language.zipButton
    settingsButton["text"] = settings.language.settings
settings.onUpdate(Settings.LANGUAGE, updateButtons)
# find current frame
def destroyEmptyFrame():
    global emptyFrame
    if emptyFrame is not None:
        emptyFrame.pack_forget()
        emptyFrame.destroy()
        emptyFrame = None
def destroyRenpyFrame():
    global renpyFrame
    if renpyFrame is not None:
        renpyFrame.destroy()
        renpyFrame = None

def showFrame():
    global gameType, filename, emptyFrame, renpyFrame
    print(str(gameType))
    if gameType == GameType.NONE or gameType == GameType.EMPTY:
        destroyEmptyFrame()
        emptyFrame = set_frame_attrs(emptyFrame, root)
        emptyLabel = ttk.Label(emptyFrame, text=settings.language.browseLabel)
        emptyLabel.pack(fill=Y, expand=True, anchor=CENTER)
        def updateEmptyFrameLang():
            emptyLabel["text"] = settings.language.browseLabel
        settings.onUpdate(Settings.LANGUAGE, updateEmptyFrameLang)
    else:
        destroyEmptyFrame()
    if gameType == GameType.RENPY:
        destroyRenpyFrame()
        renpyFrame = renpy.RenpyFrame(root, filename)
    else:
        destroyRenpyFrame()
showFrame()

# show window
root.mainloop()