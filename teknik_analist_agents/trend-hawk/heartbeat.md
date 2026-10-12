# Heartbeat — Trend Hawk

## Zamanlama
| Tetikleyici | Eylem |
|-------------|-------|
| Günlük kapanış (17:35 BIST) | Tüm açık pozisyonlar için SAR güncelle |
| Günlük kapanış | Watchlist'teki semboller için EMA crossover tara |
| Haftalık (Pazartesi 09:30) | Yeni trend adaylarını taramak için Trend Detection çalıştır |
| ADX 20-25 bandına girişte | Trend başlıyor mu? — yakın takip |

## Günlük Akış
1. Açık pozisyonlar: `position-management` skill çalıştır
2. Watchlist: `trend-detection` → `ema-crossover` pipeline
3. Yeni sinyal varsa: `breakout-scout` ile doğrula
4. Raporu `reports/YYYY-MM-DD.md` olarak kaydet

## Bekleme Koşulları
- Tüm watchlist ADX < 20 → Hiçbir şey yapma, bekle
- Piyasa genel endeksi sert düşüşte (-2%+) → Yeni giriş yapma
