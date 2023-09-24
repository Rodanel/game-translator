from tkinter import *
from tkinter import filedialog, messagebox
from os import getcwd
import threading

from src.style.buttons import enabledButtonColor, toggle_button_state
from src.style.frame import set_frame_attrs
from src.translate import renpy
from src.detect_game import detect_game, GameType

# initialize window
root = Tk()

# set title
root.title("Game Translator by Rodanel")

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
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
root.resizable(False, False)
root.minsize(window_width, window_height)

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
        emptyLabel = Label(emptyFrame, text="Click \"Browse\" for selecting a game")
        emptyLabel.pack(side= TOP, fill=X, expand=True, anchor=("center"))
    else:
        destroyEmptyFrame()
    if gameType == GameType.RENPY:
        destroyRenpyFrame()
        renpyFrame = renpy.RenpyFrame(root, filename)
    else:
        destroyRenpyFrame()
showFrame()

# select game excutable
def browse_game():
    global filename, gameType
    filename = filedialog.askopenfilename(initialdir=getcwd(), title="Select the game executable", filetypes= [("Exe file", "*.exe")])
    gameType = detect_game(filename)
    if gameType == GameType.RENPY:
        messagebox.showinfo(title="Detected a renpy game", message="Detected a renpy game! If this is wrong please report to me.")
    elif gameType == GameType.NONE:
        messagebox.showwarning(title="Not a supported game", message="This is not a supported game!\n\n"+filename)
    if gameType != GameType.NONE and gameType != GameType.EMPTY:
        toggle_button_state(startButton, "normal")
    else:
        toggle_button_state(startButton, "disabled")
    showFrame()

# start translation
def translate():
    global filename, gameType
    if gameType == GameType.RENPY and renpyFrame is not None:
        try:
            toggle_button_state(startButton, "disabled")
            renpy.translate(renpyFrame)
            toggle_button_state(startButton, "normal")
        except Exception as e:
            messagebox.showerror(title="Error", message=str(e))
            toggle_button_state(startButton, "normal")
    elif gameType == GameType.NONE:
        messagebox.showwarning(title="Not a supported game", message="This is not a supported game!\n\n"+filename)

def start_translation():
    global start_translation_thread
    start_translation_thread = threading.Thread(target=translate)
    start_translation_thread.daemon = True
    start_translation_thread.start()

# buttons

startButton = Button(root, text="Start", background=enabledButtonColor, foreground="white", disabledforeground="white", command=lambda:start_translation())
startButton.pack(side=BOTTOM, fill=X)

margin1 = Frame(root, height=5)
margin1.pack(side=BOTTOM, fill=X)

browseButton = Button(root, text="Browse", background=enabledButtonColor, foreground="white", disabledforeground="white", command=browse_game)
browseButton.pack(side=BOTTOM, fill=X)

toggle_button_state(startButton, "disabled")

# show window
root.mainloop()