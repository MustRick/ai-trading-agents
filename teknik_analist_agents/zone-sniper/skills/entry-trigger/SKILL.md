# Skill: Entry Trigger

## Ne Yapar
Zone Scanner + RSI Confirmation çıktılarını birleştirerek nihai giriş kararını verir.
Stop loss ve hedef seviyelerini hesaplar, cüzdan-agent'a boyut onayı için gönderir.

## Giriş Koşulları Özeti
```
ALIM SİNYALİ:
  ✓ Fiyat destek bölgesine ≤ %1.5 yakın
  ✓ Bölge kırılmamış (check_sr_level_break = NO_BREAK)
  ✓ RSI ≤ 30
  ✓ RSI dönüş başladı (RSI[-1] > RSI[-2])
  ✓ Sinyal puanı ≥ 3

SATIŞ SİNYALİ:
  ✓ Fiyat direnç bölgesine ≤ %1.5 yakın
  ✓ Bölge kırılmamış
  ✓ RSI ≥ 70
  ✓ RSI dönüş başladı (RSI[-1] < RSI[-2])
  ✓ Sinyal puanı ≥ 3
```

## Stop ve Hedef Hesaplama

### LONG için:
```
Stop  = zone.lo × (1 - 0.005)        ← bölgenin alt sınırının %0.5 altı
Hedef = nearest_resistance.mid        ← en yakın direnç bölgesinin ortası
R:R   = (Hedef - Giriş) / (Giriş - Stop)
```

### SHORT için:
```
Stop  = zone.hi × (1 + 0.005)        ← bölgenin üst sınırının %0.5 üstü
Hedef = nearest_support.mid           ← en yakın destek bölgesinin ortası
R:R   = (Giriş - Hedef) / (Stop - Giriş)
```

## R:R Filtresi
- R:R < 1.5 → sinyal üretme (kötü oran)
- R:R 1.5-2.0 → MODERATE sinyal
- R:R > 2.0 → STRONG sinyal

## Çıktı Formatı
```
SIGNAL: LONG | SHORT | NO_TRADE
ENTRY_PRICE: 142.30 (güncel kapanış)
STOP_PRICE:  140.65 (bölge lo - %0.5)
TARGET:      149.20 (en yakın direnç)
RISK:        1.65 TL (%1.16)
REWARD:      6.90 TL (%4.85)
RISK_REWARD: 4.18:1  → STRONG
SIGNAL_SCORE: 6/7
SIGNAL_QUALITY: STRONG

→ cüzdan-agent'a gönder:
  entry=142.30, stop=140.65, target=149.20
  için pozisyon boyutu hesapla
```

## Özel Durumlar
- **Bölge kırılımı sinyali gelirse**: Açık pozisyon varsa STOP çalıştır
- **RSI 30-40 arasında**: Destek bölgesindeyse POTENTIAL_SETUP olarak işaretle,
  30'a düşene kadar bekle
- **İki bölge arasında (ne destek ne direnç yakın)**: WAIT, nötr bölge
