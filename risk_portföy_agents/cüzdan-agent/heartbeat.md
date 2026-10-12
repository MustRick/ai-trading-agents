# Heartbeat — Cüzdan Agent

## Zamanlama
| Tetikleyici | Eylem |
|-------------|-------|
| Piyasa açılışı (09:30) | Günlük limit sıfırla, drawdown kontrolü |
| Her yeni sinyal geldiğinde | 7 adımlı karar akışını çalıştır |
| Her kapanış (17:35) | Trailing stop güncelle, günlük özet raporu |
| Haftalık (Cuma 18:00) | Drawdown kontrolü, VaR hesapla, kuralları gözden geçir |
| Ardışık 3 kayıp | Mola protokolü — 1 gün yeni işlem yok |

## Sabah Açılış Rutini
1. `check_daily_loss_limit` → günlük bütçe sıfır, bugün ne kadar riske girebiliriz?
2. `check_portfolio_heat` → gece sonrası açık pozisyonlar, ısı durumu nedir?
3. `calculate_max_drawdown` → dünden bu yana portföy durumu
4. Duruma göre günün risk modunu belirle (NORMAL / CAUTIOUS / DEFENSIVE)

## Kapanış Rutini
1. Tüm açık pozisyonlar için `update_trailing_stop`
2. Bugün kaybedilen toplam hesapla → günlük limit kullanımı güncelle
3. `reports/YYYY-MM-DD.md` oluştur
4. memory.md güncelle: equity_curve, pozisyon tablosu

## Acil Protokol
- Stop tetiklendiğinde: anında `check_daily_loss_limit` — limit aşıldıysa dur
- Portföy %5+ anlık düşüşte: `check_portfolio_heat` → gerekirse pozisyonları kapat
