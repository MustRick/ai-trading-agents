# Skill: Momentum Scanner

## Ne Yapar
Evrenden en güçlü momentuma sahip sembolleri seçer.
ROC ve MACD histogram şiddetine göre sıralama yapar.

## Ne Zaman Tetiklenir
- Günlük tarama (heartbeat: piyasa açılışından 30 dk sonra)
- Watchlist güncelleme isteğinde

## Adımlar
1. Her sembol için `calculate_roc(period=12)` çalıştır
2. ROC > 3 olanları listele (güçlü momentum adayları)
3. `calculate_macd` çalıştır, histogram değerine bak
   - Histogram pozitif VE yükseliyor → güçlü momentum
4. Sıralama: ROC × MACD_histogram büyüklüğüne göre

## Momentum Skoru
```
Momentum Skoru = ROC × (1 + histogram_artış_hızı)
```

Üst 5 sembol günlük takip listesine alınır.

## Çıktı
```
RANK | SYMBOL | ROC  | MACD_HIST | SCORE
  1  | XYZ    | 5.2% | 0.82      | 4.27
  2  | ABC    | 4.8% | 0.61      | 3.09
  ...
TOP_PICK: XYZ
PROCEED_TO: macd-signal (XYZ için)
```
