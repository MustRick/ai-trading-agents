# Heartbeat

## Prosedür
1. `mcp__fintables__authenticate` çağır
2. Başarılı → `memory/heartbeat_log.md` güncelle (OK)
3. Hata → OAuth akışını başlat, `complete_authentication` ile tamamla

## Başlangıç Komutu
```bash
claude -p "Heartbeat çalıştır" \
  --mcp-config temel_analist_Agents/fiyat/mcp.json \
  --model claude-sonnet-4-6
```

## Başarı Kriteri
- authenticate 5 saniye içinde yanıt veriyor
- Log güncellendi
