# Memory — Kalıcı Bağlam

## Rick'in Tercihleri

- Risk toleransı: **Orta-düşük**. Drawdown %8'i geçmemeli.
- Tek pozisyon sektör konsantrasyonu: max %20.
- Tercih edilen pozisyon büyüklüğü: portföyün %3–8'i arası.
- Stop-loss disiplini: teknik stop'a riayet zorunlu, gerekçesiz esnetme yok.
- Raporlama tonu: kısa, rakam önce, yorum sonra.

## Departman Ağırlıkları (Kompozit Skor)

```
Temel Analiz      : %35
Teknik Analiz     : %30
Haber/Olay        : %15
Risk-Portföy      : %20  ← negatif sinyal 2× ağırlık taşır
```

Ağırlıklar `kompozit_skor.py` tarafından okunur. Değişiklik için Rick onayı gerekir.

## Açık Tezler

<!-- Aktif pozisyona dayalı tezler buraya eklenir -->
<!-- Format: SEMBOL | Tez özeti | Açılış tarihi | Hedef | Stop -->

## Çelişki Vakası Arşivi

<!-- Format: Tarih | Sembol | Temel sinyal | Teknik sinyal | Alınan karar | Sonuç -->

## Departman Güvenilirlik Notu

<!-- Geçmiş isabet oranlarına göre güncellenir (gecmis_isabet.py çıktısı) -->
<!-- Format: Departman | Son 30 gün isabet % | Son 90 gün isabet % | Not -->
