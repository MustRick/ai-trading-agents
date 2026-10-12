# Heartbeat — Reversal Phantom

## Zamanlama
| Tetikleyici | Eylem |
|-------------|-------|
| Günlük kapanış | Extremes Scanner — tüm watchlist |
| RSI < 35 veya > 65 | Detaylı analiz başlat (divergence + bollinger) |
| Açık pozisyon varsa | Bollinger middle band'e ulaşıldı mı kontrol et |
| Haftalık | Tamamlanan işlemleri değerlendir, başarı oranını güncelle |

## Günlük Akış
1. `extremes-scanner` ile aşırı bölgede sembol var mı?
2. Varsa `divergence-detector` çalıştır
3. Divergence güçlüyse `reversion-entry` + `risk-sizing`
4. Açık pozisyonlar: Middle band'e ulaşıldıysa çıkış değerlendir

## Bekleme Koşulları
- Güçlü trendde (ADX > 30) mean-reversion denenemez
- Kazanma oranı son 10 işlemde < %40 ise strateji parametrelerini gözden geçir
