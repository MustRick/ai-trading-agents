# Skill: Smart Money Flow

## Ne Yapar
Kurumsal yatırımcı (akıllı para) izini CMF ve VWAP üzerinden takip eder.
Perakende yatırımcı ve kurumsal yatırımcı davranışı arasındaki ayrışmayı tespit eder.

## Teorik Çerçeve
- Kurumlar VWAP civarında alım/satım yapar (benchmark)
- Perakende yatırımcılar genellikle yükseliş tepelerinde alır, diplerde satar
- CMF uzun süre pozitifse kurumlar net alıcı demektir

## Adımlar
1. `calculate_vwap` çalıştır
   - Fiyat VWAP üstünde kapanıyor + yükselen hacim → Kurumsal alım
   - Fiyat VWAP altında kalıyor + yükselen hacim → Kurumsal dağıtım
2. `calculate_cmf(period=20)` çalıştır
   - CMF > +0.15 ve 5+ gün boyunca → Güçlü kurumsal birikim
   - CMF < -0.15 → Kurumsal dağıtım başladı
3. `calculate_mfi` ile para akışının yönünü teyit et

## Smart Money Skoru
| Sinyal | Puan |
|--------|------|
| Fiyat > VWAP, artan hacim | +2 |
| CMF > +0.15 (5 gün) | +2 |
| MFI 50-70 | +1 |
| OBV yeni zirve | +1 |

**Skor ≥ 4 → Kurumsal birikim şüphesi, bul ve raporla**

## Çıktı
```
VWAP: 147.20
PRICE_VS_VWAP: ABOVE (+0.8%)
CMF_20: +0.18 (STRONG_BUYING)
CMF_DAYS_POSITIVE: 7
MFI: 61
SMART_MONEY_SCORE: 5/6
VERDICT: INSTITUTIONAL_ACCUMULATION_LIKELY
```
