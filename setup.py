import sys
from cx_Freeze import setup,Executable
import os

from src.utils.assets import MyAssets
from src.utils.tool import Tool

includefiles = [
    (MyAssets.favicon, MyAssets.favicon),
    (MyAssets.icon, MyAssets.icon),
    ("README.md", "README.md"),
    ("LICENSE", "LICENSE"),
]

localeFiles = ["en", "tr"]

# Add your locale here
# localeFiles.append("your_locale_file_name")
#
# Your locale file should be inside locales/ folder.
# DO NOT INCLUDE "locales/" folder. Only file name with or without extension
#
# Example:
# localeFiles.append("fr")
# Or:
# localeFiles.append("fr.json")

for locFile in localeFiles:
    locFilePath = os.path.join("locales", locFile if locFile.endswith(".json") else locFile+".json")
    includefiles.append((locFilePath, locFilePath))

PYTHON_DLLS_DIR = None

for pypath in sys.path:
    if pypath.endswith("DLLs"):
        PYTHON_DLLS_DIR = pypath
        break

if PYTHON_DLLS_DIR is not None:
    includefiles.append((os.path.join(PYTHON_DLLS_DIR, 'tk86t.dll'), os.path.join('lib', 'tk86t.dll')))
    includefiles.append((os.path.join(PYTHON_DLLS_DIR, 'tcl86t.dll'), os.path.join('lib', 'tcl86t.dll')))

includes = ['certifi', 'chardet', 'googletrans', 'h11', 'h2', 'hpack', 'hstspreload', 'httpcore', 'httpx',
            'hyperframe', 'idna', 'lief', 'rfc3986', 'sniffio', 'tkinter', 'ttkbootstrap']
excludes = ['_gtkagg', '_tkagg', 'test', 'curses', 'pywin.debugger', 'pywin.debugger.dbgcon', 'pywin.dialogs', 
            'cx-Freeze', 'cx-Logging==3.1.0']
packages = ['tkinter','ttkbootstrap']
base = None
if sys.platform == "win32":
    base = "Win32GUI"
setup(
    name = Tool.NAME,
    description = Tool.DESCRIPTION,
    version = Tool.VERSION,
    author = Tool.AUTHOR,
    options = {'build_exe': {'includes':includes,'excludes':excludes,'packages':packages,'include_files':includefiles}},
    executables = [Executable('game_translator.py', target_name="Game Translator", icon='assets/favicon.ico', copyright="Copyright © Rodanel 2023", base = base)]
)
