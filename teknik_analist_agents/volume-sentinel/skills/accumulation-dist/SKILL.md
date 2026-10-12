# Skill: Accumulation / Distribution Analysis

## Ne Yapar
Birkaç haftalık dönemde birikim (accumulation) veya dağıtım (distribution) fazını belirler.
Wyckoff ilkelerine dayanır: fiyat hareketi ve hacim birlikte okunur.

## Accumulation Belirtileri
- Fiyat dar bantlı yatay seyrediyor (düşük volatilite)
- Hacim artıyor ama fiyat çok değişmiyor → birikim
- OBV yükseliyor, fiyat yatay
- CMF sürekli pozitif

## Distribution Belirtileri
- Fiyat zirve civarında geniş bantlı salınım
- Yüksek hacimde fiyat yükselmiyor → dağıtım
- OBV düşüyor, fiyat hâlâ yüksekte
- CMF negatife döndü

## Adımlar
1. `calculate_obv` — son 20 günlük trendine bak
2. `calculate_cmf` — ortalama CMF değeri
3. Fiyat volatilitesini hesapla: (max - min) / ortalama son 20 günde
   - < %5 → düşük volatilite, muhtemelen birikim
4. Wyckoff fazını belirle:
   - Accumulation: OBV ↑, Fiyat → , CMF > 0
   - Distribution: OBV ↓, Fiyat → veya ↑, CMF < 0

## Çıktı
```
WYCKOFF_PHASE: ACCUMULATION | DISTRIBUTION | MARKUP | MARKDOWN | UNCLEAR
OBV_TREND: RISING (+12% 20 günde)
CMF_AVG: +0.11
PRICE_VOLATILITY: 3.2% (LOW)
CONFIDENCE: HIGH | MEDIUM | LOW
ACTION_BIAS: BULLISH_WATCH | BEARISH_WATCH | NEUTRAL
```
