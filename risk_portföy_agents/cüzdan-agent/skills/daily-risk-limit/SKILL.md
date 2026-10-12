# Skill: Daily Risk Limit

## Ne Yapar
Ana paranın günde en fazla ne kadar kaybedebileceğini belirler ve kalan bütçeyi takip eder.
Günlük limit aşılırsa işlemleri durdurur.

## Günlük Limit Mantığı
```
Günlük Limit = Portföy Değeri × Günlük Risk %
Kalan Bütçe  = Günlük Limit − Bugün Kaybedilen
```

Varsayılan: %2 portföy = 100.000 TL portföyde günlük 2.000 TL limit.

## Adımlar
1. `check_daily_loss_limit(portfolio_value, daily_risk_pct, already_lost_today)` çalıştır
2. Durumu değerlendir:
   - **SAFE**: Normal çalış
   - **WARNING** (>%50 kullanıldı): Yeni pozisyon boyutlarını yarıya indir
   - **CRITICAL** (>%80 kullanıldı): Sadece mevcut pozisyonları yönet, yeni açma
   - **LIMIT_BREACHED**: Trading durdu, gün bitti

## Özel Durumlar
- Açık pozisyonda stop tetiklendiyse kaybı `already_lost_today`'e ekle
- Kâr eden pozisyon kapatılırsa bütçe geri kazanılmaz (sadece zarar sayılır)
- Ertesi gün limit sıfırlanır

## Çıktı
```
STATUS: SAFE | WARNING | CRITICAL | LIMIT_BREACHED
MAX_DAILY_LOSS: 2,000 TL (%2)
USED_TODAY: 450 TL (%22.5)
REMAINING_BUDGET: 1,550 TL
ACTION: NORMAL | REDUCE_SIZE | NO_NEW_POSITIONS | STOP_TRADING_TODAY
```
