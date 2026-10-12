# Heartbeat — Momentum Pulse

## Zamanlama
| Tetikleyici | Eylem |
|-------------|-------|
| Piyasa açılışı +30dk | Momentum Scanner — günlük top 5 listesi |
| MACD crossover tespiti | Anlık sinyal (öncelikli işlem) |
| Açık pozisyon | Histogram küçülüyor mu? → çıkış izleme |
| Haftalık Cuma | Momentum sıralamasını sıfırla, yeni hafta için hazırla |

## Günlük Akış
1. `momentum-scanner` ile günün en güçlü momentumlu semboller
2. Her aday için: `macd-signal` → `volume-confirmation` → `breakout-filter`
3. Tüm filtreleri geçen semboller için giriş hazırlığı
4. Açık pozisyonlar: histogram ivmesi kontrol et

## Bekleme Koşulları
- ROC < 1 olan semboller → işlem yok
- Volume confirmation REJECT ise → kesinlikle giriş yapma
- Piyasa geneli düşüş momentumundaysa (-ROC > 3) → savunmaya geç
