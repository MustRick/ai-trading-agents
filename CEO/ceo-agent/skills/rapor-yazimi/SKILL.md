# Skill: Rapor Yazımı

## Amaç

Sentez çıktısını Rick'in okuyacağı net, rakam önce, yorum sonra formatındaki raporlara dönüştürür.

## Şablonlar

| Şablon | Dosya | Ne zaman |
|---|---|---|
| Günlük | `templates/gunluk.md` | 09:30 + 18:45 heartbeat |
| Haftalık | `templates/haftalik.md` | Cuma 17:30 heartbeat |
| Acil Alarm | `templates/acil-alarm.md` | Seviye 2+ eskalasyon |

## Yazım Kuralları

1. **Rakam önce**: "THYAO %4.2 düştü" — "THYAO önemli bir düşüş yaşadı" değil.
2. **Tez cümlesi max 2 cümle**: Fazlası raporun altında "Detay" bölümüne gider.
3. **Kararı başa yaz**: Sonuca ulaşmak için okumak gerekmemeli.
4. **Renk kodu yok, sembol var**: ✓ (yapıldı) / ✗ (yapılmadı) / ? (belirsiz).
5. **Kaynak referansı**: Her rakamın hangi departmandan geldiği parantez içinde.

## Çıktı Yolu

- Günlük: `reports/daily/YYYY-MM-DD.md`
- Haftalık: `reports/weekly/YYYY-WNN.md`
- Alarm: `reports/alerts/YYYY-MM-DD_<sembol>_alarm.md`
