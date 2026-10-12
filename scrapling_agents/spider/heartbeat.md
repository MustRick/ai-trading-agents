# Spider — Heartbeat

## Zamanlama Mantığı

Spider tetiklendiğinde şu sırayı izler:

```
Görev Alındı
  │
  ├─ 1. Hedef URL'yi tanı → Karar Ağacı (AGENT.md)
  ├─ 2. İlgili Skill'i başlat
  ├─ 3. Fetch çalıştır
  ├─ 4. Veri ayrıştır (css_queries / parse_html)
  ├─ 5. Sonucu yapılandır
  ├─ 6. Rapor oluştur → reports/ klasörüne kaydet
  └─ 7. memory.md'yi güncelle
```

## Yeniden Deneme Protokolü

| Hata | Bekleme | Eylem |
|---|---|---|
| 429 Too Many Requests | 30 saniye | Aynı istek |
| 503 Geçici Hata | 60 saniye | Aynı istek |
| 403 Bot Tespiti | 0 saniye | Fetcher yükselt |
| Timeout | 0 saniye | Timeout 2x artır, tekrar |
| Sürekli hata (3x) | — | Hatayı raporla, dur |

## Periyodik Görevler

Periyodik tarama tanımlandıysa aşağıdaki format kullanılır:

```
GÖREV: {{site-adı}} fiyat takibi
FREKANS: Günlük / Haftalık / Anlık
SAAT: 08:00
SON_ÇALIŞMA: —
SON_DURUM: —
BİR_SONRAKİ: —
```

## Kaynak Kullanım Limitleri

| Fetcher | Maks Eşzamanlı | Maks İstek/Saniye |
|---|---|---|
| fetcher | 16 | 10 |
| stealthy | 2 | 0.5 |
| dynamic | 2 | 0.3 |
