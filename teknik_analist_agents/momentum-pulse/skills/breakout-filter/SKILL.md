# Skill: Breakout Filter

## Ne Yapar
Sahte kırılımları (fakeout) gerçek kırılımlardan ayırır.
Bollinger sıkışması + MACD momentum birleşimi en güvenilir kırılım yapısıdır.

## Adımlar
1. `calculate_bollinger_bands` çalıştır
   - bandwidth < 5 → sıkışma var, kırılım bekleniyor
   - percent_b > 1.0 → üst band kırıldı
2. MACD sinyali ile yön uyumlu mu?
   - Yukarı kırılım + MACD bullish → **Gerçek kırılım**
   - Yukarı kırılım + MACD bearish → **Fakeout şüphesi**
3. `calculate_roc` ile ivme ölç
   - ROC > 2 → ivme kırılımı destekliyor

## Fakeout Kriterleri (bunlar varsa giriş yapma)
- Hacim artışı yok
- MACD zıt yönde
- Kapanış değil mum içi bant kırılımı
- Bir önceki gün büyük yukarı gapı varsa

## Çıktı
```
BOLLINGER_SIGNAL: UPPER_TOUCH
BANDWIDTH: 4.1 (SQUEEZE)
MACD_ALIGNMENT: YES
ROC_SUPPORT: YES (3.1%)
BREAKOUT_VALID: TRUE | FALSE
FAKEOUT_RISK: LOW | MEDIUM | HIGH
```
