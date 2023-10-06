# game-translator

## External tool

### Renpy

- Used modified version of UnRen-1.0.11d in this tool

## Adding Your Locale

- Create a copy from {project-path}/locales/en.json
- Update "localeCode" and "localeName" for your language in that copy.
- The tools will detect this language automatically.

### Including Your Locale to Build

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