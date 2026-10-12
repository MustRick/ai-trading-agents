# Skill: İçerik Analizi (Full-Text & Chunk)

## Amaç
KAP dokümanlarında semantik arama yap, ilgili bölümleri çek ve yorumla. Sayısal veride olmayan niteliksel bilgiyi bul.

## Hangi Soruları Yanıtlar
- "THYAO döviz riskini nasıl yönetiyor?" → dipnot chunk'larından
- "Yönetim kapasite artırımı için ne söyledi?" → faaliyet raporu chunk'larından
- "Şirket X ile sözleşme detayları neler?" → özel durum bildirimi chunk'larından
- "Geçen yılki risk faktörleri neydi?" → yıllık rapor

## Adımlar
1. `dokumanlarda_ara` ile anahtar kelime ve semantik sorgu yap
   - `sayfa`: sayfalama için
   - `sayfa_basi`: sayfa başı sonuç sayısı
2. Sonuçları döküman tipi ve alaka puanına göre sırala
3. En alakalı chunk ID'lerini belirle
4. `dokuman_chunk_yukle` ile tam metni çek
5. Metinden soruya cevap ver, kaynağı belirt

## Sorgu Optimizasyonu
- Türkçe finansal terminoloji kullan: "kur riski" > "döviz risk"
- Dönem filtrele: son 1 yıl yeterli çoğu zaman
- Aynı bildirimden birden fazla chunk gelebilir — bağlamı birleştir

## Çıktı Formatı
```
İçerik Analizi: "{sorgu}"
────────────────────────────────────────────
Kaynak 1: {Bildirim Türü} | {Tarih} | Chunk #{id}
  "{ilgili metin alıntısı}"
  → Yorum: [2-3 cümle analiz]

Kaynak 2: ...
────────────────────────────────────────────
Özet: [tüm kaynakları sentezleyen 3-4 cümle]
```

## Sınır
Chunk metninde yoksa "bilgi mevcut değil" de — uydurma.
