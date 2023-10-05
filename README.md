# game-translator

## External tool

### Renpy

- Used modified version of UnRen-1.0.11d in this tool

## Adding your language to tool

- Create a file to: {project-path}/src/utils/languages/{your_language}.py
- Copy content of {project-path}/src/utils/languages/base.py and paste in the file you previously created.

- Replace this in your language file.

```
from typing import TypeVar, Type # You can remove this line
T = TypeVar('T', bound='LanguageBase') # You can remove this line

from src.utils.languages.base import LanguageBase # Add this line

class LanguageBase(object): # Replace to: class YourLanguage(LanguageBase):

    # IMPORTANT: "base" variable should return LanguageBase class. If you don't change it, It will be return itself.
    #            It's important for logging in english.
    @classmethod
    @property
    def base(cls: Type[T]) -> T:    # Replace to: def base(cls) -> LanguageBase:
        return cls                  # Replace to: return LanguageBase 
    ...
```

- Example Language File:

```
from src.utils.languages.base import LanguageBase

class French(LanguageBase):
    
    @classmethod
    @property
    def base(cls) -> LanguageBase:
        return LanguageBase
    ...
```


- And add your language and conditions in {project-path}/src/utils/languages/enum.py
- Example:

```
class Language(Enum):
    ENGLISH = 0
    TURKISH = 1
    YOURLANGUAGE = 2                             # Add this // Will be called with "Language.YOURLANGUAGE"
    def __str__(self):
        if self == Language.TURKISH:
            return "Türkçe"
        elif self == Language.YOURLANGUAGE:      # Add this
            return "Your Language Name"          # Add this
        else:
            return "English"
    @classmethod
    def fromStr(cls, lang) -> LanguageBase:
        if lang == str(Language.TURKISH):
            return Turkish
        elif lang == str(Language.YOURLANGUAGE): # Add this
            return YourLanguage                  # Add this / this is the class name in the language file you created
        else:
            return LanguageBase
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