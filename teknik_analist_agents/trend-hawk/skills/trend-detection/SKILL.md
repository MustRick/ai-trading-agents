# Skill: Trend Detection

## Ne Yapar
Birden fazla zaman diliminde (1H, 4H, 1D) trendin var olup olmadığını ve yönünü belirler.
ADX + EMA yapısını birlikte okuyarak "gerçek trend mi, gürültü mü?" sorusunu yanıtlar.

## Ne Zaman Tetiklenir
- Yeni bir sembol analiz edilmeye başlandığında (ilk adım her zaman budur)
- ADX değeri 20-25 arasına geldiğinde (trend başlıyor mu kontrolü)
- Pozisyon açmadan önce zorunlu geçiş

## Adımlar
1. `calculate_adx` çalıştır (period: 14)
   - ADX < 20 → STOP, yatay piyasa, bu agent çalışmaz
   - ADX 20-25 → Dikkatli, trend emekleme aşamasında
   - ADX > 25 → Devam et
2. `calculate_ema_crossover` çalıştır (fast: 9, slow: 21)
   - Yön: `plus_di > minus_di` = bullish, tersi = bearish
3. `calculate_sma` ile 50 ve 200 günlük SMA pozisyonunu kontrol et
   - Fiyat > SMA(50) > SMA(200) → Güçlü uptrend yapısı

## Çıktı Formatı
```
TREND_STATUS: BULLISH | BEARISH | NEUTRAL
ADX: 28.4 (STRONG)
DIRECTION: +DI(18.2) > -DI(12.1)
EMA_STRUCTURE: Price > EMA9 > EMA21
RECOMMENDATION: PROCEED_TO_ENTRY | WAIT | NO_TRADE
```
