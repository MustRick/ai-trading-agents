# Skill: Drawdown Control

## Ne Yapar
Portföy değerinin zirveden ne kadar düştüğünü (drawdown) takip eder.
Önceden belirlenmiş seviyelerde risk azaltma protokolünü devreye alır.

## Drawdown Seviyeleri ve Aksiyonlar
| Drawdown | Seviye | Aksiyon |
|----------|--------|---------|
| %0 - %5  | NORMAL | Standart çalış |
| %5 - %10 | CAUTION | Yeni pozisyon boyutunu %50'ye indir |
| %10 - %15 | ALERT | Sadece en yüksek kaliteli sinyaller, boyut %25 |
| %15 - %20 | DANGER | Yeni pozisyon açma, sadece mevcut yönet |
| >%20 | CRISIS | Tüm pozisyonları kapat, stratejiyi gözden geçir |

## Adımlar
1. `calculate_max_drawdown(equity_curve)` çalıştır
2. `calculate_var(portfolio_value, daily_returns)` ile mevcut risk seviyesini ölç
3. Drawdown seviyesine göre yukarıdaki tablodan aksiyon belirle
4. Kurtarma analizi: zirveye dönmek için ne kadar kazanmak gerekiyor?
   ```
   %10 drawdown → %11.1 kazanmak gerekir
   %20 drawdown → %25.0 kazanmak gerekir
   %50 drawdown → %100.0 kazanmak gerekir
   ```

## Drawdown Önleme Protokolü
- Stop loss kesinlikle taşıma (sadece kâr yönünde taşı)
- Ardışık 3 kayıp işlem → 1 gün mola, strateji gözden geçir
- Haftalık kayıp %3'ü aşarsa → o haftayı bitir

## Çıktı
```
CURRENT_DRAWDOWN: %7.3
MAX_DRAWDOWN: %7.3 (aktif)
PEAK_VALUE: 108,500 TL
CURRENT_VALUE: 100,578 TL
RECOVERY_NEEDED: %7.9
DRAWDOWN_LEVEL: CAUTION
ACTION: REDUCE_NEW_POSITION_SIZE_50%
VaR_95: %2.1 günlük (2,112 TL)
RISK_LEVEL: MEDIUM
```
