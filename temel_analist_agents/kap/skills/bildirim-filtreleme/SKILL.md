# Skill: Bildirim Filtreleme

## Amaç
Belirli şirket, tarih aralığı veya bildirim tipine göre KAP'ı tara ve ilgili bildirimleri getir.

## Bildirim Tipleri ve Önem Ağırlıkları
| Tip | Açıklama | Önem |
|-----|----------|------|
| `FINT` | Finansal tablo açıklaması | ★★★ |
| `ÖZEL` | Özel durum bildirimi | ★★★ |
| `SERM` | Sermaye artırımı/azaltımı | ★★★ |
| `TEMT` | Temettü kararı | ★★★ |
| `YÖN` | Yönetim kurulu değişikliği | ★★ |
| `İÇAL` | İçeriden alım/satım | ★★ |
| `BÖLÜ` | Hisse bölünmesi | ★★ |
| `GENEL` | Genel kurul çağrısı | ★ |

## Girdi Parametreleri
```yaml
hisse_kodu: string       # örn. THYAO
baslangic: YYYY-MM-DD
bitis: YYYY-MM-DD
bildirim_tipi: string    # opsiyonel
limit: int               # varsayılan 20
```

## Adımlar
1. `sembol_arama` ile kodu doğrula
2. `finansal_beceri_yukle(["kap_haberleri"])` ile şemayı yükle
3. SQL sorgusuyla bildirimleri çek
4. Her bildirimi önem skoruyla etiketle
5. Tarihsel sıraya göre sun

## Çıktı
```
KAP Bildirimleri: XXXXX  ({tarih_aralığı})
──────────────────────────────────────────────
Tarih       Tip    Önem  Başlık
2026-09-15  FINT   ★★★   2026/06 Finansal Tablolar
2026-08-20  ÖZEL   ★★★   Önemli Yönetim Kararı
2026-07-10  YÖN    ★★    CFO Değişikliği
──────────────────────────────────────────────
Toplam: X bildirim  |  Yüksek önem: X
```

## Not
Sadece liste döndür — içerik özeti için `icerik-analizi` veya `faaliyet-raporu-ozeti` skill'ini kullan.
