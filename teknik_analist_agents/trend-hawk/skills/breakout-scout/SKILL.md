# Skill: Breakout Scout

## Ne Yapar
Konsolidasyon sonrası kırılımları (breakout) tespit eder.
Bollinger Band sıkışması + hacim patlaması kombinasyonuna bakar.

## Ne Zaman Tetiklenir
- EMA Crossover sinyali geldiğinde ek doğrulama için
- Bollinger bandwidth < 5 olduğunda (sıkışma algılandı)

## Adımlar
1. `calculate_bollinger_bands` çalıştır
   - bandwidth < 5 → sıkışma var, kırılım yaklaşıyor
   - percent_b > 1.0 → üst band kırıldı (bullish breakout)
   - percent_b < 0.0 → alt band kırıldı (bearish breakout)
2. Kırılım yönü EMA trend yönüyle uyumlu mu kontrol et
3. `calculate_obv` ile hacim breakout'u teyit et
   - OBV yeni zirve yapıyorsa kırılım gerçektir

## Yanlış Kırılım Filtresi
- Kapanış değil, mum içi dokunuş → Güvenilmez, bekle
- Hacim artışı yoksa → Whipsaw riski yüksek, giriş yapma
- İlk kapanış band dışında değilse → Bekle

## Çıktı
```
BREAKOUT: BULLISH | BEARISH | SQUEEZE_DETECTED | NO_BREAKOUT
BANDWIDTH: 3.2 (SQUEEZE)
VOLUME_CONFIRMED: YES | NO
QUALITY: HIGH | MEDIUM | LOW
```
