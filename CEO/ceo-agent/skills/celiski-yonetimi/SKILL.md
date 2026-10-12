# Skill: Çelişki Yönetimi

## Amaç

"Temel AL dedi, Teknik SAT dedi — ne yapıyoruz?" sorusunu yapılandırılmış bir çerçevede yanıtlar.

## Tetikleyici

- `sinyal-sentezi` skili zıt sinyaller tespit ettiğinde
- İki veya daha fazla departman arası uyumsuzluk varken

## Çelişki Türleri ve Protokol

### Tip 1: Temel AL — Teknik SAT
**Yorum**: İyi şirket, kötü fiyat hareketi. Erken girilmiş veya trend bozuk.
**Protokol**:
1. Teknik departmandan stop ve giriş bölgesi netleştirmesini iste.
2. Temel departmandan "değerleme marjı ne kadar?" sorusunu sor.
3. Karar: Teknik stop yakınsa bekle. Temel marj büyükse küçük pozisyonla gir, stop sıkı tut.

### Tip 2: Temel SAT — Teknik AL
**Yorum**: Momentum var ama temel zayıf. Spekülatif hareket riski.
**Protokol**:
1. Haber departmanından katalizör sorgula.
2. Risk-Portföy'den korelasyon ve limit durumunu al.
3. Karar: Katalizör somutsa ve limit uygunsa kısa vadeli teknik tez; net katalizör yoksa geç.

### Tip 3: İki Departman Nötr, Biri AL, Biri SAT
**Protokol**: Sinyal gücü zayıf; karar otomatik olarak `İzle`'ye düşer. Rick'e bildir.

### Tip 4: Risk-Portföy ile Diğerleri Çelişkisi
**Protokol**: Risk-Portföy'ün VETOsu veya SAT sinyali üstün gelir. İstisna yok.

## Çıktı Formatı

```
ÇELİŞKİ TİPİ : <Tip 1/2/3/4>
SEMBOL       : <sembol>
TEMEL        : <sinyal>
TEKNİK       : <sinyal>
HABER        : <sinyal>
RİSK-PORTFÖY : <sinyal>
KARAR        : <karar>
GEREKÇE      : <max 3 cümle>
SONRAKI ADIM : <ne sorulacak / ne bekleniyor>
```

## Arşivleme

Her çelişki vakası `memory.md` → "Çelişki Vakası Arşivi" bölümüne eklenir.
