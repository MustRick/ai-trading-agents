# Skill: Osilatörler (RSI, MACD, Stochastic)

## Amaç
Momentum dönüşlerini, aşırı alım/satım bölgelerini ve trend güçlenme/zayıflama sinyallerini tespit et.

## İndikatörler

### RSI (14)
- **> 70**: Aşırı alım — dönüş ihtimali artar
- **50–70**: Boğa bölgesi — güçlü momentum
- **30–50**: Ayı bölgesi — zayıf momentum
- **< 30**: Aşırı satım — toparlanma ihtimali artar
- **Diverjans**: Fiyat yeni yüksek, RSI yeni yüksek yapmıyor → negatif diverjans (zayıflama sinyali)

### MACD (12, 26, 9)
- **MACD > Sinyal hattı**: Momentum pozitif
- **MACD < Sinyal hattı**: Momentum negatif
- **Sıfır hattı geçişi**: Trend değişim sinyali
- **Histogram büyüyor**: Momentum artıyor
- **Histogram küçülüyor**: Momentum azalıyor

### Stochastic (14, 3, 3)
- **> 80**: Aşırı alım
- **< 20**: Aşırı satım
- **%K, %D kesişimi**: Yön değişim sinyali
- En güçlü sinyal: Aşırı satım bölgesinde %K, %D'yi yukarı kesiyor

## Birleşik Okuma
| RSI | MACD | Stoch | Yorum |
|-----|------|-------|-------|
| 50-70 | MACD>Sinyal | >50 | Güçlü yükseliş |
| <30 | MACD>Sinyal | <20 | Olası dönüş (teyit bekle) |
| >70 | MACD<Sinyal | >80 | Aşırı alım, dikkat |
| <30 | MACD<Sinyal | <20 | Momentum tükeniyor |

## Adımlar
1. Son 60 günlük OHLCV çek
2. `scripts/rsi.py` → RSI değeri ve diverjans kontrolü
3. `scripts/macd.py` → MACD, sinyal hattı, histogram
4. Birleşik yorumu üret

## Çıktı
```
Osilatörler: XXXXX  ({tarih})
────────────────────────────────────────
RSI(14)   : XX.X  → Boğa Bölgesi
  Diverjans: Yok
MACD(12,26): +X.XX | Sinyal: +X.XX | Hist: +X.XX
  Durum   : MACD > Sinyal → Pozitif Momentum
Stochastic: %K=XX.X  %D=XX.X  → Nötr
────────────────────────────────────────
Birleşik  : GÜÇLÜ POZİTİF MOMENTUM
```
