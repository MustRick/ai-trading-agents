# Skill: Göreli Güç Analizi

## Amaç
Hissenin BIST100 ve/veya sektör endeksine göre performansını ölç. "Endeksten iyi mi, kötü mü?" sorusunu sayısal olarak yanıtla.

## Yöntemler

### 1. Göreli Güç Oranı (Price Ratio)
```
GGO = Hisse fiyatı / BIST100 endeksi
```
- GGO trend artıyorsa: hisse endeksten güçlü
- GGO trend düşüyorsa: hisse endeksten zayıf

### 2. Dönemsel Performans Karşılaştırma
| Dönem | Hisse | BIST100 | Fark | Liderlik |
|-------|-------|---------|------|----------|
| 1 Ay  | ...   | ...     | ...  | ✓ / ✗   |
| 3 Ay  | ...   | ...     | ...  | ✓ / ✗   |
| 6 Ay  | ...   | ...     | ...  | ✓ / ✗   |
| YBÜ   | ...   | ...     | ...  | ✓ / ✗   |

### 3. Beta (52 haftalık)
- **Beta > 1.0**: Endeksten daha volatil, piyasa yukarıdayken daha çok kazanır
- **Beta < 1.0**: Defansif, düşüşlerde daha az kaybeder
- **Beta < 0**: Negatif korelasyon (nadir)

### 4. Alpha (Jensen's Alpha)
- Hissenin beta'dan beklenen üstündeki fazla getirisi
- Pozitif alpha → stok spesifik değer yaratıyor

## Adımlar
1. Hisse ve BIST100 için son 252 günlük kapanış fiyatları çek
2. Dönemsel performans hesapla
3. Beta ve alpha hesapla
4. GGO grafiği için yorumla

## Çıktı
```
Göreli Güç: XXXXX vs BIST100  ({tarih})
─────────────────────────────────────────
Dönem   Hisse    BIST100   Fark    Liderlik
1 Ay    +X.X%   +X.X%    +X.X%     ✓
3 Ay    +X.X%   -X.X%    +X.X%     ✓
6 Ay    -X.X%   +X.X%    -X.X%     ✗
YBÜ     +X.X%   +X.X%    +X.X%     ✓
─────────────────────────────────────────
Beta(52H) : X.XX  → Endeksten X kat volatil
Alpha     : +X.X% → Endüstri fazlası getiri
GGO Trendi: ARTIYOR → Son 20 günde liderlik kazanıyor
─────────────────────────────────────────
Liderlik Skoru: 3/4 dönem → GÜÇLÜ
```
