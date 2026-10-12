# Skill: Hisse Tarama

## Amaç
Fintables evreninden sektör, büyüklük ve temel metrik filtrelerine göre aday hisse listesi oluştur.

## Girdi Parametreleri
```yaml
sektor: string          # örn. "banka", "teknoloji", "perakende" (opsiyonel)
piyasa_degeri_min: int  # Milyon TL (opsiyonel)
piyasa_degeri_max: int  # Milyon TL (opsiyonel)
fi_max: float           # F/K üst sınırı (opsiyonel)
pd_dd_max: float        # PD/DD üst sınırı (opsiyonel)
temettü_verimi_min: float  # % (opsiyonel)
limit: int              # Döndürülecek maksimum hisse, varsayılan 20
```

## Adımlar
1. MCP oturumunun açık olduğunu doğrula (`/heartbeat`)
2. Fintables araçları ile hisse listesini çek
3. Belirtilen filtreleri sırayla uygula
4. Sonucu F/K artan sırada sırala
5. Her aday için temel çarpanları (F/K, PD/DD, FD/FAVÖK) özet tabloda sun

## Çıktı Şeması
```
| Hisse | Sektör | Piy.Değeri | F/K | PD/DD | FD/FAVÖK | Temettü% |
|-------|--------|-----------|-----|-------|----------|----------|
| XXXXX | ...    | ...       | ... | ...   | ...      | ...      |
```

## Sonraki Adım
Çıktıyı `sektor-goreli-degerleme` skill'ine geçir — sektör medyanı olmadan çarpanlar anlamsız.

## Notlar
- Finansal sektörler için FD/FAVÖK yerine F/K ve PD/DD tercih et
- Çarpanı negatif olan hisseler listeye dahil edilmez; ayrı not düş
