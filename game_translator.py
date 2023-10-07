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
from src.utils.assets import MyAssets


# initialize window
root = ttk.Window(title="Game Translator by Rodanel", iconphoto=str(MyAssets.icon))

#window_icon = PhotoImage(file = MyAssets.icon)
#root.iconphoto(False, window_icon)
#root.iconbitmap(default=MyAssets.favicon)
# set size
window_width = 500
window_height = 300

# get the screen dimension
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# find the center point
center_x = int(screen_width / 2 - window_width / 2)
center_y = int(screen_height / 2 - window_height / 2)

# initialize size
#root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
root.geometry(f'+{center_x}+{center_y}')
root.resizable(False, False)
root.minsize(window_width, window_height)


#Settings

settingsButton = ttk.Button(root, text=settings.locale.settings, bootstyle=(INFO, OUTLINE), command=lambda:settings.window(root))
settingsButton.pack(side=TOP, anchor=E)

# set icon
# root.iconbitmap(MyAssets.icon)

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
    filename = filedialog.askopenfilename(initialdir=getcwd(), title=settings.locale.selectGameExecutable, filetypes= [(settings.locale.exeFile, "*.exe")])
    gameType = detect_game(filename)
    if gameType == GameType.RENPY:
        messagebox.showinfo(title=settings.locale.detectedRenpyTitle, message=settings.locale.detectedRenpyDesc)
    elif gameType == GameType.NONE:
        messagebox.showwarning(title=settings.locale.unsupportedGameTitle, message=settings.locale.unsupportedGame(filePath=filename))
    if gameType != GameType.NONE and gameType != GameType.EMPTY:
        startButton["state"] = "normal"
        zipButton["state"] = "normal"
    else:
        startButton["state"] = "disabled"
        zipButton["state"] = "disabled"
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
    else:
        if gameType == GameType.RENPY and renpyFrame is not None:
            try:
                startButton["text"] = settings.locale.cancelButton
                started = True
                browseButton["state"] = "disabled"
                settingsButton["state"] = "disabled"
                zipButton["state"] = "disabled"
                renpyFrame.generate_translation()
            except Exception as e:
                messagebox.showerror(title=settings.locale.errorTitle, message=str(e))
            finally:
                startButton["text"] = settings.locale.startButton
                browseButton["state"] = "normal"
                startButton["state"] = "normal"
                settingsButton["state"] = "normal"
                zipButton["state"] = "normal"

            started = False
        elif gameType == GameType.NONE:
            messagebox.showwarning(title=settings.locale.unsupportedGameTitle, message=settings.locale.unsupportedGameTitle(filePath=filename))
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


browseButton = ttk.Button(root, text=settings.locale.browseButton, bootstyle=SUCCESS, command=browse_game)
browseButton.pack(side=BOTTOM, fill=X)

margin1 = ttk.Frame(root, height=5)
margin1.pack(side=BOTTOM, fill=X)

zipButton = ttk.Button(root, text=settings.locale.zipButton, bootstyle=SUCCESS, command=lambda:start_zipping())
zipButton.pack(side=BOTTOM, fill=X)
zipButton["state"] = "disabled"

margin2 = ttk.Frame(root, height=5)
margin2.pack(side=BOTTOM, fill=X)

startButton = ttk.Button(root, text=settings.locale.startButton, bootstyle=SUCCESS, command=lambda:start_translation())
startButton.pack(side=BOTTOM, fill=X)

startButton["state"] = "disabled"

def updateButtons():
    browseButton["text"] = settings.locale.browseButton
    startButton["text"] = settings.locale.startButton
    zipButton["text"] = settings.locale.zipButton
    settingsButton["text"] = settings.locale.settings
settings.onUpdate(Settings.LOCALE, updateButtons)
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
        emptyLabel = ttk.Label(emptyFrame, text=settings.locale.browseLabel)
        emptyLabel.pack(fill=Y, expand=True, anchor=CENTER)
        def updateEmptyFrameLang():
            emptyLabel["text"] = settings.locale.browseLabel
        settings.onUpdate(Settings.LOCALE, updateEmptyFrameLang)
    else:
        destroyEmptyFrame()
    if gameType == GameType.RENPY:
        destroyRenpyFrame()
        renpyFrame = renpy.RenpyFrame(root, filename)
    else:
        destroyRenpyFrame()
showFrame()

test = tk.StringVar()

# show window
root.mainloop()