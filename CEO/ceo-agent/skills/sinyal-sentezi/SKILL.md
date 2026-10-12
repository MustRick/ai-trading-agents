# Skill: Sinyal Sentezi

## Amaç

Dört departmandan gelen özetleri birleştirip "sinyaller birlikte ne anlatıyor?" sorusunu yanıtlar. Çıktı: kompozit skor + kısa tez cümlesi.

## Tetikleyici

- 09:30 heartbeat
- Rick yeni bir sembol için tüm departman özetleri tamamlandığında

## Süreç

1. `inbox/` altındaki dört klasörde ilgili sembolün özetlerini oku.
2. Her özetin sonundaki **sinyal** satırını çek: `AL / SAT / NÖTR / VETOˋ
3. `scripts/kompozit_skor.py` çalıştır → ağırlıklı skoru al.
4. Risk-Portföy VETO içeriyorsa skoru hesaplama; direkt `VETO` döndür.
5. Çelişki varsa (örn. Temel=AL, Teknik=SAT) → `celiski-yonetimi` skilini tetikle.
6. Sentez bloğu yaz:

```
SEMBOL    : <sembol>
TARİH     : <tarih>
SKOR      : <0–100>
KARAR     : Güçlü Al / Koşullu Al / İzle / Geç / VETO
TEZ       : <max 2 cümle>
ZAYIF HALKA : <en düşük puanlı departman ve nedeni>
```

## Kural

- Tek departmandan gelen veriyle sentez yapılmaz.
- Çelişkili sinyal varsa karar `İzle` veya altına düşer; çelişki çözülmeden `Güçlü Al` çıkmaz.
