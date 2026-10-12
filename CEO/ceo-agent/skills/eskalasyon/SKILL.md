# Skill: Eskalasyon

## Amaç

"Bunu Rick'e ne zaman, nasıl sormalıyım?" sorusunu yanıtlar. Gereksiz interrupt'ı azaltırken kritik kararları kaçırmaz.

## Eskalasyon Seviyeleri

### Seviye 0 — Bilgi (Raporla, Sormadan Devam Et)
- Düşük önem: skor < 40, karar = Geç
- Rutin günlük rapor içeriği
- Baz oran uyarısı (< %45) ama aksiyon gerektirmiyor

### Seviye 1 — Onay Gerekli (Bir Sonraki Raporda Sun)
- Koşullu Al (skor 55–74): Rick'in onayıyla pozisyon açılabilir
- Pre-mortem kırmızı bayrak yok ama koşul listesi var
- Departmanlar arası çelişki çözüldü, ama karar yakın

### Seviye 2 — Acil Onay (Hemen Bildir)
- Güçlü Al (skor ≥ 75) + Pre-mortem temiz
- Risk-Portföy VETO kararı
- Alarm seviyesi ≥ 2 (açık pozisyonda)
- Limit ihlali riski

### Seviye 3 — Kriz (Anında Ulaş)
- Beklenmedik büyük fiyat hareketi (> %10 tek seansta)
- Portföy drawdown eşiği aşıldı (> %8)
- Sistem veya veri hatası şüphesi

## Bildirim Formatı

```
ESKALASİYON SEVİYESİ : <0/1/2/3>
KONU                 : <özet başlık>
SEMBOL               : <varsa>
EYLEM GEREKLİ        : <evet/hayır — varsa ne>
BAĞLAM               : <max 3 cümle>
EKLER                : <rapor dosya yolu>
```

## Kural

- Seviye 2+ bildirimler rapordan önce iletilir.
- Aynı konuda 24 saat içinde ikinci eskalasyon gerekmiyorsa sadece raporda güncelleme yapılır.
- Rick tarafından kapatılmayan Seviye 2+ eskalasyonlar bir sonraki heartbeat'te tekrar kontrol edilir.
