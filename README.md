English | [Türkçe](README-tr.md)

# game-translator

# Contents

- [For Translators](#for-translators)
  - [Supported Games](#supported-games)
    - [Renpy](#renpy)
- [For Developers](#for-developers)
  - [Adding Your Language to the Tool](#adding-your-language-to-the-tool)
  - [Building](#building)


# For Translators

- **This tool is still in development and can potentially break your game. So, don't forget to back up your game!**

## Supported Games

### Renpy:

- What it can do:
  - Extract RPA archives (you can ignore the RPA archives you don't need).
  - Decompile RPYC files.
  - Optimize texts for translation.
    - For example (Ren'Py's translation policy):
      - Not translatable: `textbutton "Confirm"`
      - Translatable: `textbutton _("Confirm")`
  - Generate translation files (Of course, that's the purpose of this tool, and it only generates translation files if they don't exist. There's no option for that.)
    - This tool will generate these translations in "game/tl/" if translation files are not exists.
    - To add missing translations, the "Force regenerate the translation files" option must be enabled.
    - Alternatively, simply delete the translation folder inside the "game/tl" directory to generate a clean translation.
  - Automatic translation using Google Translate.
    - This option can help if you don't have time for translations.
    - Depending on the length of dialogues and texts, this process can take some time. Just sit back, do your own things, and wait for the process to finish.
  - You will be notified when the process is completed or if an error occurs.
- What it cannot do:
  - Can not translate graphics (images, videos, etc.).
  - Can not translate texts assigned with variables for now.
    - For example:
    - `$ walkthrough = "Go home and sleep"`
  - And anything else not mentioned above that comes to your mind. :)

- External tools
  - This tool uses a modified version of the UnRen-1.0.11d tool.


# For Developers

## Adding Your Language to the Tool

- Create a copy of the {project-path}/locales/en.json file. And rename as whatever you want.
- Edit the "localeCode" and "localeName" in that copy according to your language.
- The tool will automatically detect this language file as long as it is in the {project-path}/locales/ folder and has the ".json" extension.
- Also it will add to the build in the same way.

## Building

- Install the requirements

```
pip install -r requirements.txt
```

- Build (Builds in "{project-path}/build")

```
python setup.py build
```