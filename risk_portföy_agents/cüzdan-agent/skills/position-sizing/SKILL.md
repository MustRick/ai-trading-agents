# Skill: Position Sizing

## Ne Yapar
"Bu hisseye kaç TL ayıralım?" sorusunu yanıtlar.
Stop mesafesi ve portföy risk kurallarına göre hem TL miktarı hem adet sayısı üretir.

## Üç Katmanlı Hesaplama
```
Katman 1 — Risk bazlı boyut:  size_fixed_fractional
Katman 2 — Portföy limiti:    check_max_allocation (%10 kuralı)
Katman 3 — Portföy ısısı:     check_portfolio_heat (kalan kapasite)
Final boyut = min(Katman1, Katman2, Katman3 kapasitesi)
```

## Adımlar
1. Stop seviyesini al (stop-loss-manager skill'inden)
2. `size_fixed_fractional(portfolio_value, risk_pct=1, entry_price, stop_price)` çalıştır
   - Agresif mod: risk_pct = 2
   - Standart mod: risk_pct = 1
   - Temkinli mod: risk_pct = 0.5
3. `check_max_allocation` ile %10 portföy limitini kontrol et
4. `check_portfolio_heat` ile mevcut ısı kapasitesi yeterli mi kontrol et
5. Üç katmandan gelen en küçük boyutu kullan

## Boyut Azaltma Koşulları
| Koşul | Azaltma |
|-------|---------|
| Sinyal gücü MODERATE | %50 standart boyut |
| Günlük bütçe %50+ kullanıldı | %50 standart boyut |
| Portföy ısısı %4+ | %50 standart boyut |
| ATR çok yüksek (volatilite HIGH) | Otomatik azalır (volatility_adjusted) |

## Çıktı
```
ENTRY_PRICE: 142.50
STOP_PRICE: 138.20
STOP_DISTANCE: 4.30 (%3.02)
RISK_AMOUNT: 1,000 TL (%1 portföy)
SHARES: 232 adet
POSITION_VALUE: 33,060 TL (%3.3 portföy)
MAX_ALLOCATION_CHECK: PASSED (3.3% < 10%)
HEAT_AFTER_ENTRY: %4.1 (kapasite: %6 → kalan %1.9)
FINAL_DECISION: APPROVED / REDUCE_TO_X / BLOCKED
```
