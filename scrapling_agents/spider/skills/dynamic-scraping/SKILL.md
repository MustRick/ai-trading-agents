# Skill: Dynamic Scraping

## Ne Yapar
Playwright ile gerçek bir Chromium tarayıcısı başlatır ve sayfadaki tüm JavaScript'i
tam olarak yürüterek DOM'u render eder. React, Vue, Angular gibi SPA'lar ve
lazy-load ile içerik yükleyen siteler için kullanılır.

Stealth modundan farkı: canvas/WebRTC koruma yok — ama daha hafif ve daha hızlı.
JS yürütme öncelikli, anti-fingerprint öncelikli değil.

## Ne Zaman Kullanılır
- `static-scraping` → boş/eksik HTML döndürdü (JS render edilmemiş)
- React, Vue, Angular, Next.js SPA'ları
- Sonsuz scroll (infinite scroll) ile yüklenen içerikler
- Sayfa yüklendikten sonra AJAX ile gelen veriler
- Cloudflare yok ama JavaScript zorunlu

## Adımlar

### Temel Kullanım
```
dynamic_fetch(
  url               = "https://spa-site.com/ürünler",
  headless          = True,
  load_dom          = True,     # JS tam yüklenene kadar bekle
  disable_resources = True,     # görsel yükleme, hız için
  css_queries       = [".product-card .name::text", ".product-card .price::text"]
)
```

### AJAX / Lazy-Load Beklet
```
dynamic_fetch(
  url            = "https://site.com",
  wait_selector  = ".lazy-loaded-grid",   # bu eleman DOM'a girene kadar bekle
  network_idle   = True,                  # tüm AJAX istekleri bitene kadar bekle
  wait           = 1500,                  # ms — ekstra güvenlik beklemesi
  css_queries    = [".lazy-loaded-grid .item h2::text"]
)
```

### Sonsuz Scroll (Infinite Scroll)
Infinite scroll sayfalar için spider_crawl kullanamayız; sayfa başına manuel adımla:
```
# 1. İlk yükleme
dynamic_fetch(url=url, wait=2000, css_queries=[".item::text"])

# 2. Eğer "Daha Fazla" butonu varsa → birden fazla fetch + offset ile yaklaş
# 3. Alternatif: API endpoint'ini tarayıcı developer tools ile bul → fetcher_get ile çek
```

## Karar Matrisi

| Durum | Parametre |
|---|---|
| Hızlı render | `load_dom=True, disable_resources=True` |
| AJAX içerik | `network_idle=True` |
| Belirli eleman | `wait_selector=".hedef"` |
| Ekstra bekleme | `wait=2000` (ms) |
| Proxy | `proxy="http://..."` |

## Çıktı Formatı
```
STATUS: 200
FETCHER: dynamic
URL: https://...
TITLE: Sayfa Başlığı
JS_RENDERED: True
CSS_RESULTS:
  .product-card .name::text → ["Ürün 1", "Ürün 2", ...]
  .product-card .price::text → ["₺ 299", "₺ 449", ...]
NEXT_ACTION: parse → veri-ayristirma | paginate → multi-page-crawl
```

## Hata Protokolü
- **Timeout:** → `wait`'i 3000'e çıkar, `network_idle=False` yap
- **JS hatası / boş DOM:** → `load_dom=True, wait=3000` ile tekrar dene
- **Anti-bot tespit:** → `stealth-scraping` skillini kullan (fingerprint koruması ekler)
- **Çok yavaş:** → `disable_resources=True` ekle

## Performans Notu
`dynamic_fetch` her çağrıda yeni bir tarayıcı başlatır (~2-4 saniye overhead).
Aynı sitede çok sayfa gerekiyorsa `spider_crawl(fetcher_type="dynamic")` kullan —
session paylaşımı sayesinde çok daha hızlıdır.
