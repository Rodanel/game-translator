from enum import Enum
from src.utils.languages.base import LanguageBase
from src.utils.languages.turkish import Turkish

class Language(Enum):
    ENGLISH = 0
    TURKISH = 1
    def __str__(self):
        if self == Language.TURKISH:
            return "Türkçe"
        else:
            return "English"
    @classmethod
    def fromStr(cls, lang) -> LanguageBase:
        if lang == str(Language.TURKISH):
            return Turkish
        else:
            return LanguageBase