# Skill: Önemli Gelişme Radarı

## Amaç
Son N günde bir hisse veya sektörde yüksek etkili bildirimleri otomatik öne çıkar. "Ne kaçırdım?" sorusunu yanıtlar.

## Yüksek Etki Kriterleri
Aşağıdaki koşullardan biri varsa YÜKSEk ETKİLİ say:

### Finansal
- Beklentinin ±%15 üzerinde/altında net kar
- FAVÖK marjında ±3 puan değişim
- Net borçta tek dönemde >%20 artış

### Kurumsal
- CEO, CFO veya Yönetim Kurulu Başkanı değişikliği
- Ana ortak hisse satışı (>%5 blok)
- Sermaye artırımı / geri alım programı başlangıcı

### Operasyonel
- Büyük sözleşme kazanımı/kaybı (>piyasa değerinin %10'u)
- Yeni tesis/kapasite duyurusu
- Düzenleyici/hukuki işlem başlangıcı

### Piyasa
- Endeks giriş/çıkış duyurusu
- Halka arz fiyat aralığı açıklaması

## Adımlar
1. Son 30 günlük bildirimleri `bildirim-filtreleme` ile çek
2. Her bildirimi yukarıdaki kriterlere göre değerlendir
3. Yüksek etkili olanları öne çıkar
4. Her biri için 1 cümle özet yaz

## Çıktı
```
Önemli Gelişme Radarı: XXXXX  (son 30 gün)
──────────────────────────────────────────────────────
🔴 2026-09-15: THYAO 2026/06 net karı beklentilerin %22 altında
🔴 2026-08-20: CFO istifası açıklandı
🟡 2026-07-30: Yeni uçak alım sözleşmesi imzalandı (15 adet)
──────────────────────────────────────────────────────
🔴 Kritik: 2  |  🟡 Önemli: 1  |  🟢 Normal: X
```
