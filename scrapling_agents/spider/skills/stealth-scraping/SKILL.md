# Skill: Stealth Scraping

## Ne Yapar
Gerçek Chromium tarayıcısı başlatarak neredeyse tüm anti-bot korumaları ve
Cloudflare Turnstile / Interstitial meydan okumalarını geçer.

Canvas parmak izi gürültüsü, WebRTC sızıntı koruması, gerçekçi kullanıcı davranışı
simülasyonu otomatik olarak uygulanır.

## Ne Zaman Kullanılır
- `static-scraping` → 403 / 429 / bot detection sayfası döndürdü
- Cloudflare, Imperva, DataDome, PerimeterX koruması var
- Site fingerprinting ile bot tespiti yapıyor
- JavaScript ile kullanıcı davranışı analiz ediliyor

## Adımlar

### Temel Kullanım
```
stealthy_fetch(
  url               = "https://korumalı-site.com",
  headless          = True,
  disable_resources = True,    # görsel/font yükleme, hız için
  block_ads         = True,    # reklam domainlerini engelle
  timeout           = 30000,   # ms cinsinden
  css_queries       = ["h1::text", ".price::text"]
)
```

### Cloudflare Çözümü
```
stealthy_fetch(
  url              = "https://cloudflare-korumalı.com",
  solve_cloudflare = True,      # Turnstile/Interstitial otomatik çöz
  network_idle     = True,      # CF challenge sonrası bekle
  wait             = 2000,      # ms — challenge geçildikten sonra ekstra bekle
  headless         = True,
  css_queries      = ["main::text"]
)
```

### Belirli Eleman Yüklenene Kadar Bekle
```
stealthy_fetch(
  url            = "https://site.com",
  wait_selector  = ".product-grid",   # bu seçici görünene kadar bekle
  timeout        = 45000,
  css_queries    = [".product-grid .item::text"]
)
```

## Karar Matrisi

| Durum | Parametre |
|---|---|
| Normal anti-bot | `headless=True, disable_resources=True` |
| Cloudflare Interstitial | `solve_cloudflare=True, network_idle=True` |
| Dinamik içerik var | `wait_selector=".target"` |
| Proxy gerekiyor | `proxy="http://user:pass@host:port"` |
| Gerçek Chrome gerekiyor | `real_chrome=True` (bilgisayarda Chrome kurulu olmalı) |

## Çıktı Formatı
```
STATUS: 200
FETCHER: stealthy
URL: https://...
CLOUDFLARE_PASSED: True / False
TITLE: Sayfa Başlığı
CSS_RESULTS:
  .price::text → ["₺ 4.599"]
NEXT_ACTION: parse → veri-ayristirma | escalate → dynamic-scraping
```

## Hata Protokolü
- **Hâlâ 403 / bot sayfası:** → `real_chrome=True` ile tekrar dene
- **HTML boş / JS yüklenmedi:** → `dynamic-scraping` ile devam et
- **Cloudflare çözülemedi:** → `solve_cloudflare=True, wait=5000` artır
- **Timeout:** → timeout 60000'e çıkar, `network_idle=True` ekle

## Önemli Notlar
- İlk çalıştırmada Chromium indirilebilir (~150 MB) — bu normaldir
- `disable_resources=True` → görsel/font yüklenmez, %40 hız kazancı
- `block_ads=True` → izleme scriptleri çalışmaz, parmak izi kirlenme riski azalır
