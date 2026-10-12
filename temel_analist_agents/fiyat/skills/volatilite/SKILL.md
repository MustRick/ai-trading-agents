# Skill: Volatilite Analizi

## Amaç
Hissenin fiyat dalgalanma riskini ölç; Bollinger Bantları ile bant kırılması fırsatlarını, ATR ile gerçek fiyat aralığını tespit et.

## İndikatörler

### Bollinger Bantları (20, 2σ)
- **Üst Bant**: EMA20 + 2 standart sapma
- **Alt Bant**: EMA20 − 2 standart sapma
- **%B**: (Fiyat − Alt Bant) / (Üst Bant − Alt Bant)
  - %B > 1.0 → Üst bandın üzerinde (aşırı gerilim)
  - %B < 0.0 → Alt bandın altında
  - %B = 0.5 → Orta bant

### Bant Sıkışması (Squeeze)
- Bantlar daralıyor → volatilite düşüyor → güçlü kırılma yaklaşıyor
- Squeeze sonrası hacimli kırılma yön sinyali verir

### ATR (14) — Average True Range
- Hissenin günlük ortalama fiyat aralığı
- **ATR / Fiyat (%)**: Normalize volatilite
  - < %1.5: Düşük volatilite
  - %1.5–3.0: Normal
  - > %3.0: Yüksek volatilite / riskli

### Tarihsel Volatilite (20 günlük, yıllıklandırılmış)
- Günlük log getirilerin standart sapması × √252
- Benchmark: BIST100 tarihsel volatilitesi ile karşılaştır

## Adımlar
1. Son 60 günlük OHLCV çek
2. `scripts/bollinger.py` → bantlar, %B, squeeze tespiti
3. ATR hesapla, yüzde normalize et
4. Tarihsel volatilite hesapla

## Çıktı
```
Volatilite Analizi: XXXXX  ({tarih})
────────────────────────────────────────────
Bollinger (20,2σ):
  Üst Bant : XX.XX TL
  Orta Bant: XX.XX TL  (EMA20)
  Alt Bant : XX.XX TL
  %B       : 0.XX → Orta bant üzerinde
  Squeeze  : EVET — kırılma yaklaşıyor

ATR(14)    : X.XX TL  (%X.X) → Normal Volatilite
Tarihsel Vol (20G, yıllık): %XX.X
  BIST100 karş.: Hisse X daha volatil
────────────────────────────────────────────
Risk Notu  : ORTA — stop için ATR x1.5 = XX.XX TL
```
