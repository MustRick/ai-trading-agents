# Skill: Rapor Yazımı

## Ne Yapar
Toplanan ham scraping verisini okunabilir, yapılandırılmış bir rapora dönüştürür.
Kaynak bilgisi, toplama tarihi, veri özeti ve bulgular dahildir.

## Ne Zaman Tetiklenir
- `spider_crawl`, `fetcher_get`, `stealthy_fetch` veya `dynamic_fetch` tamamlandı
- `veri-ayristirma` sonrası yapılandırılmış veri hazır

## Rapor Yapısı

Raporlar `reports/YYYY-MM-DD_<görev-adı>.md` olarak kaydedilir.
Şablon için `templates/rapor.md` kullanılır.

## Adımlar
1. Görev tanımını ve kaynak URL'yi yaz
2. Toplama istatistiklerini ekle (kaç istek, süre, başarı oranı)
3. Veri özetini tablo halinde göster
4. Önemli bulguları madde madde listele
5. Varsa anomalileri / eksik verileri belirt
6. Sonraki adım önerisi ekle

## Veri Özeti Formatı

Sayısal veri için:
```
| Alan | Min | Max | Ortalama | Toplam |
|---|---|---|---|---|
| Fiyat | ₺ 99 | ₺ 9.999 | ₺ 1.247 | — |
| Stok | 0 | 500 | — | 12.340 |
```

Liste verisi için:
```
| # | Ad | Fiyat | URL |
|---|---|---|---|
| 1 | Ürün A | ₺ 299 | /urun/a |
| 2 | Ürün B | ₺ 499 | /urun/b |
...
(ilk 20 göster, kalanı "ve X daha..." ile özetle)
```

## Çıktı Formatı
```
reports/2026-10-12_hedef-site-urunler.md oluşturuldu.
ITEMS: 347
FIELDS: baslik, fiyat, url, stok
ANOMALIES: 12 öğede fiyat eksik
NEXT_ACTION: kullanıcıya sun | memory.md'ye kaydet
```
