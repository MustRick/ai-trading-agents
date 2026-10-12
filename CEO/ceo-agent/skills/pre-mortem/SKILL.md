# Skill: Pre-Mortem

## Amaç

"Bu işlem 6 ay sonra neden zarar etmiş olur?" sorusunu, pozisyon açılmadan önce sistematik biçimde yanıtlar. Survivorship bias'ını ve aşırı iyimserliği kırar.

## Tetikleyici

- Kompozit skor ≥ 55 (Koşullu Al veya üstü) olan her öneride zorunlu
- Rick'in onayına sunulmadan önce çalıştırılır
- Alarm seviyesi ≥ 2 olan açık pozisyonlarda tekrar çalıştırılır

## Süreç

### Adım 1 — Senaryoları oluştur
Şu başlıklar altında en kötü durum senaryosu yaz:

| Kategori | Soru |
|---|---|
| Değerleme | Piyasa bu hisseyi neden daha düşük fiyatlamalı? |
| Bilanço | Hangi kalemler beklentinin altında gelebilir? |
| Makro | Faiz / kur / büyüme hangi yönde evrilirse tez bozulur? |
| Sektör | Rekabetçi baskı veya regülasyon riski nedir? |
| Teknik | Stop'u geçip trend dönerse ne olur? |
| Portföy | Bu pozisyon portföydeki başka bir şeyle korelasyonla zararı büyütür mü? |

### Adım 2 — Olasılık ve etki skoru
Her senaryo için:
- **Olasılık**: Düşük / Orta / Yüksek
- **Etki**: Küçük (<3%) / Orta (3–8%) / Büyük (>8%)

### Adım 3 — Kırmızı bayrak filtresi
Herhangi bir senaryo `Yüksek olasılık + Büyük etki` kombinasyonuna sahipse → otomatik `Geç` kararı. Rick'e detaylı gerekçeyle sun.

### Adım 4 — Koşul listesi
Kırmızı bayrak yoksa; tezi tehdit eden ama olası olmayan riskler için "bu gerçekleşirse çık" koşullarını yaz.

## Çıktı Formatı

```
PRE-MORTEM: <SEMBOL> — <tarih>

SENARYO         | OLASILIK | ETKİ   | KOŞUL
----------------|----------|--------|------
<senaryo 1>     | Orta     | Küçük  | <koşul>
<senaryo 2>     | Düşük    | Büyük  | <koşul>
...

KIRMIZI BAYRAK : VAR / YOK
SONUÇ          : Devam et / Geç
KOŞULLAR       : <varsa liste>
```
