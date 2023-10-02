from distutils.core import setup
from glob import glob
import py2exe

app_name = "Game Translator"

setup(
    name= app_name,
    version='0.46',
    author="Rodanel",
    windows=[
    {
        "script": "game_translator.py",
        "icon_resources": [(0, "assets/favicon.ico")],
        "dest_base" : app_name
    }],
    data_files=[('assets', glob('assets/**/*', recursive=True))]
    )