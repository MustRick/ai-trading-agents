# Skill: Static Scraping

## Ne Yapar
Tarayıcı açmadan curl_cffi ile hızlı HTTP GET/POST isteği gönderir.
Gerçek Chrome TLS parmak izi taklit ederek basit anti-bot korumalarını geçer.

## Ne Zaman Kullanılır
- Sayfa kaynağı doğrudan HTML döndürüyor (JavaScript render gerekmez)
- Haber siteleri, blog, statik katalog, JSON API
- `fetcher_get` ile 403 almıyorsa buradan başla — en hızlı yol

## Adımlar

### GET İsteği
```
fetcher_get(
  url          = "https://hedef-site.com/sayfa",
  impersonate  = "chrome",          # varsayılan, genellikle yeterli
  stealthy_headers = True,          # gerçekçi başlıklar
  css_queries  = ["h1::text", ".price::text", "a.next::attr(href)"],
  timeout      = 30
)
```

### POST İsteği (form / API)
```
fetcher_post(
  url       = "https://hedef-site.com/api/arama",
  json_data = {"q": "arama terimi", "page": 1},
  headers   = {"Accept": "application/json"},
  css_queries = [],   # JSON yanıtsa boş bırak, html alanını parse et
)
```

## CSS Seçici Kuralları
| İstenen Veri | Seçici Formatı |
|---|---|
| Eleman metni | `div.classname::text` |
| Bağlantı href'i | `a.link::attr(href)` |
| Resim src'si | `img.photo::attr(src)` |
| Veri niteliği | `div[data-id]::attr(data-id)` |
| İlk eşleşme | Tek `get()` — seçiciye `::text` yeterli |
| Tüm eşleşmeler | `getall()` — liste döner |

## Çıktı Formatı
```
STATUS: 200 | 403 | 429 | 503
FETCHER: static
URL: https://...
TITLE: Sayfa Başlığı
CSS_RESULTS:
  h1::text → ["Başlık"]
  .price::text → ["₺ 1.299", "₺ 899"]
LINKS: ["/sayfa/2", "/sayfa/3"]
NEXT_ACTION: parse → veri-ayristirma | retry → stealth-scraping
```

## Hata Protokolü
- **403 / 429 / 503:** → `stealth-scraping` skillini başlat
- **Boş HTML / başlık yok:** → JavaScript render gerekebilir → `dynamic-scraping`
- **Timeout:** → timeout değerini 60'a çıkar, tekrar dene
