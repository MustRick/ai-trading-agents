# Skill: Fon Akışı Analizi

## Amaç
Fona giren ve çıkan para miktarını izle. "Yatırımcılar bu fona güveniyor mu yoksa kaçıyor mu?"

## Metrikler
- **Net Para Akışı**: Günlük/haftalık/aylık net giriş-çıkış
- **Büyüklük Trendi**: Fon büyüklüğünün zaman içindeki değişimi
- **Akış/Büyüklük Oranı**: Akışın fon büyüklüğüne oranı (normalize)

## Yorumlama
| Akış Durumu | Sinyal |
|-------------|--------|
| Güçlü net giriş + artan büyüklük | Yatırımcı güveni yüksek |
| Net çıkış + azalan büyüklük | Baskı altında — neden araştır |
| Büyüklük artıyor ama getiri düşük | Fiyat etkisi — gerçek giriş değil |
| Yüksek çıkış + iyi performans | Piyasa zamanlaması kayıpları |

## Adımlar
1. Son 90 günlük günlük NAV ve büyüklük verisini çek
2. Günlük net akışı hesapla: Büyüklük değişimi − Getiri etkisi
3. Haftalık ve aylık toplamı üret
4. 30 günlük ortalama akışla karşılaştır

## Çıktı
```
Fon Akışı: {FON_ADI}
────────────────────────────────────────────
          Net Akış    Büyüklük   Kümülatif
Bugün     +X.X TL mn  XXX TL mn   —
1 Hafta   +X.X TL mn             +X.X TL mn
1 Ay      -X.X TL mn             -X.X TL mn
3 Ay      +X.X TL mn             +X.X TL mn
────────────────────────────────────────────
Momentum: {GİRİŞ / ÇIKIŞ / NÖTR}
Yorum   : Son 4 haftada {net giriş/çıkış} eğilimi
```
