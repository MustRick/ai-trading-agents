# Heartbeat — Tetikleme Takvimi

## Periyodik Çalışmalar

| Zaman | Tetikleyici | Görev |
|---|---|---|
| 09:30 | Günlük açılış | Tüm inbox özetlerini oku → sinyal-sentezi → günlük rapor üret |
| 18:45 | Seans kapanış | Gün sonu pozisyon durumu → delta analizi → daily/ güncelle |
| Cuma 17:30 | Haftalık kapanış | Haftalık sentez → haftalik.md şablonuyla rapor → weekly/ yaz |

## Event Tetikleyiciler

| Olay | Kaynak | Aksiyon |
|---|---|---|
| `risk-portfoy/VETO` geldi | Risk-Portföy | Acil alarm raporu → alerts/ |
| Alarm seviyesi ≥ 2 | Risk-Portföy | Pre-mortem skili tetikle, Rick'e eskalasyon |
| Temel + Teknik çelişki | inbox karşılaştırma | celiski-yonetimi skili çalıştır |
| Departman özeti eksik | 09:30 kontrolü | İlgili departmana uyarı mesajı |

## Sessizlik Protokolü

Hiçbir olay yoksa ve tüm özetler 09:30'a kadar gelmemişse:
1. Eksik departmanı logla.
2. Mevcut özetlerle kısmi sentez yap; raporun başına "EKSİK VERİ" uyarısı ekle.
3. Rick'e bildir.
