# Skill: Portfolio Heat

## Ne Yapar
Tüm açık pozisyonların "eş zamanlı toplam riski"ni (portföy ısısı) izler.
%6 ısı sınırı: en fazla 3 pozisyon × %2 risk aynı anda açık olabilir.

## Isı Nedir?
Her açık pozisyonun stop'a kadar olan kaybı = o pozisyonun ısısı.
Toplam ısı = tüm pozisyonların kayıpları toplandığında portföye etkisi.

```
Pozisyon Isısı = (Giriş - Stop) × Adet
Portföy Isısı = Σ(tüm pozisyon ısıları) / Portföy Değeri × 100
```

## Adımlar
1. `check_portfolio_heat(portfolio_value, positions, max_heat_pct=6)` çalıştır
2. Duruma göre aksiyon:
   - **NORMAL** (<%4.8): Yeni pozisyon açılabilir
   - **NEAR_LIMIT** (%4.8-6): Sadece küçük pozisyonlar açılabilir
   - **OVERHEATED** (>%6): Yeni pozisyon yasak; mevcut pozisyonu kapat veya boyut küçült

## Isı Azaltma Yolları (OVERHEATED durumunda)
1. Kârdaki pozisyonun bir kısmını kapat (partial profit take)
2. En büyük riskli pozisyonun stop'unu yukarı taşı (riski azalt)
3. Yeni sinyal bekle, mevcut pozisyonlar kapanınca yeni giriş

## Günlük İzleme
Her kapanışta portföy ısısını hesapla:
- Isi_sabah vs. Isi_kapanış → artıyorsa neden? (yeni pozisyon / stop taşımamak)
- Trend dönemlerinde ısı doğal olarak artar → daha sık stop güncellemesi gerekir

## Çıktı
```
HEAT_PCT: 4.2%
MAX_HEAT_PCT: 6.0%
REMAINING_CAPACITY: 1.8%
POSITION_COUNT: 3
STATUS: NORMAL
NEW_POSITION_ALLOWED: YES (1.8% kapasite kaldı)
TOP_RISK: XYZ — 1,200 TL (%1.2 ısı)
TOTAL_UNREALIZED_PNL: +3,450 TL
```
