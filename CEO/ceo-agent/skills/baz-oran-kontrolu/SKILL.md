# Skill: Baz Oran Kontrolü

## Amaç

"Bu skor aralığı geçmişte ne kadar tuttu?" sorusunu yanıtlar. Geçmiş isabet oranlarını bugünkü karara referans olarak sunar; aşırı güveni frenler.

## Tetikleyici

- Pre-mortem sonrası, Rick'e öneri sunulmadan önce
- Haftalık raporda her departmanın kümülatif isabet özeti için

## Süreç

1. `scripts/gecmis_isabet.py` çalıştır; mevcut kompozit skor aralığını geç.
2. Geri dönen isabet oranını sentez raporuna ekle.
3. İsabet oranı < %40 ise raporun başına **"DÜŞÜK BAZ ORAN"** uyarısı ekle.
4. Departman bazlı isabet oranlarını `memory.md` → "Departman Güvenilirlik Notu"na kaydet.

## Yorumlama Rehberi

| Baz Oran | Yorum |
|---|---|
| ≥ %65 | Geçmişte güçlü performans; skor güvenilir |
| %45–64 | Orta güvenilirlik; ek teyit ara |
| < %45 | Zayıf baz oran; karar ağırlığını düşür, Rick'i uyar |

## Kural

Baz oran düşükse karar değişmez ama **belirsizlik derecesi** raporda açıkça belirtilir. "Skor 72 ama bu aralık geçmişte %38 tuttu" ifadesi Rick'e sunulur.
