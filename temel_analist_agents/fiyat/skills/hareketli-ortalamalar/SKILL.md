# Skill: Hareketli Ortalamalar

## Amaç
EMA ve SMA değerleriyle trendin yönünü, gücünü ve olası dönüş noktalarını tespit et.

## Kullanılan Periyotlar
| Periyot | Tür | Anlamı |
|---------|-----|--------|
| 20 | EMA | Kısa vadeli dinamik destek/direnç |
| 50 | EMA | Orta vadeli trend yönü |
| 200 | SMA | Uzun vadeli bull/bear ayrım çizgisi |

## Sinyaller

### Golden Cross / Death Cross
- **Golden Cross**: EMA20 > EMA50 > SMA200 → güçlü boğa
- **Death Cross**: EMA20 < EMA50 < SMA200 → güçlü ayı

### Fiyat-HO İlişkisi
- Fiyat > EMA20 > EMA50 > SMA200 → sağlıklı yükseliş trendi
- Fiyat < EMA20 < EMA50 < SMA200 → sağlıklı düşüş trendi
- EMA'lar birbirine yakınsıyor → konsolidasyon, kırılmayı bekle

### Eğim Analizi
- EMA20 son 5 günde X% değişim → momentum hızlanıyor/yavaşlıyor

## Adımlar
1. Fintables'tan günlük kapanış fiyatlarını çek (min 200 gün)
2. `scripts/hareketli_ortalama.py` ile EMA20, EMA50, SMA200 hesapla
3. Sinyal tabloso üret
4. Son kapanışın tüm ortalamalarla uzaklığını yüzde olarak raporla

## Çıktı
```
Hareketli Ortalamalar: XXXXX  ({tarih})
────────────────────────────────────────
        Değer    Fiyata Uzaklık   Eğim
EMA20 : X.XX TL   +X.X%          ↑ Artan
EMA50 : X.XX TL   +X.X%          → Yatay
SMA200: X.XX TL   +X.X%          ↑ Artan
────────────────────────────────────────
Diziliş : EMA20 > EMA50 > SMA200  → BOĞA
Sinyal  : Golden Cross aktif (X gün önce)
```
