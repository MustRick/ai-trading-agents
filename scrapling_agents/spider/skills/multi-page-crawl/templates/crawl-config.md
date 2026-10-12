# Crawl Konfigürasyon Şablonu

## Görev
<!-- Hedef: hangi siteden, ne verisi, neden -->

## Hedef Site
- **URL:** 
- **Tip:** Statik / Anti-bot korumalı / SPA (birini sil)
- **Sayfalama:** Var / Yok

## Seçiciler

```python
start_urls = [
    "",   # başlangıç URL'leri
]

item_selectors = {
    # "alan_adı": "css_seçici::text veya ::attr(href)",
}

link_selector = ""   # sonraki sayfa veya detay linki; boşsa sayfalama yok
```

## Crawl Parametreleri

| Parametre | Değer | Not |
|---|---|---|
| `fetcher_type` | fetcher / stealthy / dynamic | |
| `concurrent_requests` | 4 | anti-bot varsa 1-2 yap |
| `download_delay` | 0.0 | korumalıysa 1.0+ |
| `max_items` | 200 | |
| `allowed_domains` | [] | domain listesi |

## Beklenen Çıktı
- Tahmini öğe sayısı:
- Alanlar:
- Format: JSON / CSV / Rapor

## Notlar
<!-- Özel davranışlar, bilinen engeller, proxy gereksinimi -->
