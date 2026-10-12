# Skill: Portföy Dağılımı Analizi

## Amaç
Fonun varlık sınıfı, sektör ve hisse bazında dağılımını analiz et. Konsantrasyon riski ve yönetici kararlarını değerlendir.

## Analiz Katmanları

### Katman 1: Varlık Sınıfı
- Hisse senedi / Tahvil / Nakit / Altın / Döviz / Diğer
- Toplam %100'e ulaşmalı

### Katman 2: Sektör Dağılımı (hisse payı için)
- BIST sektörlerine göre ağırlık
- Endeks ağırlığından sapma (aktif bahis)

### Katman 3: Bireysel Varlık Konsantrasyonu
- Top 5 / Top 10 varlık ağırlığı
- Tek varlık > %10 → konsantrasyon riski
- Tek sektör > %40 → sektör konsantrasyonu

### Katman 4: Değişim Analizi
- Son çeyrekte portföye giren/çıkan varlıklar
- Yöneticinin ne satın aldığı/sattığı

## Adımlar
1. Son TEFAS portföy raporunu çek
2. Varlık sınıfı dağılımını hesapla
3. Sektör bazında grupla
4. Konsantrasyon metriklerini hesapla
5. Önceki dönemle değişimi karşılaştır

## Çıktı
```
Portföy Dağılımı: {FON_ADI}  ({tarih})
────────────────────────────────────────────
Varlık Sınıfı:
  Hisse    %XX.X  │████████████████
  Tahvil   %XX.X  │████████
  Nakit    %X.X   │██

Top 5 Hisse:
  XXXXX  %X.X   XXXXX  %X.X   ...

Sektör Yoğunlaşma:
  Banka    %XX.X  (BIST100: %XX.X  Sapma: +X.X pp)
  Teknoloji%XX.X  ...

Konsantrasyon Riski: {DÜŞÜK/ORTA/YÜKSEK}
  Top 10 ağırlık: %XX.X
```
