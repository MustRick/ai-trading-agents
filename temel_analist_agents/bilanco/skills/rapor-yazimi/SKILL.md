# Skill: Rapor Yazımı

## Amaç
Tüm analiz adımlarının çıktısını `templates/rapor.md` şablonuna göre yatırımcı dostu tek bir rapora dönüştür.

## Girdi Kaynakları
| Bölüm | Kaynak Skill |
|-------|-------------|
| Hisse özeti | `hisse-tarama` çıktısı |
| Değerleme | `sektor-goreli-degerleme` çıktısı |
| Bilanço | `bilanco-sagligi` çıktısı |
| Risk | `value-trap-kontrolu` çıktısı |

## Adımlar
1. Dört skill'den gelen yapılandırılmış çıktıları topla
2. `templates/rapor.md` şablonunu aç
3. Her bölümü doldur — veri yoksa "Veri Mevcut Değil" yaz, tahmin yapma
4. "Genel Görüş" bölümünde tüm analizleri 3–5 cümleyle sentezle
5. Dosyayı `reports/YYYYMMDD_XXXXX.md` olarak kaydet

## Dosya Adı Şeması
```
reports/20261012_GARAN.md
         ^^^^^^^^ ^^^^
         tarih    hisse kodu
```

## Kalite Kuralları
- Her sayısal iddia kaynaklanmış olmalı (Fintables, hesaplama scripti)
- "Alın" / "Satın" kelimeleri raporlarda yasak
- Tüm değerler TL cinsindendir; USD varsa belirt
- Rapor tarihi ve analiz dönemi başlıkta gösterilmeli

## Çıktı
Kayıt yolu: `reports/YYYYMMDD_HISSE.md`
