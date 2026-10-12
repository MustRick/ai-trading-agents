# Skill: Reversion Entry

## Ne Yapar
Aşırı bölge + divergence doğrulandıktan sonra en uygun giriş noktasını belirler.
Bollinger Band orta bandını hedef, alt/üst bandı stop referansı olarak kullanır.

## Ne Zaman Tetiklenir
- Divergence Detector → SIGNAL_STRENGTH: STRONG veya MODERATE sonrasında

## Adımlar
1. `calculate_bollinger_bands` çalıştır
   - Giriş bölgesi: percent_b < 0.10 (alt band yakını) veya > 0.90 (üst band yakını)
   - Hedef: middle band (SMA 20)
2. Giriş zamanlaması:
   - Oversold long: İlk yeşil kapanış mumu + RSI > 30'a dönüş
   - Overbought short: İlk kırmızı kapanış mumu + RSI < 70'e dönüş
3. Risk/Ödül hesabı:
   - Stop: Bollinger alt/üst band'ın %1 ötesi
   - Hedef: Middle band
   - R:R minimum 2:1 olmalı

## Çıktı
```
ENTRY_ZONE: 139.8 - 140.5
TARGET: 145.2 (middle band)
STOP: 138.3 (alt band - %1)
RISK_REWARD: 2.8:1
ENTRY_TRIGGER: First green close + RSI > 30
ACTION: READY_TO_ENTER | WAIT_FOR_TRIGGER | SKIP_RR_TOO_LOW
```
