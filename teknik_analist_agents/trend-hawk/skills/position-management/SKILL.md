# Skill: Position Management

## Ne Yapar
Açık pozisyon için Parabolic SAR tabanlı dinamik stop seviyesini günceller.
Kâr hedefi ve risk/ödül oranını hesaplar.

## Ne Zaman Tetiklenir
- Her yeni kapanış barında (heartbeat: günlük)
- SAR tersine döndüğünde (acil çıkış)

## Adımlar
1. `calculate_parabolic_sar` çalıştır
   - SAR fiyatın altında → uptrend devam, pozisyonu koru
   - SAR fiyatın üstüne geçti → **EXIT SIGNAL**
2. Mevcut SAR değerini stop seviyesi olarak kaydet (memory.md güncelle)
3. `calculate_adx` ile trend gücü hâlâ > 20 mi kontrol et
   - ADX < 20'ye düştüyse → kâr al, çık

## Risk/Ödül Hesabı
```
Risk     = Giriş Fiyatı - SAR Stop
Reward   = Son SAR Seviyesinden Fiyat Mesafesi
R:R Ratio = Reward / Risk
```
R:R < 1.5 olduğunda pozisyon büyütme önerilmez.

## Çıktı
```
SAR_STOP: 142.30
CURRENT_PRICE: 148.50
UNREALIZED_GAIN: +4.4%
TREND_STRENGTH: ADX 31 (STRONG)
ACTION: HOLD | TIGHTEN_STOP | EXIT
```
