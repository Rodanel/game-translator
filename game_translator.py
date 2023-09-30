from tkinter import *
from tkinter import filedialog, messagebox, ttk
from os import getcwd
import threading
import traceback
from src.style.buttons import enabledButtonColor, toggle_button_state
from src.style.frame import set_frame_attrs
from src.games import renpy
from src.games.detect_game import detect_game, GameType
from src.utils.settings import settings, Settings

# initialize window
root = Tk()

# set title
root.title("Game Translator by Rodanel")

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

settingsButton = Button(root, text=settings.language.settings, command=lambda:settings.window(root))
settingsButton.pack(side="top", anchor=E)

# set icon
# root.iconbitmap('./assets/icon.ico')

# empty panel
emptyFrame = None
emptyLabel = None

# renpy panel
renpyFrame = None

# globals
filename = StringVar()
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
        toggle_button_state(startButton, "normal")
        toggle_button_state(zipButton, "normal")
    else:
        toggle_button_state(startButton, "disabled")
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
                toggle_button_state(startButton, "disabled")
                renpyFrame.cancel()
                settingsButton["state"] = "normal"
            except:
                toggle_button_state(startButton, "normal")
                settingsButton["state"] = "disabled"
                print(traceback.format_exc())
    else:
        if gameType == GameType.RENPY and renpyFrame is not None:
            try:
                startButton["text"] = settings.language.cancelButton
                started = True
                toggle_button_state(browseButton, "disabled")
                settingsButton["state"] = "disabled"
                renpyFrame.generate_translation()
                startButton["text"] = settings.language.startButton
                toggle_button_state(browseButton, "normal")
                toggle_button_state(startButton, "normal")
                settingsButton["state"] = "normal"
            except Exception as e:
                messagebox.showerror(title=settings.language.errorTitle, message=str(e))
                startButton["text"] = settings.language.startButton
                toggle_button_state(browseButton, "normal")
                toggle_button_state(startButton, "normal")
                settingsButton["state"] = "normal"
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
            toggle_button_state(zipButton, "disabled")
            renpyFrame.archive()
            toggle_button_state(zipButton, "normal")
        except:
            toggle_button_state(zipButton, "normal")
            print(traceback.format_exc())
    pass

def start_zipping():
    start_zipping_thread = threading.Thread(target=zip_game)
    start_zipping_thread.daemon = True
    start_zipping_thread.start()
# buttons

zipButton = Button(root, text=settings.language.zipButton, background=enabledButtonColor, foreground="white", disabledforeground="white", command=lambda:start_zipping())
zipButton.pack(side=BOTTOM, fill=X)
toggle_button_state(zipButton, "disabled")

margin1 = Frame(root, height=5)
margin1.pack(side=BOTTOM, fill=X)

startButton = Button(root, text=settings.language.startButton, background=enabledButtonColor, foreground="white", disabledforeground="white", command=lambda:start_translation())
startButton.pack(side=BOTTOM, fill=X)

margin2 = Frame(root, height=5)
margin2.pack(side=BOTTOM, fill=X)

browseButton = Button(root, text=settings.language.browseButton, background=enabledButtonColor, foreground="white", disabledforeground="white", command=browse_game)
browseButton.pack(side=BOTTOM, fill=X)

toggle_button_state(startButton, "disabled")

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
        emptyLabel = Label(emptyFrame, text=settings.language.browseLabel)
        emptyLabel.pack(side= TOP, fill=X, expand=True, anchor=("center"))
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