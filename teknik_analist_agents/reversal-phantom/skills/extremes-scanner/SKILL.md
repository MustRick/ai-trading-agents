# Skill: Extremes Scanner

## Ne Yapar
RSI, Williams %R ve CCI'yi eş zamanlı okuyarak aşırı alım/satım bölgelerini tespit eder.
Tek gösterge yeterli değildir; minimum 2'den teyit alınır.

## Ne Zaman Tetiklenir
- Watchlist'teki tüm semboller için günlük tarama
- RSI < 35 veya > 65 olduğunda detaylı analiz başlatılır

## Adımlar
1. `calculate_rsi` çalıştır (period: 14)
2. `calculate_williams_r` çalıştır (period: 14)
3. `calculate_cci` çalıştır (period: 20)
4. Puanlama:

| Gösterge | Oversold Koşul | Puan |
|----------|----------------|------|
| RSI < 30 | ✓ | +2 |
| RSI 30-35 | ✓ | +1 |
| Williams %R < -80 | ✓ | +1 |
| CCI < -100 | ✓ | +1 |

**Minimum 3 puan → Divergence Scanner'a geç**

## Çıktı
```
RSI: 28.4 (OVERSOLD)
WILLIAMS_R: -85.2 (OVERSOLD)
CCI: -112.3 (OVERSOLD)
EXTREME_SCORE: 4/4
PROCEED_TO: divergence-detector
```
