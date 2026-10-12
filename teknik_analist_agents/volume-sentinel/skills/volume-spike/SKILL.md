# Skill: Volume Spike Detection

## Ne Yapar
Anormal hacim artışlarını tespit eder ve fiyat hareketiyle ilişkisini analiz eder.
"Sessiz birikim" (yüksek hacim + küçük fiyat hareketi) en güçlü sinyaldir.

## Adımlar
1. Son 20 günlük ortalama hacmi hesapla
2. Bugünkü hacim / ortalama = hacim oranı
   - ≥ 2x → Spike tespit edildi
   - ≥ 3x → Güçlü spike (kurumsal aktivite şüphesi)
3. Fiyat-hacim ilişkisini değerlendir:
   - Yüksek hacim + küçük fiyat değişimi → **Sessiz birikim/dağıtım** (en önemli)
   - Yüksek hacim + büyük fiyat artışı → Kırılım / climax
   - Yüksek hacim + büyük fiyat düşüşü → Panik satış (dip olabilir)
4. `calculate_obv` ile spike'ın birikiim mi dağıtım mı olduğunu belirle

## Çıktı
```
VOLUME_RATIO: 2.8x
PRICE_CHANGE: +0.4%
PATTERN: SILENT_ACCUMULATION | BREAKOUT | CLIMAX | PANIC_SELL
OBV_DIRECTION: RISING
INTERPRETATION: Kurumsal sessiz alım şüphesi
```
