from enum import Enum
from os import path
class GameType(Enum):
    EMPTY = -1
    NONE = 0
    RENPY = 1
    def __str__(self):
        if self == GameType.EMPTY:
            return "empty"
        elif self == GameType.NONE:
            return "none"
        elif self == GameType.RENPY:
            return "renpy"
        else:
            return super.__str__(self)

def detect_game(filename: str) -> GameType:
    if filename == "" or filename is None:
        print("Selection cancelled by user!")
        return GameType.EMPTY

    dirname = path.dirname(filename)
    print("Selected Directory: "+dirname)

    # Check renpy
    if path.exists(path.join(dirname, "game")) and path.exists(path.join(dirname, "lib")) and path.exists(path.join(dirname, "renpy")):
        return GameType.RENPY

    return GameType.NONE