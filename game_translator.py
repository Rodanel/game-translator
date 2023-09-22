from tkinter import *
from tkinter import filedialog, messagebox
from os import getcwd

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
root.resizable(True, True)
root.minsize(window_width, window_height)

# set icon
# root.iconbitmap('./assets/icon.ico')

root.columnconfigure(0, weight= 1)
root.rowconfigure(0, weight= 1)

mainFrame = Frame(root)
mainFrame.grid(column=0, row=0, sticky='nesw')

def browse_game():
    filename = filedialog.askopenfilename(initialdir=getcwd(), title="Select the game executable", filetypes= [("Exe file", "*.exe")])
    gameType = detect_game(filename)
    if gameType == GameType.RENPY:
        messagebox.showinfo(title="Detected a renpy game", message="Detected a renpy game! If this is wrong please report to me.")
    elif gameType == GameType.NONE:
        messagebox.showwarning(title="Not a supported game", message="This is not a supported game!\n\n"+filename)
    if gameType != GameType.NONE and gameType != GameType.EMPTY:
        toggle_state_button(startButton, "normal")
def toggle_state_button(button: Button, state:str):
    button["state"] = state
    if state == "disabled":
        button["background"] = disabledButtonColor
    else:
        button["background"] = enabledButtonColor

enabledButtonColor = "#008000"
disabledButtonColor = "#386b38"

browseButton = Button(root, text="Browse", background=enabledButtonColor, foreground="white", disabledforeground="white", command=browse_game)
browseButton.grid(column=0, row=1, sticky='nesw')

margin1 = Frame(root, height=3)
margin1.grid(column=0, row=2, sticky='nesw')

startButton = Button(root, text="Start", background=enabledButtonColor, foreground="white", disabledforeground="white")
startButton.grid(column=0, row=3, sticky='nesw')

toggle_state_button(startButton, "disabled")

# show window
root.mainloop()