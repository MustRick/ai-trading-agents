# Skill: Teknik Görünüm Özet Kartı

## Amaç
Bir hisse için tüm teknik indikatörleri tek seferde çalıştır ve "yeşil/sarı/kırmızı" özet kart üret. Diğer skill'lerin girişi.

## Adımlar
1. Son 200 günlük OHLCV verisini çek
2. Şu indikatörleri hesapla (ilgili skill'leri çağır):
   - Trend: EMA20/50/200 pozisyonu
   - Momentum: RSI(14), MACD(12,26,9)
   - Volatilite: Bollinger %B, ATR(14)
   - Göreli güç: hisse / BIST100 son 20 gün

## Çıktı Formatı
```
─────────────────────────────────────────
TEKNIK GÖRÜNÜM: XXXXX  |  {tarih}
─────────────────────────────────────────
Fiyat    : X.XX TL  (52H: X.XX – X.XX)
Hacim    : XMTL  (20G Ort: XMTL)
─────────────────────────────────────────
TREND      │ ● YÜKSELİŞ  / ◐ YATAY / ○ DÜŞÜŞ
MOMENTUM   │ ● GÜÇLܠ   / ◐ NÖTR  / ○ ZAYIF
VOLATİLİTE │ ● DÜŞÜK    / ◐ NORMAL / ○ YÜKSEK
GÖRELI GÜÇ │ ● GÜÇLÜ    / ◐ NÖTR  / ○ ZAYIF
─────────────────────────────────────────
GENEL      │ ● AL ZEMİNİ / ◐ BEKLE / ○ SAT ZEMİNİ
─────────────────────────────────────────
Kritik seviyeler:
  Destek  : X.XX / X.XX
  Direnç  : X.XX / X.XX
─────────────────────────────────────────
```

## Genel Sinyal Mantığı
- **● AL ZEMİNİ**: 3/4 veya 4/4 indikatör pozitif
- **◐ BEKLE**: 2/4 pozitif veya çelişen sinyaller
- **○ SAT ZEMİNİ**: 3/4 veya 4/4 indikatör negatif

## Uyarı
"Al zemini" alım tavsiyesi değil — elverişli teknik koşul demektir.
