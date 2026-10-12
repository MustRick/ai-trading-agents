# Skill: BES Fonu Analizi

## Amaç
Bireysel Emeklilik Sistemi (BES) fonlarını analiz et. Devlet katkısı ve vergi avantajlarını dahil ederek gerçek getiriyi hesapla.

## BES'e Özgü Faktörler

### Devlet Katkısı
- Katılımcı katkısının **%30'u** devlet tarafından eklenir
- Yıllık limit: Net asgari ücretin yıllık toplamı × %30
- 3 yıl önce sistemden çıkılırsa devlet katkısı iade edilmez

### Vergi Avantajı
- Katkı payları stopajsız brüt gelirden düşülebilir (vergili kişiler için)
- Emeklilikte çekimde %5 stopaj (65 yaş üzeri veya 10 yıl sonra)

### Gerçek Getiri Hesabı
```
Efektif Getiri = (Fon Getirisi × 1.30 Devlet Katkısı Etkisi) + Vergi Avantajı
```

## Analiz Boyutları
1. **Fon kategorisi**: Standart, Büyüme, Dengeli, Emeklilik, Gruplama
2. **Risk grubu**: Devlet katkısı fonları 1-5 risk puanına göre
3. **Vade uyumu**: Emekliliğe kaç yıl kaldığına göre uygun risk seviyesi

## Önerilen Risk Profili (Kılavuz)
| Emekliliğe Kalan | Öneri |
|-------------------|-------|
| > 20 yıl | Agresif — %80 hisse |
| 10-20 yıl | Dengeli — %50 hisse |
| 5-10 yıl | Muhafazakâr — %30 hisse |
| < 5 yıl | Koruyucu — %10 hisse |

## Adımlar
1. `finansal_beceri_yukle(["yatirim_fonlari"])` ile şemayı yükle
2. BES fonlarını filtrele
3. Standart fon metrikleriyle birlikte devlet katkısı etkisini hesapla
4. Kullanıcının emeklilik vadesine göre uygunluk değerlendir

## Çıktı
```
BES Fonu Analizi: {FON_ADI}
────────────────────────────────────────────
Risk Grubu    : {1-5}
Kategori      : {Standart/Büyüme/Dengeli}
1 Yıl Ham Getiri   : %XX.X
Devlet Katkısı Etkisi: +%X.X (ilk yıl için)
Efektif Getiri : %XX.X
Benchmark Farkı: +X.X%
────────────────────────────────────────────
Uygunluk (X yıl kaldıysa): UYGUN / UYGUN DEĞİL
```
