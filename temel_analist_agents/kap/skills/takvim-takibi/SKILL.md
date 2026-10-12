# Skill: Finansal Takvim Takibi

## Amaç
Yaklaşan finansal açıklamalar, genel kurul tarihleri ve temettü ödemeleri için takvim üret.

## Takip Edilen Olaylar
| Olay | Önem | Açıklama |
|------|------|----------|
| Çeyrek finansal tablo | ★★★ | Q1(Mart), Q2(Haziran), Q3(Eylül), Q4(Aralık) |
| Yıllık faaliyet raporu | ★★★ | Genellikle Nisan-Mayıs |
| Temettü kararı | ★★★ | Genel kurul öncesi/sonrası |
| Temettü ödemesi | ★★ | KAP'ta ilan edilen ödeme tarihi |
| Genel kurul | ★★ | Olağan veya olağanüstü |
| Halka arz fiyat tespiti | ★★ | Varsa |

## Adımlar
1. `finansal_beceri_yukle(["kap_haberleri"])` ile şemayı yükle
2. Şirketin geçmiş açıklama tarihlerinden sonraki dönem için tahmini tarih hesapla
3. KAP'ta duyurulan kesin tarihler varsa onları kullan
4. Bugünden itibaren sırala

## Tahmini Tarih Hesaplama
- Şirket son 4 çeyreği kaç günde açıkladı? Ortalamasını al
- Bir sonraki çeyrek sonundan o kadar gün ekle

## Çıktı
```
Finansal Takvim: XXXXX  (bugün: {tarih})
────────────────────────────────────────────
Olay                      Tarih         Gün Kaldı   Kesin mi?
2026 Q3 Finansal Tablo    ~2026-11-10   29 gün      Tahmini
Temettü Ödemesi           2026-10-28    15 gün      Kesin (KAP)
Olağanüstü Genel Kurul    2026-10-20    7 gün       Kesin (KAP)
────────────────────────────────────────────
⚠ Yaklaşan kritik olay: Genel Kurul — 7 gün kaldı
```
