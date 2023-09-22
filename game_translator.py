from tkinter import *
from tkinter import filedialog, messagebox
from os import getcwd

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
window_height = 200

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

root.grid_columnconfigure(1, weight= 1)
root.grid_rowconfigure(0, weight= 1)

mainFrame = Frame(root)
mainFrame.grid(column=0, row=0, sticky='nesw')

placeholderFrame = Frame(root)
placeholderFrame.grid(column=0, row=1)

# empty panel
emptyFrame = None
emptyLabel = None

# renpy panel
renpyFrame = None

# globals
filename = StringVar()
gameType = GameType.EMPTY

# find current frame
def showFrame():
    global gameType, filename, emptyFrame, emptyLabel, renpyFrame
    print(str(gameType))
    if gameType == GameType.NONE or gameType == GameType.EMPTY:
        set_frame_attrs(emptyFrame, mainFrame)
        emptyLabel = Label(emptyFrame, text="Click \"Browse\" for selecting a game")
        emptyLabel.grid(column=1, row=0, columnspan=2, sticky="nesw")
    else:
        if emptyLabel is not None:
            emptyLabel.destroy()
        emptyLabel = None
        if emptyFrame is not None:
            emptyFrame.destroy()
        emptyFrame = None
    if gameType == GameType.RENPY:
        renpyFrame = renpy.RenpyFrame(mainFrame, filename)
    else:
        if renpyFrame is not None:
            renpyFrame.destroy()
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
def start_translation():
    global filename, gameType, renpyLanguageName, renpyLockLocalizationBool
    if gameType == GameType.RENPY and renpyFrame is not None:
        renpy.translate(renpyFrame)
    elif gameType == GameType.NONE:
        messagebox.showwarning(title="Not a supported game", message="This is not a supported game!\n\n"+filename)

# buttons
browseButton = Button(root, text="Browse", background=enabledButtonColor, foreground="white", disabledforeground="white", command=browse_game)
browseButton.grid(column=0, row=20, columnspan=2, sticky='nesw')

margin1 = Frame(root, height=5)
margin1.grid(column=0, row=21, columnspan=2, sticky='nesw')

startButton = Button(root, text="Start", background=enabledButtonColor, foreground="white", disabledforeground="white", command=start_translation)
startButton.grid(column=0, row=22, columnspan=2, sticky='nesw')

toggle_button_state(startButton, "disabled")

# show window
root.mainloop()