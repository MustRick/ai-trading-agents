# Skill: MACD Signal

## Ne Yapar
MACD crossover'ı detaylı analiz eder: histogram ivmesi, sinyal gücü ve gecikmeli doğrulama.

## Adımlar
1. `calculate_macd(fast=12, slow=26, signal=9)` çalıştır
2. Crossover tipi:
   - `BULLISH_CROSSOVER`: histogram sıfırı yukarı kesti → ana sinyal
   - `BULLISH` + histogram büyüyor → momentum devam ediyor
   - Histogram küçülüyor → momentum zayıflıyor, pozisyon küçült
3. Histogram ivmesi hesapla: `hist[-1] - hist[-2]`
   - Pozitif ve büyüyor → ivme artıyor (**giriş zamanı**)
   - Pozitif ama küçülüyor → ivme azalıyor (**çıkış hazırlığı**)

## Sinyal Kalite Matrisi
| Durum | Aksiyon |
|-------|---------|
| BULLISH_CROSSOVER + hist büyüyor | STRONG BUY |
| BULLISH + hist sabit | HOLD |
| BULLISH + hist küçülüyor | PREPARE_EXIT |
| BEARISH_CROSSOVER | EXIT |

## Çıktı
```
MACD: 1.24
SIGNAL_LINE: 0.87
HISTOGRAM: 0.37 (↑ increasing)
CROSSOVER: BULLISH_CROSSOVER
HISTOGRAM_MOMENTUM: ACCELERATING
SIGNAL_QUALITY: STRONG_BUY
```
