# Heartbeat — Zone Sniper

## Zamanlama
| Tetikleyici | Eylem |
|-------------|-------|
| Piyasa açılışı (09:35) | Tüm watchlist için zone-entry-scanner çalıştır |
| Her 30 dk (gün içi) | Aktif kurulumları izle, proximity değişti mi? |
| Her kapanış (17:35) | Açık pozisyonlar için exit-manager |
| S/R bölgesi kırıldığında | Anlık: o bölgeye bağlı kurulumları iptal et |
| RSI 30 altı / 70 üstü | Anlık: o sembol için tam analiz başlat |

## Günlük Tarama Rutini
```
1. calculate_sr_zones       → Her sembol için güncel bölgeler
2. proximity filtresi       → Hangi semboller bölge yakınında?
3. calculate_rsi            → Yakın sembollerde RSI kontrolü
4. SETUP_READY listesi çıkar → sinyal puanı ≥ 3 olanlar
5. POTENTIAL_SETUP listesi  → sinyal puanı 1-2, izlemeye al
6. Raporu kaydet
```

## Sinyal Öncelik Sırası
1. **STRONG_SIGNAL** (puan ≥ 5): Hemen entry-trigger
2. **MODERATE_SIGNAL** (puan 3-4): entry-trigger (yarım boyut)
3. **POTENTIAL_SETUP** (puan 1-2): memory.md'ye ekle, izle

## Bekleme Koşulları
- Bölge yoksa (az pivot) → o sembol için analiz duraklat
- Günlük limit (cüzdan-agent) dolmuşsa → sinyal üretme, sadece izle
- Aynı bölgede son 3 işlemden 2'si kayıpsa → o bölgeyi 5 gün skip
