# Heartbeat — Volume Sentinel

## Zamanlama
| Tetikleyici | Eylem |
|-------------|-------|
| Günlük kapanış | Volume Spike Detection — tüm watchlist |
| Hacim ≥ 2x spike | Anlık Smart Money Flow analizi başlat |
| Haftalık | Accumulation/Distribution fazı güncellemesi |
| Aylık | Wyckoff fazı özeti — hangi semboller hangi fazda |

## Günlük Akış
1. `volume-spike` — bugün anormal hacim var mı?
2. Spike varsa `smart-money` ile kurumsal aktivite mi, perakende panik mi?
3. Haftalık `accumulation-dist` ile döngüsel faz tespiti
4. memory.md'deki takip listesini güncelle

## Bekleme Koşulları
- Hacim verisi olmayan semboller analiz edilemez
- Tatil öncesi / sonrası düşük hacimli seanslarda sinyal üretme
- Sadece volume sinyali varsa, fiyat sinyali yoksa pozisyon açma
