# Skill: Veri Ayrıştırma

## Ne Yapar
Scrapling'in `parse_html` aracıyla veya fetch araçlarının `css_queries` / `xpath_queries`
parametreleriyle ham HTML'den yapılandırılmış veri çıkarır.

Zaten indirilmiş HTML'yi yeniden HTTP isteği yapmadan ayrıştırmak, farklı seçiciler
denemek veya iç içe geçmiş veri yapıları çıkarmak için kullanılır.

## Ne Zaman Kullanılır
- Fetch tamamlandı, ham HTML elimde var → yapılandırılmış veri çıkaracağım
- Seçici geliştirme / test aşaması
- Birden fazla farklı seçici kombinasyonu denemek gerekiyor
- `spider_crawl` sonucu eksik alan içeriyor, ek ayrıştırma lazım

## Adımlar

### Ham HTML'den Veri Çekme
```
parse_html(
  html = "<html>...</html>",   # fetch aracının döndürdüğü html alanı
  url  = "https://kaynak-site.com",   # göreli URL'leri çözmek için
  css_queries = [
    "h1::text",
    ".product-name::text",
    ".price::text",
    "table.data tr td::text",
    "a.pagination::attr(href)"
  ],
  xpath_queries = [
    "//div[@class='data']//text()",
    "//table//tr/td[2]/text()"
  ]
)
```

### Tablo Verisi Çıkarma
HTML tabloları için XPath daha güvenilirdir:
```
parse_html(
  html = html_string,
  xpath_queries = [
    "//table[@id='veri-tablosu']//tr/td[1]/text()",   # 1. sütun
    "//table[@id='veri-tablosu']//tr/td[2]/text()",   # 2. sütun
    "//table[@id='veri-tablosu']//tr/td[3]/text()"    # 3. sütun
  ]
)
```

## CSS Seçici Hızlı Referans

| Hedef | Seçici |
|---|---|
| Eleman metni | `div.classname::text` |
| Nitelik değeri | `a::attr(href)`, `img::attr(src)` |
| Veri niteliği | `div::attr(data-price)` |
| İlk eşleşme | seçici normal — tek değer döner |
| Tüm eşleşmeler | aynı seçici — liste döner |
| İç içe seçici | `.parent .child::text` |
| ID seçici | `#element-id::text` |
| Çoklu sınıf | `.class1.class2::text` |

## XPath Hızlı Referans

| Hedef | XPath |
|---|---|
| Tüm metin | `//div[@class='content']//text()` |
| Nitelik | `//a/@href` |
| Koşul | `//div[@data-type='product']//h2/text()` |
| Sıralı eleman | `//ul/li[2]/text()` |
| İçerik filtresi | `//td[contains(text(),'TL')]/text()` |

## Veri Temizleme (scripts/selector_builder.py)
Seçici sonuçları bazen boşluk veya gereksiz karakter içerebilir.
`selector_builder.py` içindeki `clean_results()` fonksiyonu ile temizle:
```python
from scripts.selector_builder import clean_results, zip_columns

prices = clean_results(css_results[".price::text"])
names  = clean_results(css_results[".name::text"])
items  = zip_columns({"ad": names, "fiyat": prices})
```

## Çıktı Formatı
```
CSS_RESULTS:
  h1::text → ["Sayfa Başlığı"]
  .product::text → ["Ürün A", "Ürün B", "Ürün C"]
  a.next::attr(href) → ["/sayfa/2"]

XPATH_RESULTS:
  //table//tr/td[1]/text() → ["Alan1", "Alan2"]
  //table//tr/td[2]/text() → ["Değer1", "Değer2"]

STRUCTURED_DATA:
  [{"ad": "Ürün A", "fiyat": "₺ 299"}, ...]

NEXT_ACTION: rapor-yazimi
```

## Hata Protokolü
- **Sonuç boş liste `[]`:** → seçiciyi browser DevTools (F12) ile doğrula
- **Metin değil eleman döndü:** → `::text` veya `::attr(x)` ekle
- **Çok fazla sonuç:** → seçiciyi daha özgün hale getir (`.parent .child::text`)
- **XPath çalışmıyor:** → `//` ile başla, namespaces sorununu kontrol et
