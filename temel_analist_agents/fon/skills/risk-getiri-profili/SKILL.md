# Skill: Risk-Getiri Profili

## Amaç
Fonun risk-ayarlı getirisini ölç. Ham getiri yüksek ama risk de yüksekse "iyi" fon değildir.

## Metrikler

### Sharpe Oranı
```
Sharpe = (Fon Getirisi − Risksiz Faiz) / Fon Volatilitesi
```
- > 1.0: İyi risk-getiri dengesi
- > 2.0: Mükemmel
- < 0.5: Kötü — risk almaya değmez

### Sortino Oranı
```
Sortino = (Fon Getirisi − Risksiz Faiz) / Aşağı Yönlü Volatilite
```
Sharpe'tan daha adil — yalnızca negatif volatiliteyi cezalandırır.

### Maximum Drawdown
- En yüksek zirveden en derin dibe düşüş yüzdesi
- "Bu fonda kalmak için ne kadar sinir gerekir?"

### Calmar Oranı
```
Calmar = Yıllık Getiri / |Maximum Drawdown|
```
- > 1.0: Drawdown riski iyi telafi ediliyor

### VaR (Tarihsel, %95, 1 Ay)
- "Kötü senaryoda 1 ayda en fazla ne kadar kaybedebilirim?"

## Risksiz Faiz
Güncel TCMB politika faizi veya Hazine 3 aylık bono faizi kullan.

## Adımlar
1. Son 252 günlük fon birim fiyatı çek
2. `scripts/risk_getiri.py` ile tüm metrikleri hesapla
3. Aynı kategorideki fonlarla karşılaştır

## Çıktı
```
Risk-Getiri Profili: {FON_ADI}
────────────────────────────────────────────
Sharpe Oranı    : X.XX   → İyi / Orta / Kötü
Sortino Oranı   : X.XX
Max Drawdown    : -%XX.X% (tarih)
Calmar Oranı    : X.XX
VaR(95%, 1ay)   : -%X.X%
Volatilite (yıl): %XX.X
────────────────────────────────────────────
Özet: Bu fon risk başına {iyi/orta/kötü} getiri üretiyor.
Kategori ortalaması Sharpe: X.XX ({sıralama}/X)
```
