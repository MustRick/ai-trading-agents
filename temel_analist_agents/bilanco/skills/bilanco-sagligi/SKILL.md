# Skill: Bilanço Sağlığı

## Amaç
"Bu şirketin bilançosu sağlıklı mı?" sorusunu iki bağımsız modelle yanıtla.

## Modeller

### Piotroski F-Skoru (0–9)
Karlılık (4 kriter) + Kaldıraç (3 kriter) + Verimlilik (2 kriter) = toplam 9 puan.
- **7–9:** Güçlü — momentum long pozisyon için uygun
- **5–6:** Ortalama — dikkatli izle
- **0–4:** Zayıf — kısa veya uzak dur

### Altman Z-Skoru (iflas riski)
- **Z > 2.99:** Güvenli bölge
- **1.81 < Z ≤ 2.99:** Gri bölge — dikkat
- **Z ≤ 1.81:** Tehlike — ciddi iflas riski

## Girdi
- Bilanço: dönen varlıklar, toplam varlıklar, kısa/uzun vadeli borç
- Gelir tablosu: net satış, FAVÖK, net kar, önceki yıl verileri
- Nakit akış tablosu: faaliyetlerden nakit akışı

## Adımlar
1. Fintables'tan son 4 çeyrek finansal verisini çek
2. `scripts/piotroski_f.py` ile F-Skoru hesapla
3. `scripts/altman_z.py` ile Z-Skoru hesapla
4. İki modeli birleştirerek kalite kararı ver:

| Piotroski | Altman | Karar |
|-----------|--------|-------|
| 7-9 | >2.99 | Güçlü kalite |
| 5-6 | >1.81 | Ortalama |
| 7-9 | <1.81 | Dikkat — nakit iyi ama borç riskli |
| <5 | <1.81 | Kaçın |

## Çıktı
```
Bilanço Sağlığı: XXXXX
───────────────────────────────
Piotroski F-Skoru: 7/9  → Güçlü
  Karlılık    : ████████ 4/4
  Kaldıraç    : ██████   2/3
  Verimlilik  : ████     1/2

Altman Z-Skoru: 3.42  → Güvenli Bölge

Genel Kalite Kararı: GÜÇLÜ
───────────────────────────────
```

## Notlar
- Bankalar için Altman Z-Skoru geçersizdir — yalnızca Piotroski kullan
- Son çeyrek verisi yoksa LTM (son 12 ay) kullan, belirt
