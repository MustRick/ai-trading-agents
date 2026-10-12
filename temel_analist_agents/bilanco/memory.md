# Memory

Kalıcı bağlam indeksi — agent kapanıp açılsa bile bu dosya ve `memory/` klasörü sürekliliği sağlar.

## Aktif Bellek Dosyaları

| Dosya | İçerik | Son Güncelleme |
|-------|--------|---------------|
| [heartbeat_log.md](memory/heartbeat_log.md) | MCP bağlantı geçmişi | — |
| [watchlist.md](memory/watchlist.md) | Takip listesi ve notlar | — |
| [tezler.md](memory/tezler.md) | Aktif yatırım tezleri | — |
| [sonuclar.md](memory/sonuclar.md) | Tamamlanan analizler özeti | — |

## Bellek Kuralları
1. **Geçici veri buraya gelmez** — tek seferlik hesaplamalar `reports/` altına gider
2. **Tez değişince güncelle** — stale tez yanıltıcıdır
3. **Watchlist'e eklerken gerekçe yaz** — "neden takip ediyorum?" olmadan kaydetme
4. **Heartbeat log'u temizleme** — sorun tespiti için 30 günlük geçmiş tut

## Bellek Nasıl Kullanılır
Yeni bir analizde agent şunları yapar:
1. `watchlist.md`'yi oku — hedef hisse daha önce incelenmiş mi?
2. `tezler.md`'yi oku — aktif tez var mı, tutarlı mı?
3. `sonuclar.md`'yi oku — önceki sonuç yeni veriyle çelişiyor mu?
4. Analiz tamamlanınca `sonuclar.md`'yi güncelle

## Kısa Notlar (son 5)
<!-- Agent burayı her analizin sonunda günceller -->
