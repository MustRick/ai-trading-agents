# Skill: Fon Getiri Analizi

## Amaç
Yatırım fonlarının mutlak ve karşılaştırmalı getiri performansını ölç. "Bu fon parasını hak ediyor mu?" sorusunu yanıtla.

## Analiz Dönemleri
1 hafta | 1 ay | 3 ay | 6 ay | YBÜ | 1 yıl | 3 yıl | 5 yıl

## Kıyaslama Kriterleri
| Fon Türü | Benchmark |
|----------|-----------|
| Hisse fonu | BIST100 |
| Tahvil fonu | KYD Tüm Tahvil Endeksi |
| Para piyasası | Gecelik Repo Faizi |
| Karma | Ağırlıklı benchmark |
| BYF (ETF) | Takip ettiği endeks |

## Adımlar
1. `finansal_beceri_yukle(["yatirim_fonlari"])` ile şemayı yükle
2. Fon kodu veya adıyla `sembol_arama` ile doğrula
3. Seçilen dönemler için fon ve benchmark getirilerini çek
4. `scripts/getiri_analizi.py` ile risk-ayarlı metrikleri hesapla
5. Yönetim ücreti ve gider oranını dahil et

## Getiri Sıralaması Notu
- **Kategori içi sıralama** → Fon benzerleri arasında kaçıncı?
- **Benchmark farkı (Alpha)** → Endeks fonundan iyi mi, kötü mü?

## Çıktı
```
Getiri Analizi: {FON_ADI} ({KOD})
Kategori: {kategori}  |  PYŞ: {sirket}  |  Büyüklük: X TL mn
────────────────────────────────────────────────────────
Dönem    Fon      Benchmark  Fark     Kategori Sırası
1 Ay    +X.X%    +X.X%     +X.X%    X/XXX
3 Ay    +X.X%    +X.X%     +X.X%    X/XXX
YBÜ     +X.X%    +X.X%     +X.X%    X/XXX
1 Yıl   +X.X%    +X.X%     +X.X%    X/XXX
────────────────────────────────────────────────────────
Yönetim Ücreti: %X.XX/yıl
Gider Oranı   : %X.XX/yıl
Değerlendirme : Benchmark{i geçmiş / geçememiş}
```
