from typing import TypeVar, Type
T = TypeVar('T', bound='LanguageBase')
class LanguageBase(object):

    @classmethod
    @property
    def base(cls: Type[T]) -> T:
        return cls

    @classmethod
    @property
    def browseLabel(cls):
        return "Click \""+LanguageBase.browseButton+"\" for selecting a game"

    @classmethod
    @property
    def browseButton(cls):
        return "Browse"
    
    @classmethod
    @property
    def startButton(cls):
        return "Start"
    
    @classmethod
    @property
    def zipButton(cls):
        return "Create an Archive (.zip)"
    
    @classmethod
    @property
    def settings(cls):
        return "Settings"
    
    @classmethod
    @property
    def languageDot(cls):
        return "Language:"
    
    @classmethod
    @property
    def cancelButton(cls):
        return "Cancel"
    
    @classmethod
    @property
    def saveButton(cls):
        return "Save"
    
    @classmethod
    @property
    def selectGameExecutable(cls):
        return "Select the game's executable:"
    
    @classmethod
    @property
    def exeFile(cls):
        return "Exe file"
    
    @classmethod
    @property
    def detectedRenpyTitle(cls):
        return "Detected a renpy game"
    
    @classmethod
    @property
    def detectedRenpyDesc(cls):
        return "This tool may not be suitable for renpy versions of some games. And it may broke your game.\n\nDon't forget to backup the game!\n\nIf you encounter an error, please let me know."
    
    @classmethod
    @property
    def unsupportedGameTitle(cls):
        return "Unsupported Game"
    
    @classmethod
    def unsupportedGame(cls, filePath: str):
        return "This is not a supported game!\n\n"+filePath
    
    @classmethod
    @property
    def errorTitle(cls):
        return "Error"

    @classmethod
    @property
    def renpyGameTranslation(cls):
        return "Renpy Game Translation"

    @classmethod
    def gameName(cls, filePath: str):
        return "Game: "+filePath
    
    @classmethod
    @property
    def languageNameDot(cls):
        return "Language Name:"
    
    @classmethod
    @property
    def languageFolderNameDot(cls):
        return "Language Folder Name:"
    
    @classmethod
    @property
    def lockTranslation(cls):
        return "Lock the game to this translation."
    
    @classmethod
    @property
    def extractRPAArhives(cls):
        return "Extract RPA archives."

    @classmethod
    @property
    def add(cls):
        return "Add"

    @classmethod
    @property
    def remove(cls):
        return "Remove"

    @classmethod
    @property
    def decompileRPYCFiles(cls):
        return "Decompile RPYC files."

    @classmethod
    @property
    def forceRegenerateTranslation(cls):
        return "Force Regenerate Translation Files. (Adds only missing translations.)"

    @classmethod
    @property
    def translateWithGoogle(cls):
        return "Translate with Google Translate (Experimental and increases completion time)."

    @classmethod
    @property
    def translateToDot(cls):
        return "Translate to:"
    
    @classmethod
    @property
    def noFileAdded(cls):
        return "No file added."
    
    @classmethod
    def ignoredRPAArchives(cls, arhiveFileListSeperated: str):
        return "Ignored RPA Archives: " + arhiveFileListSeperated

    @classmethod
    @property
    def ignoredRPAArchivesSeperator(cls):
        return ", " # This is rpa file seperator for ignoredRPAArchives.

    @classmethod
    def logfileEndDescription(cls, filePath: str):
        return "You can find this log file in "+filePath+" later."

    @classmethod
    def exrtractingFile(cls, fileName: str):
        return "Extracting \""+fileName+"\"..."

    @classmethod
    def exrtractedFileSuccess(cls, fileName: str):
        return "Extracted \""+fileName+"\" successfully!"

    @classmethod
    @property
    def extractFileErrorTitle(cls):
        return "Could not extract archive"

    @classmethod
    def extractFileError(cls, filePath:str, error: str=None):
        if error is None:
            return "Could not extract \""+filePath+"\" archive.\n\nSee logs for details."
        else:
            return "Could not extract \""+filePath+"\" archive.\n\n"+error

    @classmethod
    def ignoredFileWarning(cls, fileName: str):
        return "Ignored \""+fileName+"\"..."

    @classmethod
    @property
    def decompilingRpyc(cls):
        return "Decompiling rpyc files..."

    @classmethod
    @property
    def searchingForRpycFiles(cls):
        return "Searching for rpyc files..."

    @classmethod
    def workingIn(cls, folderPath:str):
        return "Working in \""+folderPath+"\""

    @classmethod
    def decompilingRpycTo(cls, rpycFilePath:str, rpyFilePath:str):
        return "Decompiling \""+rpycFilePath+"\" to \""+rpyFilePath+"\"..."

    @classmethod
    def decompilingRpycFileSkipped(cls, rpycFilePath:str):
        return "\""+rpycFilePath+"\" already exists - skipped"
    
    @classmethod
    def decompilingRpycError(cls, filePath:str):
        return "Error while decompiling \""+filePath+"\":"

    @classmethod
    def fileNotFound(cls, filePath:str):
        return "File not found: \""+filePath+"\""

    @classmethod
    @property
    def noScriptFiles(cls):
        return "No script files to decompile."

    @classmethod
    def decompileRpycSuccess(cls, fileCount:str, isMultipleFiles:bool):
        return "Decompilation of "+fileCount+" script file%s successful." % ("s" if isMultipleFiles else "")

    @classmethod
    def decompileRpycFailed(cls, fileCount:str, isMultipleFiles:bool):
        return "Decompilation of "+fileCount+" file%s failed." % ("s" if isMultipleFiles else "")

    @classmethod
    def decompileRpycSuccessAndFail(cls, successFileCount:str, isSuccessMultipleFiles:bool, failFileCount:str, isFailMultipleFiles:bool, ):
        return "Decompilation of "+successFileCount+" file%s successful, but decompilation of "+failFileCount+" file%s failed" % ("s" if isSuccessMultipleFiles else "", "s" if isFailMultipleFiles else "")
    
    @classmethod
    @property
    def decompilingRpycCompleted(cls):
        return "Decompiling rpyc files completed. Removing temp files..."
    
    @classmethod
    @property
    def removedTmpFiles(cls):
        return "Temp files removed successfully!"
    
    @classmethod
    @property
    def decompileRpycErrorTitle(cls):
        return "Could not decompile"

    @classmethod
    def decompileRpycError(cls, error: str=None):
        if error is None:
            return "Could not decompile rpyc files.\n\nSee logs for details."
        else:
            return "Could not decompile rpyc files.\n\n"+error

    @classmethod
    @property
    def translationSkipped(cls):
        return "Generation of translation files skipped, because translation folder already exists and force regenerate is disabled."

    @classmethod
    @property
    def regeneratingTranslation(cls):
        return "Regenerating translation files..."

    @classmethod
    @property
    def generatingTranslation(cls):
        return "Generating translation files..."

    @classmethod
    @property
    def generatedTranslation(cls):
        return "Generated translation files successfully."

    @classmethod
    @property
    def generatingTranslationErrorTitle(cls):
        return "Could not create translation"

    @classmethod
    def generatingTranslationError(cls, error: str=None):
        if error is None:
            return "Could not create translation files.\n\nSee logs for details."
        else:
            return "Could not create translation files.\n\n"+error
    
    @classmethod
    def translating(cls, filePath: str):
        return "Translating \""+filePath+"\"..."

    @classmethod
    def translatingSkipped(cls, filePath: str):
        return "Translation of \""+filePath+"\" skipped. Because it's already translated!"
    
    @classmethod
    @property
    def connectingGoogleTrans(cls):
        return "Connecting with google translate. Depending on the length of the dialogues in file, this may take time..."

    @classmethod
    def stringsTranslated(cls, seconds:int):
        return "Strings translated in "+str(seconds)+ " second%s!" % ("s" if seconds > 1 else "")

    @classmethod
    def translatingFileSuccess(cls, filePath: str):
        return "Translation of \""+filePath+"\" successfull!" 

    @classmethod
    @property
    def translatingSuccess(cls):
        return "Translation completed! Please launch the game and check if has any error."

    @classmethod
    def translationFolderNotFound(cls, folderPath: str):
        return "Translation folder \""+folderPath+"\" not found!"
    
    @classmethod
    @property
    def translationFailedTitle(cls):
        return "Translation Failed"
    
    @classmethod
    def translationFailed(cls, error: str=None):
        if error is None:
            return "Translation failed!\n\nSee logs for details."
        else:
            return "Translation failed!\n\n"+error

    @classmethod
    def lockingTranslation(cls, languageName: str, languageFolderName: str):
        return "Language locking to "+languageName+" ("+languageFolderName+")..."
    
    @classmethod
    @property
    def lookingExistedLockFile(cls):
        return "Looking for existed lock file."
    
    @classmethod
    def lockFileFoundLoc(cls, filePath: str):
        return "Lock file found in \""+filePath+"\" and removed.\nCreating new one..."
    
    @classmethod
    @property
    def lockFileNotFound(cls):
        return "Lock file not found, creating one..."
    
    @classmethod
    def lockFileCreated(cls, languageName: str, languageFolderName: str, lockFileName:str):
        return "Language locked to "+languageName+" ("+languageFolderName+"). For unlocking just delete \""+lockFileName+"\" file."
    
    @classmethod
    @property
    def lockFileFailedTitle(cls):
        return "Could not create lock file"
    
    @classmethod
    def lockFileFailed(cls, error: str=None):
        if error is None:
            return "Could not create translation lock file.\n\nSee logs for details."
        else:
            return "Could not create translation lock file.\n\n"+error

    @classmethod
    @property
    def languageSettingsDesc(cls):
        return "\nAdd this code to \"screen preferences():\" in screens.rpy. Replace English with game's orijinal language."

    @classmethod
    @property
    def translationCancelledByUser(cls):
        return "Translation cancelled by user!"

    @classmethod
    @property
    def translationCompletedTitle(cls):
        return "Translation Completed"

    @classmethod
    @property
    def translationCompleted(cls):
        return "Translation completed successfully!"

    @classmethod
    @property
    def googleTransCanNotBeEmpty(cls):
        return "Google translate language can not be empty."

    @classmethod
    @property
    def languageNameInvalid(cls):
        return "Language name can not be empty."

    @classmethod
    @property
    def languageFolderNameInvalid(cls):
        return "Language folder name should be at least 3 characters and contain only lowercase english characters."

    @classmethod
    @property
    def cancellingTranslation(cls):
        return "Cancelling translation. It can take long according to background processes..."

    @classmethod
    def zipStarted(cls, arhivePath: str):
        return "Started generating a zip archive in \""+arhivePath+"\"..."

    @classmethod
    def addedFileToArchive(cls, filePath: str):
        return "Added \""+filePath+"\" file to archive."

    @classmethod
    def createdArchiveSuccess(cls, archivePath: str):
        return "Created archive in \""+archivePath+"\" successfully!"

    @classmethod
    @property
    def creatingArchiveErrorTitle(cls):
        return "Could not Create an Archive"

    @classmethod
    def creatingArchiveError(cls, error: str):
        return "Archive could not be created!\n\nError: "+error

    @classmethod
    @property
    def optimizeTexts(cls):
        return "Optimize texts and textbuttons for translation."

    @classmethod
    @property
    def errorTitle(cls):
        return "Error!"

    @classmethod
    def optimizeTextsErrorDesc(cls, error: str=None):
        if error is None:
            return "Could not optimize texts and text buttons.\n\nSee logs for details."
        else:
            return "Could not optimize texts and text buttons.\n\n"+error
    
    @classmethod
    @property
    def startedOptimizingTexts(cls):
        return "Started optimizing text and textbuttons."
    
    @classmethod
    def optimizingFile(cls, filePath: str):
        return "Optimizing text and textbutton in "+filePath
    
    @classmethod
    def optimizedTextAndButtons(cls, count: int):
        if count == 0:
            return "No text or textbutton found."
        else:
            return str(count)+" string%s optimized." % ("s" if count > 1 else "")
    
    @classmethod
    @property
    def alreadyActiveTitle(cls):
        return "Already Active"
    
    @classmethod
    @property
    def settingsWindowAlreadyActive(cls):
        return "Settings window already is active."