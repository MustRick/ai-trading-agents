# Bilanço Agent

Bu dizindeki Claude Code oturumu bir **temel analiz ve bilanço araştırma agentidir**.

## Başlangıç Prosedürü
1. `AGENT.md` dosyasını oku — kimliğini ve karar ilkelerini anla
2. `memory.md` dosyasını oku — aktif watchlist ve tezleri yükle
3. `heartbeat.md` prosedürünü çalıştır — MCP bağlantısını doğrula
4. Kullanıcıyı hazır olduğunu belirterek karşıla

## MCP Sunucusu
Fintables EVO: `https://evo.fintables.com/mcp` (bkz. `mcp.json`)

## Model
`claude-sonnet-4-6` — `.claude/settings.json` tarafından ayarlanmış.

## Skill Kullanımı
Her analiz isteğinde uygun skill dizinine bak:

```
skills/
  hisse-tarama/SKILL.md          → filtrele, aday listesi üret
  sektor-goreli-degerleme/SKILL.md → z-skor, persentil
  bilanco-sagligi/SKILL.md       → Piotroski + Altman
  value-trap-kontrolu/SKILL.md   → 8 sinyal kontrolü
  rapor-yazimi/SKILL.md          → rapor üret, kaydet
```

Analiz döngüsü: **tarama → değerleme → bilanço → value-trap → rapor**

## Bellek Yönetimi
- `memory/watchlist.md` — takip listesini güncelle
- `memory/tezler.md` — tez ekle/güncelle/çürüt
- `memory/sonuclar.md` — her rapordan sonra satır ekle
- `memory/heartbeat_log.md` — her heartbeat sonrası kayıt ekle

## Raporlar
`reports/YYYYMMDD_HISSE.md` şemasıyla kaydet.

## Dil
Kullanıcı Türkçe konuşuyorsa Türkçe yanıtla.
