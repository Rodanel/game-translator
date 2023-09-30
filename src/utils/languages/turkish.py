from src.utils.languages.base import LanguageBase

class Turkish(LanguageBase):
    
    @classmethod
    @property
    def browseLabel(cls):
        return "Oyun seçmek için \""+LanguageBase.browseButton+"\" butonuna tıklayın"

    @classmethod
    @property
    def browseButton(cls):
        return "Gözat"
    
    @classmethod
    @property
    def startButton(cls):
        return "Başlat"
    
    @classmethod
    @property
    def zipButton(cls):
        return "Arşiv Oluştur (.zip)"
    
    @classmethod
    @property
    def settings(cls):
        return "Ayarlar"
    
    @classmethod
    @property
    def languageDot(cls):
        return "Dil:"
    
    @classmethod
    @property
    def cancelButton(cls):
        return "İptal"
    
    @classmethod
    @property
    def saveButton(cls):
        return "Kaydet"
    
    @classmethod
    @property
    def selectGameExecutable(cls):
        return "Oyunun .exe dosyasını seçin:"
    
    @classmethod
    @property
    def exeFile(cls):
        return "Exe dosyası"
    
    @classmethod
    @property
    def detectedRenpyTitle(cls):
        return "Renpy oyunu tespit edildi"
    
    @classmethod
    @property
    def detectedRenpyDesc(cls):
        return "Renpy oyunu tespit edildi! Bu yanlış ise lütfen bana bildirin."
    
    @classmethod
    @property
    def unsupportedGameTitle(cls):
        return "Desteklemeyen Oyun"
    
    @classmethod
    def unsupportedGame(cls, filePath: str):
        return "Bu desteklenmeyen bir oyun!\n\n"+filePath
    
    @classmethod
    @property
    def errorTitle(cls):
        return "Hata"

    @classmethod
    @property
    def renpyGameTranslation(cls):
        return "Renpy Oyun Çevirisi"

    @classmethod
    def gameName(cls, filePath: str):
        return "Oyun: "+filePath
    
    @classmethod
    @property
    def languageNameDot(cls):
        return "Dil Adı:"
    
    @classmethod
    @property
    def languageFolderNameDot(cls):
        return "Dil Klasörü Adı:"
    
    @classmethod
    @property
    def lockTranslation(cls):
        return "Oyunu bu dile kilitle. (Bu seçenek seçiliyse, oyunu bu dile kilitler ve dil ayarı eklemek için screens.rpy dosyasını düzenlemenize gerek kalmaz.)"
    
    @classmethod
    @property
    def extractRPAArhives(cls):
        return "RPA arşivlerini çıkar."

    @classmethod
    @property
    def add(cls):
        return "Ekle"

    @classmethod
    @property
    def remove(cls):
        return "Kaldır"

    @classmethod
    @property
    def decompileRPYCFiles(cls):
        return "RPYC dosyalarını RPY dosyasına dönüştür."

    @classmethod
    @property
    def forceRegenerateTranslation(cls):
        return "Çeviri klasörünü tekrar oluşturmaya zorla. (Sadece eksik çevirileri tekrar oluşturur.)"

    @classmethod
    @property
    def translateWithGoogle(cls):
        return "Google Çeviri Kulanarak Çevir (Deneysel ve tamamlanma süresini arttırır.)."

    @classmethod
    @property
    def translateToDot(cls):
        return "Şu dile çevir:"
    
    @classmethod
    @property
    def noFileAdded(cls):
        return "Dosya eklenmedi."
    
    @classmethod
    def ignoredRPAArchives(cls, arhiveFileListSeperated: str):
        return "Yoksayılan RPA Arşivleri: " + arhiveFileListSeperated

    @classmethod
    @property
    def ignoredRPAArchivesSeperator(cls):
        return ", " # This is rpa file seperator for ignoredRPAArchives.

    @classmethod
    def logfileEndDescription(cls, filePath: str):
        return "Bu log dosyasını daha sonra \""+filePath+"\" konumunda bulabilirsiniz."

    @classmethod
    @property
    def exrtractingFile(cls, fileName: str):
        return "\""+fileName+"\" arşivi çıkartılıyor..."

    @classmethod
    def exrtractedFileSuccess(cls, fileName: str):
        return "\""+fileName+"\" arşivi başarıyla çıkartıldı!"

    @classmethod
    @property
    def exrtractFileErrorTitle(cls):
        return "Arşiv çıkartılamadı"

    @classmethod
    def exrtractFileError(cls, filePath:str, error:str):
        return "\""+filePath+"\" arşivi çıkartılamadı.\n\nHata: "+error

    @classmethod
    def ignoredFileWarning(cls, fileName: str):
        return "\""+fileName+"\" arşivi yoksayıldı..."

    @classmethod
    @property
    def extractRPASkipped(cls):
        return "RPA arşivlerini çıkarma atlandı."

    @classmethod
    @property
    def decompilingRpyc(cls):
        return "Rpyc dosyaları çıkartılıyor..."
    
    @classmethod
    @property
    def decompilingRpycCompleted(cls):
        return "Rpyc dosyalarını çıkartma başarılı. Geçici dosyalar siliniyor..."
    
    @classmethod
    @property
    def removedTmpFiles(cls):
        return "Geçici dosyalar başarıyla silindi!"
    
    @classmethod
    @property
    def decompileRpycErrorTitle(cls):
        return "Çıkartılamıyor"

    @classmethod
    def decompileRpycError(cls, error:str):
        return "Rpyc dosyaları çıkartılamıyor.\n\nHata: "+error
    

    @classmethod
    @property
    def decompilingRpycSkipped(cls):
        return "Rpyc dosyalarını çıkartma atlandı."

    @classmethod
    @property
    def translationSkipped(cls):
        return "Çeviri dosyalarını oluşturma atlandı, çünkü çeviri klasörü zaten mevcut ve tekrar oluşturmaya zorla seçeneği devredışı."

    @classmethod
    @property
    def regeneratingTranslation(cls):
        return "Çeviri dosyaları tekrar oluşturuluyor..."

    @classmethod
    @property
    def generatingTranslation(cls):
        return "Çeviri dosyaları oluşturuluyor..."

    @classmethod
    @property
    def generatedTranslation(cls):
        return "Çeviri dosyaları başarıyla oluşturuldu."

    @classmethod
    @property
    def generatingTranslationErrorLog(cls):
        return "Çeviri dosyaları oluşturulamadı.\n\nYukarıdaki hataları kontrol edin." # Shows on log file

    @classmethod
    @property
    def generatingTranslationErrorMSGTitle(cls):
        return "Could not create translation"

    @classmethod
    @property
    def generatingTranslationErrorMSG(cls):
        return "Çeviri dosyaları oluşturulamadı.\n\nLog dosyasındaki hataları kontrol edin." # Shows on messagebox
    
    @classmethod
    def translating(cls, filePath: str):
        return "\""+filePath+"\" dosyası çevriliyor..."

    @classmethod
    def translatingSkipped(cls, filePath: str):
        return "\""+filePath+"\ dosyasının çevirisi atlandı skipped. Dosya zaten çevrilmiş!"
    
    @classmethod
    @property
    def connectingGoogleTrans(cls):
        return "Google translate ile bağlantı kuruluyor. Dosyadaki diyalogların uzunluğu ve sayısına göre bu işlem uzun sürebilir..."

    @classmethod
    @property
    def stringsTranslated(cls):
        return "Yazılar başarıyla çevrildi!"

    @classmethod
    def translatingFileSuccess(cls, filePath: str):
        return "\""+filePath+"\" dosyasının çevirisi başarılı!" 

    @classmethod
    @property
    def translatingSuccess(cls):
        return "Çeviri başarılı! Lütfen oyunda bir hata olup olmadığını kontrol etmek için oyunu başlatın."

    @classmethod
    def translationFolderNotFound(cls, folderPath: str):
        return "\""+folderPath+"\" isminde bir çeviri klasörü bulunamadı!"
    
    @classmethod
    @property
    def translationFailedTitle(cls):
        return "Çeviri Başarısız"
    
    @classmethod
    def translationFailed(cls, error:str):
        return "Çeviri başarısız!\n\nHata: "+error
    
    @classmethod
    def lockingTranslation(cls, languageName: str, languageFolderName: str):
        return "Dil kilitleniyor: "+languageName+" ("+languageFolderName+")..."
    
    @classmethod
    @property
    def lookingExistedLockFile(cls):
        return "Var olan kilit dosyası aranıyor."
    
    @classmethod
    def lockFileFoundLoc(cls, filePath: str):
        return "Kilit dosyası \""+filePath+"\" içerisinde bulundu ve silindi.\nYeni bir tane oluşturuluyor..."
    
    @classmethod
    @property
    def lockFileNotFound(cls):
        return "Kilit dosyası bulunmadı, bir tane oluşturuluyor..."
    
    @classmethod
    def lockFileCreated(cls, languageName: str, languageFolderName: str, lockFileName:str):
        return "Dil, şu dile kilitlendi: "+languageName+" ("+languageFolderName+"). Kilidi açmak için sadece \""+lockFileName+"\" dosyasını silmeniz yeterli."
    
    @classmethod
    @property
    def lockFileFailedTitle(cls):
        return "Kilit Dosyası Oluşturulamadı"
    
    @classmethod
    def lockFileFailed(cls, error: str):
        return "Dil kilit dosyası oluşturulamadı.\n\nHata: "+error

    @classmethod
    @property
    def languageSettingsDesc(cls):
        return "\nBu kodu screens.rpy dosyasında \"screen preferences():\" içerine düzgün bir şekilde ekleyin . English kısmını oyunun orjinal dili ile (ingilizce değilse) değiştirin."

    @classmethod
    @property
    def translationCancelledByUser(cls):
        return "Çeviri kullanıcı tarafından iptal edildi!"

    @classmethod
    @property
    def translationCompletedTitle(cls):
        return "Çeviri tamamlandı"

    @classmethod
    @property
    def translationCompleted(cls):
        return "Çeviri başarıyla tamamlandı!"

    @classmethod
    @property
    def googleTransCanNotBeEmpty(cls):
        return "Google çeviri dili boş olamaz."

    @classmethod
    @property
    def languageNameInvalid(cls):
        return "Dil adı boş olamaz."

    @classmethod
    @property
    def languageFolderNameInvalid(cls):
        return "Dil klasör adı en az 3 karakter olmadı ve sadece küçük ingilizce karakterler içermelidir."

    @classmethod
    @property
    def cancellingTranslation(cls):
        return "Çeviri iptal ediliyor. Arkaplan servislerine göre bu işlem uzun sürebilir..."

    @classmethod
    def zipStarted(cls, arhivePath: str):
        return "\""+arhivePath+"\" içerisine bir zip arşivi oluşturma başladı..."

    @classmethod
    def addedFileToArchive(cls, filePath: str):
        return "\""+filePath+"\" dosyası arşive eklendi."

    @classmethod
    @property
    def createdArhiveSuccess(cls):
        return "Arşiv başarıyla oluşturuldu!"

    @classmethod
    @property
    def creatingArhiveErrorTitle(cls):
        return "Arşiv Oluşturulamadı"

    @classmethod
    def creatingArhiveError(cls, error: str):
        return "Arşiv dosyası oluşturulamadı!\n\nHata: "+error