# Skill: Stop Loss Manager

## Ne Yapar
Her pozisyon için stop loss seviyesini belirler ve açık pozisyonlarda trailing stop'u günceller.
Stop olmadan pozisyon açılmasına izin vermez.

## Stop Seçim Rehberi
| Durum | Önerilen Stop |
|-------|--------------|
| Trend takip işlemi | `stop_chandelier` (3× ATR, 22 gün) |
| Swing trade | `stop_atr` (2× ATR) |
| Hızlı işlem / scalp | `stop_percentage` (%3-5) |
| Destek kırılımı | `stop_support_level` (destek - %0.5) |

## Adımlar — Yeni Pozisyon
1. Strateji türünü belirle (trend / swing / scalp)
2. `stop_atr` çalıştır → ATR bazlı stop öner
3. `stop_chandelier` çalıştır → alternatif daha geniş stop
4. İkisini karşılaştır: teknik analizle hangisi daha mantıklı?
5. `evaluate_risk_reward` ile seçilen stopla R:R hesapla
   - R:R < 1.5 ise stop çok geniş veya hedef çok yakın → işlem iptal

## Adımlar — Açık Pozisyon Güncelleme (Heartbeat)
1. `update_trailing_stop(current_price, current_stop, trail_pct)` çalıştır
2. Stop yukarı taşındıysa → memory.md güncelle
3. Fiyat stop seviyesine ulaştıysa → EXIT SIGNAL üret

## Çıktı
```
STOP_METHOD: ATR | CHANDELIER | PERCENTAGE | SUPPORT
STOP_PRICE: 138.50
DISTANCE: 4.20 (%2.94)
RISK_REWARD_AT_TARGET: 2.4:1
RECOMMENDATION: USE_THIS_STOP | WIDEN_STOP | NARROW_STOP
TRAILING_UPDATE: MOVED_TO 142.10 (+3.60 TL kilitlendi)
```
