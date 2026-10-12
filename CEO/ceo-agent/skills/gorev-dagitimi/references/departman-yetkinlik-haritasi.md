# Departman Yetkinlik Haritası

## Temel Analiz

**Sorumluluk**: Aday filtreleme, değerleme, bilanço kalitesi, büyüme tezi.

| Yetkin | Yetsiz |
|---|---|
| F/K, FD/FAVÖK yorumu | Teknik giriş noktası |
| Bilanço güçlü/zayıf tespiti | Kısa vadeli fiyat hareketi |
| Sektörel karşılaştırma | Haber akışı takibi |
| Temettü sürdürülebilirliği | Portföy risk hesabı |

**Çıktı formatı**: `inbox/temel/<SEMBOL>_temel.md`

---

## Teknik Analiz

**Sorumluluk**: Giriş bölgesi, stop seviyesi, hedef, trend durumu.

| Yetkin | Yetsiz |
|---|---|
| Destek/direnç seviyeleri | Şirket fundamentalleri |
| Trend + momentum göstergeleri | Makroekonomik yorum |
| Risk/ödül oranı hesabı | Portföy korelasyonu |
| Stop-loss önerisi | Haber etkisi değerlendirme |

**Çıktı formatı**: `inbox/teknik/<SEMBOL>_teknik.md`

---

## Haber / Olay Analizi

**Sorumluluk**: Şirkete veya sektöre etki eden olayları sınıflandırma.

| Yetkin | Yetsiz |
|---|---|
| Etki sınıfı (pozitif/negatif/nötr) | Fiyat hedefi |
| Kalıcı vs geçici etki tespiti | Teknik seviye yorumu |
| Rakip/sektör karşılaştırması | Portföy limit kontrolü |

**Çıktı formatı**: `inbox/haber/<SEMBOL>_haber.md` veya `inbox/haber/makro_<tarih>.md`

---

## Risk-Portföy

**Sorumluluk**: Portföy durumu, limit kontrolü, korelasyon, stres testi, VETO.

| Yetkin | Yetsiz |
|---|---|
| Açık pozisyon ve limit kullanımı | Şirket analizi |
| Sektör/hisse konsantrasyon kontrolü | Teknik sinyal |
| VaR ve drawdown hesabı | Haber yorumu |
| VETO kararı (limit/kural ihlali) | Görev dağıtımı |

**Çıktı formatı**: `inbox/risk-portfoy/portfoy_durum.md` veya `inbox/risk-portfoy/VETO_<SEMBOL>.md`
