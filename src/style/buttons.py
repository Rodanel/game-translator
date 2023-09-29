from tkinter import Button

def toggle_button_state(button: Button, state:str):
    button["state"] = state
    if state == "disabled":
        button["background"] = disabledButtonColor
    else:
        button["background"] = enabledButtonColor

enabledButtonColor = "#008000"
disabledButtonColor = "#386b38"

enabledRedButtonColor = "#FF0000"
disabledRedButtonColor = "#E12626"