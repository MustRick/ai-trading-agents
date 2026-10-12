# Skill: Divergence Detector

## Ne Yapar
Fiyat ile RSI arasındaki uyumsuzluğu (divergence) tespit eder.
Divergence = trend yavaşlıyor, dönüş yakın sinyali.

## Divergence Türleri
- **Regular Bullish:** Fiyat yeni dip, RSI daha yüksek dip → Alım sinyali
- **Regular Bearish:** Fiyat yeni zirve, RSI daha düşük zirve → Satım sinyali
- **Hidden Bullish:** Fiyat daha yüksek dip, RSI daha düşük dip → Trend devam (atlat)
- **Hidden Bearish:** Fiyat daha düşük zirve, RSI daha yüksek zirve → Trend devam (atlat)

## Adımlar
1. Son 20 barda fiyat düşük noktalarını listele
2. `calculate_rsi` çalıştır, aynı noktalardaki RSI değerlerini al
3. Son iki dip/zirveyi karşılaştır:
   - Fiyat[n-1] > Fiyat[n] VE RSI[n-1] < RSI[n] → Regular Bullish Divergence
4. Stochastic ile teyit: `calculate_stochastic`
   - Stochastic %K da yükselen dip yapıyorsa divergence güçlüdür

## Çıktı
```
DIVERGENCE_TYPE: REGULAR_BULLISH
PRICE_LOWS: [142.1, 139.8]
RSI_LOWS: [27.3, 29.1]
STOCHASTIC_CONFIRM: YES
SIGNAL_STRENGTH: STRONG | MODERATE | WEAK
PROCEED_TO: reversion-entry
```
