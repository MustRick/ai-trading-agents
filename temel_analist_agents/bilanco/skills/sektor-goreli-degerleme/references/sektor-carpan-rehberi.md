# Sektör Çarpan Rehberi

Tarihsel BIST ortalamaları — referans aralıklar, garanti değil.

## F/K Bant Beklentileri

| Sektör | Düşük | Makul | Yüksek | Not |
|--------|-------|-------|--------|-----|
| Banka | 4-6 | 7-10 | >12 | Faiz döngüsüne duyarlı |
| Teknoloji | 15-20 | 25-40 | >50 | Büyüme beklentisi primli |
| Perakende | 8-12 | 14-20 | >25 | Marj baskısı izle |
| Enerji | 5-8 | 9-14 | >18 | Emtia fiyatına bağlı |
| Holding | 3-6 | 7-10 | >13 | NAD iskontosu önemli |
| Gayrimenkul | 6-10 | 12-18 | >22 | Kira getirisiyle kıyasla |
| Kimya | 7-11 | 12-18 | >22 | Ham madde maliyeti |
| İnşaat | 5-9 | 10-15 | >20 | Proje görünürlüğü düşük |

## PD/DD Bant Beklentileri

| Sektör | Cazip | Normal | Pahalı |
|--------|-------|--------|--------|
| Banka | <0.6 | 0.7-1.2 | >1.5 |
| Teknoloji | <2.0 | 2.5-5.0 | >7.0 |
| Perakende | <1.0 | 1.2-2.5 | >3.5 |
| Enerji | <0.8 | 1.0-1.8 | >2.5 |
| Holding | <0.5 | 0.6-0.9 | >1.2 |

## FD/FAVÖK Bant Beklentileri

| Sektör | Düşük | Normal | Yüksek |
|--------|-------|--------|--------|
| Perakende | <5 | 6-9 | >12 |
| Enerji | <4 | 5-8 | >11 |
| Teknoloji | <10 | 12-20 | >25 |
| Kimya | <5 | 6-9 | >13 |
| Telekomünikasyon | <4 | 5-7 | >9 |

## Kullanım Notu
Bu bantlar z-skor hesabını desteklemek için tarihsel referans noktasıdır. Güncel piyasa koşulları (enflasyon, faiz, döviz) bant beklentilerini yukarı veya aşağı kaydırabilir. `carpan_zskor.py` canlı akran verisini kullanır — bu rehber yalnızca "makul bant" için bağlam sağlar.
