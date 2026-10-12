# Skill: Zone Entry Scanner

## Ne Yapar
Güncel S/R bölgelerini hesaplar ve fiyatın hangi bölgeye yakın olduğunu tespit eder.
Yakınlık (proximity) eşiği içindeki bölgeleri "aktif bölge" olarak işaretler.

## Adımlar

### 1. S/R Bölgelerini Hesapla
```
calculate_sr_zones(
  highs, lows, closes,
  prd=10,
  channel_width_pct=10,
  maxnumsr=5,
  min_strength=2        ← zayıf bölgeleri ele
)
```

### 2. Proximity Kontrolü
Her bölge için:
```
distance_pct = (zone.mid - current_price) / current_price × 100

Aktif bölge koşulu:
  |distance_pct| ≤ 1.5%
```

### 3. Bölge Kırılımı Kontrolü
```
check_sr_level_break(highs, lows, closes)
```
- `signal = SUPPORT_BROKEN` → o destek bölgesi geçersiz, atla
- `signal = RESISTANCE_BROKEN` → o direnç bölgesi geçersiz, atla

### 4. Aktif Bölge Sınıflandırması
| Durum | Aksiyon |
|-------|---------|
| Destek bölgesine yakın + kırılmamış | → rsi-confirmation'a geç (LONG yön) |
| Direnç bölgesine yakın + kırılmamış | → rsi-confirmation'a geç (SHORT yön) |
| Bölge kırıldı | → BU BÖLGE İPTAL, diğerlerine bak |
| Hiç aktif bölge yok | → WAIT, tarama bitti |

## Çıktı
```
ACTIVE_ZONES:
  - type: SUPPORT   mid: 142.30  strength: 4  distance: -0.8%  status: VALID
  - type: RESISTANCE mid: 148.90  strength: 3  distance: +2.1%  status: OUT_OF_RANGE

NEAREST_VALID_SUPPORT:    142.30 (-0.8%)
NEAREST_VALID_RESISTANCE: ---
SCAN_RESULT: SUPPORT_PROXIMITY_DETECTED
PROCEED_TO: rsi-confirmation (yön: LONG)
```
