# game-translator

## Renpy

### What it can do:

- **First and most important thing: Since this tool is still in development, it can potentially break your game! Don't forget to back up your game!**
- Extract RPA archives (You can ignore specific RPA archives).
- Decompile RPYC files.
- Optimize texts for translation.
  - For example (Renpy's translation policy):
    - Not translatable: `textbutton "Confirm"`
    - Translatable: `textbutton _("Confirm")`
- Create a translation file (Of course this is the tool's purpose, and it will automatically create translation files if they don't exist. There's no option for this.)
  - This tool will automatically create the translation folder in the "game/tl/" directory if it doesn't exist.
  - To add missing or new texts, you need to enable the "Force regenerate translation files" option.
  - Alternatively, delete your translation folder in the "game/tl" directory to generate a clean translation.
- Automatic translation using Google Translate.
  - This option can be helpful if you don't have time for translation.
  - Depending on the length of dialogues and texts, this process may take a while. Just do your own things and wait for the translation to complete.
- You'll be notified with a message box upon completion of the translation or if an error occurs.

### What it can't do:

- Cannot translate graphics (images, videos, etc.).
- Cannot translate text assigned with variables (for now).
  - For example:
  - `$ walkthrough = "Go home and sleep"`
- And anything that comes to mind and is not mentioned above. :)


### External tools

- Used modified version of UnRen-1.0.11d in this tool

## Adding Your Language

- Create a copy from {project-path}/locales/en.json
- Update "localeCode" and "localeName" for your language in that copy.
- The tools will detect this language automatically.

### Including Your Language to Build

- Open setup.py and find this comment line:

```
# Add your locale here
```

- And add your locale file after that comment lines:

```
# Your locale file should be inside "locales/" folder
localeFiles.append("your_locale_file_name") # DO NOT INCLUDE "locales/" folder. Only file name with or without extension
```


## Building

- Install requirements

```
pip install -r requirements.txt
```

- Build (Builds in "{project_folder}/build")

```
python setup.py build
```