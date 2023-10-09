import sys
from cx_Freeze import setup,Executable
import os
import re

from src.utils.assets import MyAssets
from src.utils.tool import Tool

includefiles = [
    (MyAssets.favicon, MyAssets.favicon),
    (MyAssets.icon, MyAssets.icon),
    ("LICENSE", "LICENSE"),
]

for readmeFile in os.listdir(os.getcwd()):
    if readmeFile.lower().endswith(".md"):
        includefiles.append((readmeFile, readmeFile))   

localesPath = os.path.join(os.getcwd(), Tool.LOCALE_FOLDER_NAME)

if not os.path.exists(os.path.join(localesPath, Tool.DEFAULT_LOCALE_FILE+".json")):
    raise Exception("Default locale file "+Tool.DEFAULT_LOCALE_FILE+".json not found. This locale file required for this tool.")

for locFile in os.listdir(localesPath):
    locFileFullPath = os.path.abspath(os.path.join(localesPath, locFile))
    if os.path.isfile(locFileFullPath) and locFileFullPath.endswith(".json"):
        includefiles.append((locFileFullPath, os.path.join(Tool.LOCALE_FOLDER_NAME, locFile)))

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
