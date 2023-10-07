import json

from os import getcwd, path, listdir

from typing import TypeVar, Type
T = TypeVar('T', bound='Locale')
class Locale(object):

    DEFAULT_LOCALE = "English"

    __KEYNOT_FOUND_ERROR__ = "Locale key not found. Corrupted locale json file."

    def __init__(self, locale:str=None, isBase:bool=False):
        self.__isBase__ = isBase
        if locale is None:
            self.__locale__ = Locale.DEFAULT_LOCALE
        else:
            self.__locale__ = locale
        self.__locales__ = {}
        self.__path__ = path.join(getcwd(), "locales")
        for localeF in listdir(self.__path__):
            if localeF.endswith(".json"):
                with open(path.join(self.__path__, localeF), "r") as localeFile:
                    localeFileContent = json.load(localeFile)
                localeFile.closed
                if "localeCode" in localeFileContent and "localeName" in localeFileContent:
                    self.__locales__[localeFileContent["localeName"]] = localeFileContent
                else:
                    print("Locale file \"{}\" could not load because localeCode or localeName attr is missing.")
    @property
    def base(self):
        return self.__class__(locale=Locale.DEFAULT_LOCALE, isBase=True)

    @property
    def isBase(self):
        return self.__isBase__

    @property
    def locales(self):
        return [key for key,value in self.__locales__.items()]

    @property
    def browseLabel(self):
        try:
            return self.__locales__[self.__locale__]["browseLabel"].format(self.browseButton)
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.browseLabel

    @property
    def browseButton(self):
        try:
            return self.__locales__[self.__locale__]["browseButton"]
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.browseButton
    
    @property
    def startButton(self):
        try:
            return self.__locales__[self.__locale__]["startButton"]
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.startButton
    
    @property
    def zipButton(self):
        try:
            return self.__locales__[self.__locale__]["zipButton"]
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.zipButton
    
    @property
    def settings(self):
        try:
            return self.__locales__[self.__locale__]["settings"]
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.settings
    
    @property
    def languageDot(self):
        try:
            return self.__locales__[self.__locale__]["languageDot"]
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.languageDot
    
    @property
    def cancelButton(self):
        try:
            return self.__locales__[self.__locale__]["cancelButton"]
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.cancelButton
    
    @property
    def saveButton(self):
        try:
            return self.__locales__[self.__locale__]["saveButton"]
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.saveButton
    
    @property
    def selectGameExecutable(self):
        try:
            return self.__locales__[self.__locale__]["selectGameExecutable"]
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.selectGameExecutable
    
    @property
    def exeFile(self):
        try:
            return self.__locales__[self.__locale__]["exeFile"]
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.exeFile
    
    @property
    def detectedRenpyTitle(self):
        try:
            return self.__locales__[self.__locale__]["detectedRenpyTitle"]
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.detectedRenpyTitle
    
    @property
    def detectedRenpyDesc(self):
        try:
            return self.__locales__[self.__locale__]["detectedRenpyDesc"]
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.detectedRenpyDesc

    @property
    def unsupportedGameTitle(self):
        try:
            return self.__locales__[self.__locale__]["unsupportedGameTitle"]
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.unsupportedGameTitle
    
    def unsupportedGame(self, filePath: str):
        try:
            return self.__locales__[self.__locale__]["unsupportedGame"].format(filePath)
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.unsupportedGame
    
    @property
    def errorTitle(self):
        try:
            return self.__locales__[self.__locale__]["errorTitle"]
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.errorTitle

    @property
    def renpyGameTranslation(self):
        try:
            return self.__locales__[self.__locale__]["renpyGameTranslation"]
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.renpyGameTranslation

    def gameName(self, gamePath: str):
        try:
            return self.__locales__[self.__locale__]["gameName"].format(gamePath)
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.gameName(gamePath)
    
    @property
    def languageNameDot(self):
        try:
            return self.__locales__[self.__locale__]["languageNameDot"]
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.languageNameDot
    
    @property
    def languageFolderNameDot(self):
        try:
            return self.__locales__[self.__locale__]["languageFolderNameDot"]
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.languageFolderNameDot
    
    @property
    def lockTranslation(self):
        try:
            return self.__locales__[self.__locale__]["lockTranslation"]
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.lockTranslation
    
    @property
    def extractRPAArhives(self):
        try:
            return self.__locales__[self.__locale__]["extractRPAArhives"]
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.extractRPAArhives

    @property
    def add(self):
        try:
            return self.__locales__[self.__locale__]["add"]
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.add

    @property
    def remove(self):
        try:
            return self.__locales__[self.__locale__]["remove"]
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.remove

    @property
    def decompileRPYCFiles(self):
        try:
            return self.__locales__[self.__locale__]["decompileRPYCFiles"]
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.decompileRPYCFiles

    @property
    def forceRegenerateTranslation(self):
        try:
            return self.__locales__[self.__locale__]["forceRegenerateTranslation"]
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.forceRegenerateTranslation

    @property
    def translateWithGoogle(self):
        try:
            return self.__locales__[self.__locale__]["translateWithGoogle"]
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.translateWithGoogle

    @property
    def translateToDot(self):
        try:
            return self.__locales__[self.__locale__]["translateToDot"]
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.translateToDot
    
    @property
    def noFileAdded(self):
        try:
            return self.__locales__[self.__locale__]["noFileAdded"]
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.noFileAdded
    
    def ignoredRPAArchives(self, archiveFileListSeperated: str):
        try:
            return self.__locales__[self.__locale__]["ignoredRPAArchives"].format(archiveFileListSeperated)
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.ignoredRPAArchives(archiveFileListSeperated=archiveFileListSeperated)

    @property
    def ignoredRPAArchivesSeperator(self):
        try:
            return self.__locales__[self.__locale__]["ignoredRPAArchivesSeperator"]
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.ignoredRPAArchivesSeperator

    def logfileEndDescription(self, filePath: str):
        try:
            return self.__locales__[self.__locale__]["logfileEndDescription"].format(filePath)
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.logfileEndDescription(filePath=filePath)

    def exrtractingFile(self, fileName: str):
        try:
            return self.__locales__[self.__locale__]["exrtractingFile"].format(fileName)
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.exrtractingFile(fileName=fileName)

    def exrtractedFileSuccess(self, fileName: str):
        try:
            return self.__locales__[self.__locale__]["exrtractedFileSuccess"].format(fileName)
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.exrtractedFileSuccess(fileName=fileName)

    @property
    def extractFileErrorTitle(self):
        try:
            return self.__locales__[self.__locale__]["extractFileErrorTitle"]
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.extractFileErrorTitle

    def extractFileError(self, filePath:str, error: str=None):
        try:
            return self.__locales__[self.__locale__]["extractFileError"].format(filePath, self.seeLogs if error is None else error)
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.extractFileError(filePath=filePath, error=error)

    @property
    def seeLogs(self):
        try:
            return self.__locales__[self.__locale__]["seeLogs"]
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.seeLogs

    def ignoredFileWarning(self, fileName: str):
        try:
            return self.__locales__[self.__locale__]["ignoredFileWarning"].format(fileName)
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.ignoredFileWarning(fileName=fileName)

    @property
    def decompilingRpyc(self):
        try:
            return self.__locales__[self.__locale__]["decompilingRpyc"]
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.decompilingRpyc

    @property
    def searchingForRpycFiles(self):
        try:
            return self.__locales__[self.__locale__]["searchingForRpycFiles"]
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.searchingForRpycFiles

    def workingIn(self, folderPath:str):
        try:
            return self.__locales__[self.__locale__]["workingIn"].format(folderPath)
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.workingIn(folderPath=folderPath)

    def decompilingRpycTo(self, rpycFilePath:str, rpyFilePath:str):
        try:
            return self.__locales__[self.__locale__]["decompilingRpycTo"].format(rpycFilePath, rpyFilePath)
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.decompilingRpycTo(rpycFilePath=rpycFilePath, rpyFilePath=rpyFilePath)

    def decompilingRpycFileSkipped(self, rpycFilePath:str):
        try:
            return self.__locales__[self.__locale__]["decompilingRpycFileSkipped"].format(rpycFilePath)
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.decompilingRpycFileSkipped(rpycFilePath=rpycFilePath)
    
    def decompilingRpycError(self, filePath:str):
        try:
            return self.__locales__[self.__locale__]["decompilingRpycError"].format(filePath)
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.decompilingRpycError(filePath=filePath)

    def fileNotFound(self, filePath:str):
        try:
            return self.__locales__[self.__locale__]["fileNotFound"].format(filePath)
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.fileNotFound(filePath=filePath)

    @property
    def noScriptFiles(self):
        try:
            return self.__locales__[self.__locale__]["noScriptFiles"]
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.noScriptFiles

    def decompileRpycSuccess(self, fileCount:str):
        try:
            return self.__locales__[self.__locale__]["decompileRpycSuccess"].format(fileCount)
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.decompileRpycSuccess(fileCount=fileCount)

    def decompileRpycFailed(self, fileCount:str):
        try:
            return self.__locales__[self.__locale__]["decompileRpycFailed"].format(fileCount)
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.decompileRpycFailed(fileCount=fileCount)

    def decompileRpycSuccessAndFail(self, successFileCount:str, failFileCount:str):
        try:
            return self.__locales__[self.__locale__]["decompileRpycSuccessAndFail"].format(successFileCount, failFileCount)
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.decompileRpycSuccessAndFail(successFileCount=successFileCount, failFileCount=failFileCount)

    @property
    def decompilingRpycCompleted(self):
        try:
            return self.__locales__[self.__locale__]["decompilingRpycCompleted"]
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.decompilingRpycCompleted
    
    @property
    def removedTmpFiles(self):
        try:
            return self.__locales__[self.__locale__]["removedTmpFiles"]
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.removedTmpFiles
    
    @property
    def decompileRpycErrorTitle(self):
        try:
            return self.__locales__[self.__locale__]["decompileRpycErrorTitle"]
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.decompileRpycErrorTitle

    def decompileRpycError(self, error: str=None):
        try:
            return self.__locales__[self.__locale__]["decompileRpycError"].format(self.seeLogs if error is None else error)
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.decompileRpycError(error=error)

    @property
    def translationSkipped(self):
        try:
            return self.__locales__[self.__locale__]["translationSkipped"]
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.translationSkipped

    @property
    def regeneratingTranslation(self):
        try:
            return self.__locales__[self.__locale__]["regeneratingTranslation"]
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.regeneratingTranslation

    @property
    def generatingTranslation(self):
        try:
            return self.__locales__[self.__locale__]["generatingTranslation"]
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.generatingTranslation

    @property
    def generatedTranslation(self):
        try:
            return self.__locales__[self.__locale__]["generatedTranslation"]
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.generatedTranslation

    @property
    def generatingTranslationErrorTitle(self):
        try:
            return self.__locales__[self.__locale__]["generatingTranslationErrorTitle"]
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.generatingTranslationErrorTitle

    def generatingTranslationError(self, error: str=None):
        try:
            return self.__locales__[self.__locale__]["generatingTranslationError"].format(self.seeLogs if error is None else error)
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.generatingTranslationError(error=error)
    
    def translating(self, filePath: str):
        try:
            return self.__locales__[self.__locale__]["translating"].format(filePath)
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.translating(filePath=filePath)

    def translatingSkipped(self, filePath: str):
        try:
            return self.__locales__[self.__locale__]["translatingSkipped"].format(filePath)
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.translatingSkipped(filePath=filePath)
    
    @property
    def connectingGoogleTrans(self):
        try:
            return self.__locales__[self.__locale__]["connectingGoogleTrans"]
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.connectingGoogleTrans

    def fileTranslatedInSeconds(self, seconds:int):
        try:
            return self.__locales__[self.__locale__]["fileTranslatedInSeconds"].format(str(seconds))
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.fileTranslatedInSeconds(seconds=seconds)

    def translatingFileSuccess(self, filePath: str):
        try:
            return self.__locales__[self.__locale__]["translatingFileSuccess"].format(filePath)
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.translatingFileSuccess(filePath=filePath)

    @property
    def translatingSuccess(self):
        try:
            return self.__locales__[self.__locale__]["translatingSuccess"]
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.translatingSuccess

    def translationFolderNotFound(self, folderPath: str):
        try:
            return self.__locales__[self.__locale__]["translationFolderNotFound"].format(folderPath)
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.translationFolderNotFound(folderPath=folderPath)
    
    @property
    def translationFailedTitle(self):
        try:
            return self.__locales__[self.__locale__]["translationFailedTitle"]
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.translationFailedTitle
    
    def translationFailed(self, error: str=None):
        try:
            return self.__locales__[self.__locale__]["translationFailed"].format(self.seeLogs if error is None else error)
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.translationFailed(error=error)

    def lockingTranslation(self, languageName: str, languageFolderName: str):
        try:
            return self.__locales__[self.__locale__]["lockingTranslation"].format(languageName, languageFolderName)
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.lockingTranslation(languageName=languageName, languageFolderName=languageFolderName)
    
    @property
    def lookingExistedLockFile(self):
        try:
            return self.__locales__[self.__locale__]["lookingExistedLockFile"]
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.lookingExistedLockFile
    
    def lockFileFoundLoc(self, filePath: str):
        try:
            return self.__locales__[self.__locale__]["lockFileFoundLoc"].format(filePath)
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.lockFileFoundLoc(filePath=filePath)
    
    @property
    def lockFileNotFound(self):
        try:
            return self.__locales__[self.__locale__]["lockFileNotFound"]
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.lockFileNotFound
    
    def lockFileCreated(self, languageName: str, languageFolderName: str, lockFileName:str):
        try:
            return self.__locales__[self.__locale__]["lockFileCreated"].format(languageName, languageFolderName, lockFileName)
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.lockFileCreated(languageName=languageName, languageFolderName=languageFolderName, lockFileName=lockFileName)
    
    @property
    def lockFileFailedTitle(self):
        try:
            return self.__locales__[self.__locale__]["lockFileFailedTitle"]
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.lockFileFailedTitle
    
    def lockFileFailed(self, error: str=None):
        try:
            return self.__locales__[self.__locale__]["lockFileFailed"].format(self.seeLogs if error is None else error)
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.lockFileFailed(error=error)

    @property
    def languageSettingsDesc(self):
        try:
            return self.__locales__[self.__locale__]["languageSettingsDesc"]
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.languageSettingsDesc

    @property
    def translationCancelledByUser(self):
        try:
            return self.__locales__[self.__locale__]["translationCancelledByUser"]
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.translationCancelledByUser

    @property
    def translationCompletedTitle(self):
        try:
            return self.__locales__[self.__locale__]["translationCompletedTitle"]
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.translationCompletedTitle

    @property
    def translationCompleted(self):
        try:
            return self.__locales__[self.__locale__]["translationCompleted"]
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.translationCompleted

    @property
    def googleTransCanNotBeEmpty(self):
        try:
            return self.__locales__[self.__locale__]["googleTransCanNotBeEmpty"]
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.googleTransCanNotBeEmpty

    @property
    def languageNameInvalid(self):
        try:
            return self.__locales__[self.__locale__]["languageNameInvalid"]
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.languageNameInvalid

    @property
    def languageFolderNameInvalid(self):
        try:
            return self.__locales__[self.__locale__]["languageFolderNameInvalid"]
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.languageFolderNameInvalid

    @property
    def cancellingTranslation(self):
        try:
            return self.__locales__[self.__locale__]["cancellingTranslation"]
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.cancellingTranslation

    def zipStarted(self, archivePath: str):
        try:
            return self.__locales__[self.__locale__]["zipStarted"].format(archivePath)
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.zipStarted(arhivePath=archivePath)

    def addedFileToArchive(self, filePath: str):
        try:
            return self.__locales__[self.__locale__]["addedFileToArchive"].format(filePath)
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.addedFileToArchive(filePath=filePath)

    def createdArchiveSuccess(self, archivePath: str):
        try:
            return self.__locales__[self.__locale__]["createdArchiveSuccess"].format(archivePath)
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.createdArchiveSuccess(archivePath=archivePath)

    @property
    def creatingArchiveErrorTitle(self):
        try:
            return self.__locales__[self.__locale__]["creatingArchiveErrorTitle"]
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.creatingArchiveErrorTitle

    def creatingArchiveError(self, error: str=None):
        try:
            return self.__locales__[self.__locale__]["creatingArchiveError"].format(self.seeLogs if error is None else error)
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.creatingArchiveError(error=error)

    @property
    def optimizeTexts(self):
        try:
            return self.__locales__[self.__locale__]["optimizeTexts"]
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.optimizeTexts

    def optimizeTextsErrorDesc(self, error: str=None):
        try:
            return self.__locales__[self.__locale__]["optimizeTextsErrorDesc"].format(self.seeLogs if error is None else error)
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.optimizeTextsErrorDesc(error=error)
    
    @property
    def startedOptimizingTexts(self):
        try:
            return self.__locales__[self.__locale__]["startedOptimizingTexts"]
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.startedOptimizingTexts
    
    def optimizingFile(self, filePath: str):
        try:
            return self.__locales__[self.__locale__]["optimizingFile"].format(filePath)
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.optimizingFile(filePath=filePath)
    
    def optimizedTextAndButtons(self, count: int):
        try:
            return self.__locales__[self.__locale__]["optimizedTextAndButtons"].format(str(count))
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.optimizedTextAndButtons(count=count)
    
    @property
    def alreadyActiveTitle(self):
        try:
            return self.__locales__[self.__locale__]["alreadyActiveTitle"]
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.alreadyActiveTitle
    
    @property
    def settingsWindowAlreadyActive(self):
        try:
            return self.__locales__[self.__locale__]["settingsWindowAlreadyActive"]
        except:
            if self.isBase:
                raise Exception(Locale.__KEYNOT_FOUND_ERROR__)
            else:
                return self.base.settingsWindowAlreadyActive