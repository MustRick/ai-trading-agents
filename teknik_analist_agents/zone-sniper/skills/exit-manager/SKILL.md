# Skill: Exit Manager

## Ne Yapar
Açık pozisyonlar için çıkış koşullarını izler.
Üç çıkış türü: Hedef ulaşıldı / Stop tetiklendi / Erken çıkış sinyali.

## Çıkış Türleri

### 1. Hedef Ulaşıldı (Kâr Al)
```
LONG : close ≥ target_price → EXIT (kâr al)
SHORT: close ≤ target_price → EXIT (kâr al)
```
Kısmi çıkış seçeneği: Hedefin %50'sinde pozisyonun yarısını kapat, geri kalanı sür.

### 2. Stop Tetiklendi (Zarar Kes)
```
LONG : close ≤ stop_price → EXIT (zarar kes)
SHORT: close ≥ stop_price → EXIT (zarar kes)
```

### 3. Erken Çıkış Sinyalleri (Bölge Kırıldı)
```
check_sr_level_break çalıştır:
  LONG pozisyon + SUPPORT_BROKEN  → Hemen çık (destek kırıldı)
  SHORT pozisyon + RESISTANCE_BROKEN → Hemen çık (direnç kırıldı)
```

### 4. RSI Dönüş Çıkışı (Momentum Bitti)
```
LONG  pozisyon: RSI > 65 → Momentum bitti, kâr al (hedefe ulaşmasa bile)
SHORT pozisyon: RSI < 35 → Momentum bitti, kâr al
```
Bu erken çıkış hedefe ulaşılmasa bile pozisyonu korur.

## Günlük İzleme Akışı
```
1. calculate_rsi(closes)          → RSI hâlâ aşırıdan mı dönüyor?
2. check_sr_level_break(...)      → Bölge kırıldı mı?
3. Fiyat hedef/stop'a ulaştı mı? → Karşılaştır
4. Aksiyon belirle
```

## Çıkış Kararı Matrisi
| Durum | LONG Aksiyonu | SHORT Aksiyonu |
|-------|--------------|----------------|
| Hedef kırıldı | TAKE_PROFIT | TAKE_PROFIT |
| Stop kırıldı | CUT_LOSS | CUT_LOSS |
| Destek kırıldı | EXIT_NOW | — |
| Direnç kırıldı | — | EXIT_NOW |
| RSI > 65 (longta) | EARLY_EXIT | — |
| RSI < 35 (shortta) | — | EARLY_EXIT |
| Hiçbiri | HOLD | HOLD |

## Çıktı
```
POSITION: LONG @ 142.30
CURRENT_PRICE: 147.80
STOP: 140.65
TARGET: 149.20
UNREALIZED_PNL: +5.50 TL (+3.87%)
RSI_CURRENT: 58.4

EXIT_CHECK:
  Stop tetiklendi: NO (147.80 > 140.65)
  Hedef ulaşıldı: NO (147.80 < 149.20) — hedefe %0.94 kaldı
  Bölge kırıldı:  NO
  RSI erken çıkış: NO (58.4 < 65)

ACTION: HOLD
NOTE: Hedefe %0.94 kaldı, RSI henüz aşırı alım değil — pozisyonu koru
```
