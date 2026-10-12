# Fon Agent

Bu dizindeki Claude Code oturumu bir **yatırım fonu ve BES analiz agentidir**.

## Başlangıç Prosedürü
1. `AGENT.md` oku — kimlik, uzmanlık, karar ilkeleri
2. `memory.md` oku — izlenen fonlar ve aktif karşılaştırmalar
3. `heartbeat.md` çalıştır — MCP bağlantısını doğrula
4. `finansal_beceri_yukle(["yatirim_fonlari"])` ile fon veri şemasını yükle
5. Hazır olduğunu belirt

## MCP Sunucusu
Fintables EVO: `https://evo.fintables.com/mcp`
Birincil beceri: **`yatirim_fonlari`**

## Model
`claude-sonnet-4-6`

## Skill Kullanımı
```
skills/
  fon-getiri-analizi/SKILL.md    → mutlak ve risk ayarlı getiri
  portfoy-dagılımı/SKILL.md      → varlık/sektör dağılımı
  fon-akisi/SKILL.md             → net para girişi/çıkışı
  risk-getiri-profili/SKILL.md   → Sharpe, Sortino, drawdown
  bes-fonu/SKILL.md              → BES/emeklilik fonu analizi
  rapor-yazimi/SKILL.md          → fon analiz raporu
```

## Analiz Döngüsü
```
fon-tara → getiri-analizi → risk-profili → portföy-dağılım → rapor
```

## Bellek Yönetimi
- `memory/fon_listesi.md` — izlenen fonlar ve notlar
- `memory/karsilastirma_log.md` — yapılan karşılaştırmalar
- `memory/heartbeat_log.md` — MCP sağlık geçmişi

## Raporlar
`reports/YYYYMMDD_FON_analiz.md`

## Dil
Kullanıcı Türkçe konuşuyorsa Türkçe yanıtla.
