# Skill: Faaliyet Raporu Özeti

## Amaç
Şirketin en son yıllık faaliyet raporundan anahtar bulguları çıkar: strateji, kapasite, iştirakler, riskler, hedefler.

## Faaliyet Raporunda Aranacaklar
### Mutlaka çıkarılacak bölümler:
1. **CEO/Yönetim Mesajı** — öncelikler, vurgu yapılan riskler
2. **Operasyonel Performans** — kapasite kullanımı, üretim/satış hacimleri
3. **Yatırımlar** — CAPEX planı, yeni projeler, tesis açılışları
4. **İştirakler** — yeni alım, satış, değer değişimi
5. **Borçlanma** — refinansman, yeni kredi, tahvil ihracı
6. **Stratejik Hedefler** — 3-5 yıl görünümü, büyüme planı
7. **Risk Faktörleri** — yönetimin öne çıkardığı riskler

## Adımlar
1. `finansal_beceri_yukle(["kap_haberleri"])` ile şemayı yükle
2. Şirketin son faaliyet raporu KAP bildirim ID'sini bul
3. `dokumanlarda_ara` ile anahtar bölümleri ara
4. `dokuman_chunk_yukle` ile ilgili chunk'ları çek
5. Her bölümden 2-3 cümle özet çıkar

## Çıktı Şeması
```
Faaliyet Raporu Özeti: XXXXX  ({yıl})
──────────────────────────────────────────────────
CEO Mesajı   : [2-3 cümle — yönetimin öncelikleri]
Operasyonel  : [kapasite, hacim, verimlilik notu]
Yatırımlar   : [CAPEX tutarı ve odak alanı]
İştirakler   : [önemli değişiklikler]
Borçlanma    : [yeni/refinanse borç detayı]
Hedefler     : [sayısal hedefler varsa belirt]
Riskler      : [yönetimin öne çıkardığı 2-3 risk]
──────────────────────────────────────────────────
Kaynak: KAP Bildirim #{id}  |  Yayın: {tarih}
```

## Not
- Sayısal veriyi finansal tablolardan al — faaliyet raporu metin bağlamı için
- "Şirket X'i hedefliyor" ile "Şirket X'e ulaştı" ayrımını koru
