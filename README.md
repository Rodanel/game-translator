# game-translator

## External tool

### Renpy

- UnRen-1.0.11d used in this tool as rpa extractor and rpyc decompiler
    - Contains unrpyc from (CensoredUsername/unrpyc)[https://github.com/CensoredUsername/unrpyc]

## Building

- Install pyinstaller

```
pip install -U pyinstaller
```

- Build

```
pyinstaller --noconsole --name "Game Translator" game_translator.py
```