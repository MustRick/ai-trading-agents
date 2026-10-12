# Skill: Multi-Page Crawl

## Ne Yapar
`spider_crawl` ile otomatik link takip ederek birden fazla sayfayı sırayla tarar.
Sayfalama (pagination), kategori listeleri, ürün katalogları ve tüm site taraması için kullanılır.

Spider, `link_selector` ile bulduğu her linki kuyruğa ekler ve izin verilen domainler
içinde kaldığı sürece otomatik olarak devam eder.

## Ne Zaman Kullanılır
- Sayfalama var: "Sonraki Sayfa", `/page/2`, `?offset=20`
- Liste sayfası → detay sayfası iş akışı
- Kategori + alt kategori tüm ürünler
- Tüm site veya belirli bir alan taraması

## Adımlar

### Temel Sayfalama
```
spider_crawl(
  start_urls    = ["https://site.com/urunler/"],
  item_selectors = {
    "baslik"  : ".product-title::text",
    "fiyat"   : ".product-price::text",
    "url"     : "a.product-link::attr(href)"
  },
  link_selector       = ".pagination .next a",   # sonraki sayfa linki
  allowed_domains     = ["site.com"],
  concurrent_requests = 4,
  max_items           = 500,
  fetcher_type        = "fetcher"   # statik, stealthy, dynamic
)
```

### Detay Sayfası Tarama
Liste → Detay akışı için link_selector ürün linklerini göstermeli:
```
spider_crawl(
  start_urls    = ["https://site.com/liste/"],
  item_selectors = {
    "baslik"      : "h1::text",
    "aciklama"    : ".description::text",
    "fiyat"       : ".price::text",
    "stok"        : ".stock-status::text"
  },
  link_selector = "a.product-detail",   # her ürün detay linkini takip et
  allowed_domains = ["site.com"],
  max_items     = 200,
  fetcher_type  = "fetcher"
)
```

### Anti-Bot Korumalı Site Crawl
```
spider_crawl(
  start_urls     = ["https://korumalı-site.com/liste/"],
  item_selectors = {"ad": "h2::text", "fiyat": ".price::text"},
  link_selector  = ".next-page",
  fetcher_type   = "stealthy",     # her istek için stealth tarayıcı
  download_delay = 1.0,            # istekler arası 1 saniye bekle
  max_items      = 100
)
```

## `fetcher_type` Seçim Rehberi

| Site Tipi | fetcher_type |
|---|---|
| Statik HTML, haber, blog | `"fetcher"` |
| Cloudflare / anti-bot | `"stealthy"` |
| React/Vue SPA | `"dynamic"` |

## item_selectors Yazım Kuralları
```
# DOĞRU — ::text ile metin değeri
"baslik": "h1.product-title::text"

# DOĞRU — ::attr ile nitelik değeri
"link": "a.product::attr(href)"
"resim": "img.thumb::attr(src)"

# YANLIŞ — ::text / ::attr eksik
"baslik": "h1.product-title"   ← None döner
```

## Çıktı Formatı
```
CRAWL_COMPLETE: True / False (paused)
TOTAL_ITEMS: 347
RETURNED_ITEMS: 200 (max_items sınırı)
STATS:
  requests_count: 35
  elapsed_seconds: 42.1
  requests_per_second: 0.83
  failed_requests_count: 2
ITEMS_SAMPLE:
  [0] {"baslik": "Ürün A", "fiyat": "₺ 299", "url": "/urun/a"}
  [1] {"baslik": "Ürün B", "fiyat": "₺ 499", "url": "/urun/b"}
  ...
NEXT_ACTION: rapor-yazimi | veri-ayristirma (temizlik gerekiyorsa)
```

## Hata Protokolü
- **failed_requests_count yüksek:** → fetcher_type'ı yükselt (fetcher → stealthy)
- **items boş ama requests var:** → item_selectors CSS seçicilerini kontrol et
- **Crawl takılı kaldı:** → allowed_domains kontrol et, site dışına çıkıyor olabilir
- **Çok yavaş:** → `concurrent_requests=8` artır (fetcher tipinde güvenli)
