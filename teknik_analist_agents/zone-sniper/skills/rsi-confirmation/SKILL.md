# Skill: RSI Confirmation

## Ne Yapar
Zone Entry Scanner'ın bulduğu aktif bölgeyi RSI ile doğrular.
RSI sadece aşırı bölgede olması yetmez — **geri dönmeye başlaması** gerekir.

## Temel Kural
```
LONG  (destek bölgesi): RSI ≤ 30  →  aşırı satılmış, alım baskısı yakında
SHORT (direnç bölgesi): RSI ≥ 70  →  aşırı alınmış,  satış baskısı yakında
```

## Adımlar

### 1. RSI Hesapla
```
calculate_rsi(closes, period=14)
→ values[-1] = son RSI
→ values[-2] = bir önceki RSI (dönüş teyidi için)
```

### 2. Aşırı Bölge Kontrolü
| Yön   | Koşul         | Puan |
|-------|---------------|------|
| LONG  | RSI ≤ 30      | +2   |
| LONG  | RSI ≤ 25      | +1 bonus |
| SHORT | RSI ≥ 70      | +2   |
| SHORT | RSI ≥ 75      | +1 bonus |

### 3. Dönüş Teyidi (Kritik!)
RSI'ın aşırıdan GERİ DÖNMEYİ başlaması güçlü sinyaldir:
```
LONG  dönüş: RSI[-2] < RSI[-1]  (yani RSI dipten yukarı döndü)
SHORT dönüş: RSI[-2] > RSI[-1]  (yani RSI zirvedan aşağı döndü)
```
Dönüş varsa: **+2 puan**

### 4. Stochastic Ek Doğrulama
```
calculate_stochastic(highs, lows, closes, k_period=14, d_period=3)
```
- LONG: Stoch %K < 20 → +1 puan
- SHORT: Stoch %K > 80 → +1 puan
- Stoch %K ile %D aynı yönde çaprazlanıyorsa → +1 puan

### 5. Bollinger Dokunuşu
```
calculate_bollinger_bands(closes, period=20, std_multiplier=2.0)
```
- LONG: `percent_b ≤ 0.05` (alt band dokunuşu) → +1 puan
- SHORT: `percent_b ≥ 0.95` (üst band dokunuşu) → +1 puan

## Toplam Puan → Karar
| Puan | Karar |
|------|-------|
| ≥ 5  | STRONG_SIGNAL → entry-trigger'a geç |
| 3-4  | MODERATE_SIGNAL → entry-trigger'a geç (küçük boyut) |
| 1-2  | WEAK → BEKLE, henüz değil |
| 0    | NO_SIGNAL → bölge geçerli ama RSI uyumsuz |

## Çıktı
```
DIRECTION: LONG
RSI: 27.4 (OVERSOLD)
RSI_TURNING: YES (26.1 → 27.4, dönüş başladı)
STOCH_K: 18.2 (OVERSOLD)
BOLLINGER_PCT_B: 0.03 (LOWER_TOUCH)
TOTAL_SCORE: 6/7
SIGNAL_QUALITY: STRONG_SIGNAL
PROCEED_TO: entry-trigger
```
