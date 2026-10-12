# Skill: Destek & Direnç Seviyeleri

## Amaç
Fiyatın geçmişte güçlü tepki verdiği kritik seviyeleri tespit et. Olası geri çekilme desteği ve kırılma hedeflerini belirle.

## Yöntemler

### 1. Yatay Seviyeler (Hacim Ağırlıklı)
- Son 52 haftada yüksek hacimle test edilmiş fiyat bölgeleri
- En az 2 kez test edilmiş ve tutulmuş seviyeler geçerli sayılır

### 2. Pivot Noktaları (Haftalık)
```
PP  = (Yüksek + Düşük + Kapanış) / 3
R1  = 2×PP − Düşük
R2  = PP + (Yüksek − Düşük)
S1  = 2×PP − Yüksek
S2  = PP − (Yüksek − Düşük)
```

### 3. Fibonacci Geri Çekilme Seviyeleri
Son major düşüş veya yükseliş hareketinin Fibonacci seviyeleri:
- %23.6 / %38.2 / %50.0 / %61.8 / %78.6

### 4. Hareketli Ortalama Destekleri
- EMA20, EMA50, SMA200 dinamik destek/direnç işlevi görür

## Önem Sıralaması
Seviyenin gücü = kaç farklı yöntemle teyit ediliyor?
- 1 yöntem: Zayıf seviye
- 2 yöntem: Orta seviye
- 3+ yöntem: Güçlü seviye

## Adımlar
1. Son 52 haftalık OHLCV çek
2. Yatay seviyeleri belirle (hacim filtresi uygula)
3. Haftalık pivot hesapla
4. Fibonacci seviyeleri çiz
5. HO desteklerini ekle
6. Tüm seviyeleri önem skoruyla birleştir

## Çıktı
```
Destek & Direnç: XXXXX  ({tarih})  Fiyat: XX.XX TL
─────────────────────────────────────────────────
DİRENÇLER
  XX.XX TL  ★★★  (Yatay + Fib %61.8 + R1 Pivot)
  XX.XX TL  ★★   (52H Yüksek)
  XX.XX TL  ★    (Fib %78.6)

DESTEKLER
  XX.XX TL  ★★★  (EMA50 + Yatay + S1 Pivot)
  XX.XX TL  ★★   (Fib %38.2 + Yatay)
  XX.XX TL  ★    (52H Düşük)
─────────────────────────────────────────────────
Risk/Ödül (en yakın S→R): XX.XX → XX.XX = 1:X.X
```
