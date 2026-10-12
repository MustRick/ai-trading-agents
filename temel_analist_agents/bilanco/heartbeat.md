# Heartbeat

## Amaç
Fintables EVO MCP bağlantısının sağlıklı olduğunu doğrula, oturumu başlat veya yenile.

## Ne Zaman Çalıştır
- Her yeni Claude CLI oturumu açılışında
- Bir Fintables araç çağrısı başarısız olduğunda
- Günlük ilk analizden önce

## Prosedür

### Adım 1 — Bağlantı Testi
```
mcp__fintables__authenticate çağır
```
- Başarılı dönüş → Adım 3'e geç
- Hata / timeout → Adım 2

### Adım 2 — OAuth Akışını Başlat
```
mcp__fintables__authenticate → kullanıcıya URL göster
kullanıcı URL'yi tarayıcıda açar ve doğrular
mcp__fintables__complete_authentication → oturumu tamamla
```

### Adım 3 — Sağlık Raporu Yaz
Başarılı bağlantıdan sonra `memory/heartbeat_log.md` dosyasına ekle:
```
## {YYYY-MM-DD HH:MM}
- Durum: OK
- Araçlar: authenticate, complete_authentication
- Gecikme: ~{ms}
```

### Adım 4 — Hata Durumu
Bağlantı kurulamazsa:
```
## {YYYY-MM-DD HH:MM}
- Durum: HATA
- Mesaj: {hata detayı}
- Eylem: 5 dakika sonra yeniden dene veya manuel giriş iste
```

## Hızlı Test Komutu
Claude CLI terminalinden:
```bash
claude -p "Fintables heartbeat çalıştır" \
  --mcp-config temel_analist_Agents/bilanco/mcp.json \
  --model claude-sonnet-4-6
```

## Başarı Kriteri
- `mcp__fintables__authenticate` 5 saniye içinde yanıt veriyor
- Oturum tokeni alınmış ve geçerli
- `memory/heartbeat_log.md` güncellendi
