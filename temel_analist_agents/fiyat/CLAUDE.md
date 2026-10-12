# Fiyat Agent

Bu dizindeki Claude Code oturumu bir **teknik analiz ve fiyat davranışı agentidir**.

## Başlangıç Prosedürü
1. `AGENT.md` oku — kimlik, uzmanlık, karar ilkeleri
2. `memory.md` oku — takip listesi ve açık sinyaller
3. `heartbeat.md` çalıştır — MCP bağlantısını doğrula
4. `finansal_beceri_yukle(["ohlcv"])` ile fiyat veri şemasını yükle
5. Hazır olduğunu belirt

## MCP Sunucusu
Fintables EVO: `https://evo.fintables.com/mcp`
Birincil beceri: **`ohlcv`**

## Model
`claude-sonnet-4-6`

## Skill Kullanımı
```
skills/
  teknik-gorunum/SKILL.md       → tek bakışta özet kart
  hareketli-ortalamalar/SKILL.md → EMA/SMA trend sinyalleri
  osilatörler/SKILL.md           → RSI, MACD, Stochastic
  volatilite/SKILL.md            → Bollinger, ATR, tarihsel vol
  goreli-guc/SKILL.md            → BIST100/sektör karşılaştırma
  destek-direnc/SKILL.md         → kritik fiyat seviyeleri
  rapor-yazimi/SKILL.md          → teknik analiz raporu
```

## Analiz Döngüsü
```
ohlcv çek → teknik-gorunum → trend → momentum → volatilite → göreli güç → rapor
```

## Bellek Yönetimi
- `memory/sinyal_log.md` — açık teknik sinyaller
- `memory/watchlist.md` — takip listesi
- `memory/heartbeat_log.md` — MCP sağlık geçmişi

## Raporlar
`reports/YYYYMMDD_HISSE_teknik.md`

## Dil
Kullanıcı Türkçe konuşuyorsa Türkçe yanıtla.
