# Skill: Görev Dağıtımı

## Amaç

Rick'ten gelen yatırım sorusunu veya genel talebi somut departman görevlerine böler. Her departmanın neyi, hangi formatta, hangi sürede teslim edeceğini belirtir.

## Tetikleyici

- Rick yeni bir sembol / tema / soru ilettiğinde
- Haftalık tarama döngüsü başladığında

## Süreç

1. **Talebi ayrıştır**: Sembol mü, sektör mü, makro tema mı?
2. **Departman yetkinlik haritasına bak**: `references/departman-yetkinlik-haritasi.md`
3. **Her departman için görev kartı yaz**:
   ```
   DEPARTMAN: <ad>
   GÖREV: <ne yapacak>
   ÇIKTI FORMATI: <inbox/X altına hangi dosya>
   TERMİN: <saat / gün>
   ÖNCELİK: yüksek / normal / düşük
   ```
4. **Görev kartını ilgili agent'ın `tasks/` klasörüne yaz.**

   Görev kartı dosya adı: `<YYYY-MM-DD_SAAT>_<SEMBOL>_gorev.md`

   | Agent | Görev kartı yolu |
   |---|---|
   | bilanco | `../../../temel_analist_agents/bilanco/tasks/` |
   | fiyat | `../../../temel_analist_agents/fiyat/tasks/` |
   | fon | `../../../temel_analist_agents/fon/tasks/` |
   | kap | `../../../temel_analist_agents/kap/tasks/` |
   | momentum-pulse | `../../../teknik_analist_agents/momentum-pulse/tasks/` |
   | reversal-phantom | `../../../teknik_analist_agents/reversal-phantom/tasks/` |
   | trend-hawk | `../../../teknik_analist_agents/trend-hawk/tasks/` |
   | volume-sentinel | `../../../teknik_analist_agents/volume-sentinel/tasks/` |
   | zone-sniper | `../../../teknik_analist_agents/zone-sniper/tasks/` |
   | spider | `../../../scrapling_agents/spider/tasks/` |
   | cüzdan-agent | `../../../risk_portföy_agents/cüzdan-agent/tasks/` |
5. **09:30 kontrolünde** eksik teslimatları heartbeat.md'deki protokole göre işle.

## Kural

- CEO Agent departman analizine müdahale etmez; sadece görev tanımlar.
- Çakışan veya anlamsız görev kombinasyonlarında (örn. aynı sembol için hem "al" hem "sat" tezi sorma) Rick'e sor.
