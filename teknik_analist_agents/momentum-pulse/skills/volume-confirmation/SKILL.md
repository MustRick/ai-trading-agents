# Skill: Volume Confirmation

## Ne Yapar
Momentum sinyalini hacim verisiyle doğrular.
Hacim yoksa kırılım sahte; bu skill olmadan giriş yapılmaz.

## Kural
> "Momentum + Hacim = Gerçek hareket. Momentum - Hacim = Whipsaw"

## Adımlar
1. `calculate_obv` çalıştır
   - OBV yeni zirve yapıyor mu? → Güçlü teyit
2. `calculate_mfi` çalıştır
   - MFI 50-70 arası → Para giriyor, henüz doygunluk yok → **Giriş için ideal**
   - MFI > 80 → Doygunluk riski, dikkatli ol
3. Son 5 barda ortalama hacim hesapla
   - Sinyal günü hacim ≥ 1.5x ortalama → Hacim spike ✓

## Hacim Skoru
| Koşul | Puan |
|-------|------|
| OBV yeni zirve | +2 |
| MFI 50-70 | +2 |
| Hacim ≥ 1.5x | +2 |
| Hacim ≥ 2.0x | +1 bonus |

**Minimum 4 puan olmadan giriş yapılmaz.**

## Çıktı
```
OBV_NEW_HIGH: YES
MFI: 62.3 (IDEAL ZONE)
VOLUME_RATIO: 1.8x
VOLUME_SCORE: 6/6
CONFIRMATION: STRONG | MODERATE | WEAK | REJECT
```
