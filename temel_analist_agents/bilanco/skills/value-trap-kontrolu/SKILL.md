# Skill: Value Trap Kontrolü

## Amaç
"Bu hisse ucuz görünüyor, ama neden ucuz?" — yapısal veya geçici düşük değerlemeyi ayırt et.

## Value Trap Nedir?
Hissenin çarpanları sektör medyanının altında olmakla birlikte:
- Kazanç kapasitesi kalıcı olarak düşüyor
- Borç yükü yönetilemez seviyede artıyor
- Rekabet avantajı (moat) eriyor
- Sektörel yıkım devam ediyor

## Kontrol Listesi (8 sinyal)

### Kazanç Kalitesi
- [ ] **K1** — Son 3 yılda net kar düşüş trendi (her yıl azalan)
- [ ] **K2** — Faaliyet nakit akışı ≠ Net kar (büyük tahakkuk farkı)
- [ ] **K3** — FAVÖK marjı son 2 yıldır düşüyor

### Borç Yapısı
- [ ] **B1** — Net Borç / FAVÖK > 4.0 (sektöre göre ayarla)
- [ ] **B2** — Kısa vadeli borç, dönen varlıkların %80'inden fazla

### Rekabetçi Pozisyon
- [ ] **R1** — Pazar payı son 3 yılda gerilemiş (gelir büyümesi < sektör büyümesi)
- [ ] **R2** — Brüt kar marjı sürekli eğim aşağı (3 yıl)

### Yapısal Risk
- [ ] **Y1** — Sektör teknolojik dönüşüm altında (dijital, otomasyon baskısı)

## Skorlama
- **0–2 sinyal:** Value trap olasılığı düşük — değerleme geçici baskıdan kaynaklanıyor olabilir
- **3–4 sinyal:** Dikkatli ol — kısmi value trap riski, yakın izle
- **5+ sinyal:** Yüksek value trap riski — ucuz görünmesine rağmen uzak dur

## Adımlar
1. Fintables'tan son 3 yıl gelir tablosu ve bilanço çek
2. Her K, B, R, Y sinyali için hesapla ve işaretle
3. Toplam sinyal sayısını raporla
4. 3+ sinyal varsa: hangi sinyallerin kalıcı, hangilerinin geçici olduğunu tartış

## Çıktı
```
Value Trap Kontrolü: XXXXX
───────────────────────────────────
Sinyal                     Durum   Ağırlık
K1 Kar düşüş trendi        ✗ YOK   —
K2 Nakit ≠ Kar             ✓ VAR   ⚠
K3 FAVÖK marj düşüşü       ✗ YOK   —
B1 Borç/FAVÖK > 4          ✓ VAR   ⚠
B2 KV borç baskısı         ✗ YOK   —
R1 Pazar payı kaybı        ✗ YOK   —
R2 Brüt marj eğimi         ✓ VAR   ⚠
Y1 Sektörel bozunum        ✗ YOK   —
───────────────────────────────────
Aktif Sinyal: 3/8  →  DİKKATLİ OL
```
