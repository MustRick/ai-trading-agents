# Skill: Risk Sizing

## Ne Yapar
Giriş noktası ve stop mesafesine göre pozisyon büyüklüğünü hesaplar.
Sabit risk prensibi: portföyün maksimum %1-2'si bir işlemde riske atılır.

## Formül
```
Risk Tutarı    = Portföy × Risk Yüzdesi (varsayılan: %1)
Stop Mesafesi  = Giriş Fiyatı - Stop Fiyatı
Pozisyon Adedi = Risk Tutarı / Stop Mesafesi
```

## Ayarlamalar
| Sinyal Gücü | Risk Yüzdesi |
|-------------|--------------|
| STRONG      | %1.5         |
| MODERATE    | %1.0         |
| WEAK        | %0.5         |

## Çıktı Formatı
```
PORTFOLIO: 100,000
RISK_PCT: 1.0%
RISK_AMOUNT: 1,000
ENTRY: 140.2
STOP: 138.3
STOP_DISTANCE: 1.9 (%1.36)
POSITION_SIZE: 526 adet (yüzde olarak: %0.74 portföy ağırlığı)
MAX_LOSS: 1,000
```

## Notlar
- Gerçek emir önerilmez, yalnızca boyut hesabı yapılır
- Tek seferde 3'ten fazla açık pozisyon önerilmez (toplam risk %3)
