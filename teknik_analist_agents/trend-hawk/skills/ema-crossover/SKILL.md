# Skill: EMA Crossover

## Ne Yapar
EMA(9)/EMA(21) ve EMA(21)/EMA(50) çiftlerinde crossover sinyali üretir.
Golden Cross / Death Cross anında alarm oluşturur.

## Ne Zaman Tetiklenir
- Trend Detection → PROCEED_TO_ENTRY sonrasında
- Günlük kapanış kontrolünde (heartbeat)

## Adımlar
1. `calculate_ema_crossover(fast=9, slow=21)` çalıştır
2. Sinyal `GOLDEN_CROSS` ise:
   a. `calculate_adx` ile ADX > 25 doğrula
   b. `calculate_obv` ile hacim trendin yönünde mi kontrol et
   c. Üçü uyumluysa → **ENTRY SIGNAL**
3. Sinyal `DEATH_CROSS` ise → mevcut long pozisyon için **EXIT ALERT**

## Crossover Kalite Puanı
| Koşul | Puan |
|-------|------|
| ADX > 30 | +2 |
| ADX > 25 | +1 |
| OBV yükselen | +1 |
| Fiyat > SMA(50) | +1 |
| Hacim > 1.5x ortalama | +1 |

**Minimum 3 puan olmadan giriş yapılmaz.**

## Çıktı
```
CROSSOVER: GOLDEN_CROSS
QUALITY_SCORE: 4/5
ENTRY_VALID: YES
```
