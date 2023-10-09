[English](README.md) | Türkçe

# game-translator

# İçerikler

- [Çevirmenler İçin](#çevirmenler-i̇çin)
  - [Desteklenen Oyunlar](#desteklenen-oyunlar)
    - [Renpy](#renpy)
- [Geliştiriciler İçin](#geliştiriciler-i̇çin)
  - [Araca Kendi Dilinizi Ekleme](#araca-kendi-dilinizi-ekleme)
  - [Derlemek](#derlemek)


# Çevirmenler İçin

- **Bu araç hala geliştirme aşamasındadır ve oyununuzu bozabilir. O yüzden oyunu yedeklemeyi unutmayın!**

## Desteklenen Oyunlar

### Renpy:

- Neler Yapabilir?
  - RPA arşivlerini çıkarma (İstediğiniz RPA arşivlerini yoksayabilirsiniz.).
  - RPYC dosyalarını decompile etme.
  - Yazıları çeviri için optimize etme.
    - Örneğin (Ren'Py'nin çeviri politikası):
      - Çevrilebilir değil: `textbutton "Confirm"`
      - Çevrilebilir: `textbutton _("Confirm")`
  - Çeviri dosyaları oluşturma (Tabiki bu aracın amacı bu, ve sadece çeviri dosyaları mevcut değilse oluşturur. Bunun için bir seçenek mevcut değil.)
    - Bu araç çeviri dosyaları mevcut değilse, "game/tl/" içinde bu çevirileri oluşturur.
    - Eksik çevirileri eklemek için "Çeviri dosyalarını yeniden oluşturmaya zorla" seçeneği etkinleştirilmelidir.
    - Alternatif olarak, temiz bir çeviri oluşturmak için "game/tl" klasörü içindeki çeviri klasörünü silmeniz yeterlidir.
  - Google çeviri ile otomatik çeviri.
    - Bu seçenek çeviri için vaktiniz yoksa yardımcı olabilir.
    - Diyalogların ve yazıların uzunluğuna göre, bu işlem zaman alabilir. Sadece arkanıza yaslanın, kendi işlerinizi halledin ve işlemin bitmesini bekleyin.
  - İşlem tamamlandığında veya bir hata oluştuğunda bildirim alacaksınız.
- Neler yapamaz?
  - Grafikleri (resimler, videolar, vb.) çeviremez.
  - Şimdilik, değişken ile atanmış yazıları çeviremez.
    - Örneğin:
    - `$ walkthrough = "Go home and sleep"`
  - Ve yukarıda bahsedilmeyen ve aklınıza gelen diğer şeyleyi yapamaz. :)

- Dış araçlar
  - Bu araçta UnRen-1.0.11d aracının düzenlenmiş bir versiyonu kullanılmaktadır


# Geliştiriciler İçin

## Araca Kendi Dilinizi Ekleme

- {proje-yolu}/locales/en.json dosyasının bir kopyasını oluşturun.
- Oluşturduğunuz kopyada "localeCode" ve "localeName" kısımlarının dilinize göre düzenleyin.
- Araç bu dil dosyasını {proje-yolu}/locales/ klasörü içerisinde bulunduğu ve ".json" uzantısı bulunduğu sürece otomatik olarak algılayacaktır.
- Dil dosyasını derlenmiş araca dahi aynı şekilde ekleyebilirsiniz.

## Derlemek

- Gereksinimleri kurma

```
pip install -r requirements.txt
```

- Derlemek (Derlenen dosyalar "{proje-yolu}/build" klasöründe oluşturulur.)

```
python setup.py build
```