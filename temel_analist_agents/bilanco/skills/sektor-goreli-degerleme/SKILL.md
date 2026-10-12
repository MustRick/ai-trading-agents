# Skill: Sektör Göreli Değerleme

## Amaç
"Bu hisse sektörüne göre ucuz mu, pahalı mı?" sorusunu z-skor ve persentil ile yanıtla.

## Girdi
- Tek hisse kodu veya `hisse-tarama` çıktısı listesi
- Çarpanlar: F/K, PD/DD, FD/FAVÖK (hangisi uygunsa)

## Adımlar
1. Hedef hissenin sektör grubundaki tüm akranları Fintables'tan çek
2. Her çarpan için sektör medyanı ve standart sapmasını hesapla
3. `scripts/carpan_zskor.py` ile z-skor ve persentil üret
4. Yorumla:
   - z < −1.0 → sektöre göre ucuz (alt %16)
   - −1.0 ≤ z ≤ +1.0 → ortalama bant
   - z > +1.0 → sektöre göre pahalı (üst %16)
5. `references/sektor-carpan-rehberi.md` ile bant beklentilerini çapraz kontrol et

## Çıktı
```
Hisse: XXXXX  |  Sektör: Banka  |  Akran sayısı: 12
──────────────────────────────────────────────────
Çarpan    Hisse   Medyan  Z-Skor  Persentil  Yorum
F/K        6.2     8.1    -0.87      19%     Ucuz
PD/DD      0.7     0.9    -1.10      14%     Ucuz
FD/FAVÖK   4.1     5.3    -0.95      17%     Ucuz
──────────────────────────────────────────────────
Genel Değerleme Sinyali: UCUZ (3/3 çarpan alt banda)
```

## Dikkat
- Tek çarpana bağlı karar verme; en az 2 çarpan teyit etmeli
- Banka/sigorta için FD/FAVÖK anlamsız — yalnızca F/K ve PD/DD kullan
- Sonucu `value-trap-kontrolu` ile takip et: ucuz ≠ iyi yatırım
