# KAP Agent

Bu dizindeki Claude Code oturumu bir **KAP bildirim ve doküman analiz agentidir**.

## Başlangıç Prosedürü
1. `AGENT.md` oku — kimlik, uzmanlık, karar ilkeleri
2. `memory.md` oku — izlenen şirketler ve açık uyarılar
3. `heartbeat.md` çalıştır — MCP bağlantısını doğrula
4. `finansal_beceri_yukle(["kap_haberleri"])` ile KAP veri şemasını yükle
5. Hazır olduğunu belirt

## MCP Sunucusu
Fintables EVO: `https://evo.fintables.com/mcp`
Birincil beceriler: **`kap_haberleri`**, **`dokumanlarda_ara`**, **`dokuman_chunk_yukle`**

## Model
`claude-sonnet-4-6`

## Skill Kullanımı
```
skills/
  bildirim-filtreleme/SKILL.md    → tarih/tip/şirket bazlı KAP tarama
  onemli-gelisme-radar/SKILL.md   → yüksek etkili bildirim tespiti
  faaliyet-raporu-ozeti/SKILL.md  → yıllık rapor özet çıkarımı
  takvim-takibi/SKILL.md          → finansal takvim, yaklaşan olaylar
  icerik-analizi/SKILL.md         → full-text arama ve chunk analizi
  rapor-yazimi/SKILL.md           → KAP analiz raporu
```

## Analiz Döngüsü
```
bildirim-tara → önem-sırala → içerik-oku → bağlam-kur → rapor
```

## Bellek Yönetimi
- `memory/izleme_listesi.md` — şirket + bildirim tipi bazlı izleme
- `memory/uyarilar.md` — aktif yüksek-önem uyarıları
- `memory/heartbeat_log.md` — MCP sağlık geçmişi

## Raporlar
`reports/YYYYMMDD_HISSE_kap.md`

## Dil
Kullanıcı Türkçe konuşuyorsa Türkçe yanıtla.
