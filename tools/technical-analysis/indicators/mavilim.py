"""
MavilimW göstergesi — çok katmanlı WMA cascade.
Yazan: KIVANÇ ÖZBİLGİÇ (@mavilim0732) — Pine Script'ten Python'a çevrildi.
Lisans: MPL 2.0
"""


def _wma(data: list[float], period: int) -> list[float]:
    """Ağırlıklı Hareketli Ortalama (WMA) — yeni verilere daha yüksek ağırlık."""
    if len(data) < period:
        return []
    weights = list(range(1, period + 1))
    total_w = sum(weights)
    result = []
    for i in range(period - 1, len(data)):
        window = data[i - period + 1: i + 1]
        result.append(sum(w * v for w, v in zip(weights, window)) / total_w)
    return result


def mavilim_w(
    closes: list[float],
    fmal: int = 3,
    smal: int = 5,
) -> dict:
    """
    MavilimW: 6 katmanlı WMA cascade ile dinamik trend çizgisi.
    Uzunluklar: fmal → smal → tmal → Fmal → Ftmal → Smal (toplamsal büyüme).

    Sinyal:
      BULLISH  → MAVW yükseliyor (mavi)
      BEARISH  → MAVW düşüyor (kırmızı)
      BUY      → yönü düşüşten yükselişe döndü (alım alarmı)
      SELL     → yönü yükselişten düşüşe döndü (satış alarmı)

    Minimum bar sayısı: fmal + smal + tmal + Fmal + Ftmal + Smal - 5
    """
    tmal  = fmal + smal
    Fmal  = smal + tmal
    Ftmal = tmal + Fmal
    Smal  = Fmal + Ftmal

    M1   = _wma(closes, fmal)
    M2   = _wma(M1, smal)
    M3   = _wma(M2, tmal)
    M4   = _wma(M3, Fmal)
    M5   = _wma(M4, Ftmal)
    MAVW = _wma(M5, Smal)

    min_bars = fmal + (smal - 1) + (tmal - 1) + (Fmal - 1) + (Ftmal - 1) + (Smal - 1)

    if len(MAVW) < 2:
        return {
            "values": MAVW,
            "latest": MAVW[-1] if MAVW else None,
            "signal": "NEUTRAL",
            "buy_signal": False,
            "sell_signal": False,
            "min_bars_required": min_bars,
            "error": f"Yetersiz veri — en az {min_bars} bar gerekli",
        }

    rising  = MAVW[-1] > MAVW[-2]
    falling = MAVW[-1] < MAVW[-2]
    signal  = "BULLISH" if rising else "BEARISH" if falling else "NEUTRAL"

    # Crossover: yön değişimi (Pine: ta.crossover(MAVW, MAVW[1]))
    # = MAVW[-1] > MAVW[-2] VE MAVW[-2] <= MAVW[-3]
    buy_signal  = False
    sell_signal = False
    if len(MAVW) >= 3:
        buy_signal  = MAVW[-1] > MAVW[-2] and MAVW[-2] <= MAVW[-3]
        sell_signal = MAVW[-1] < MAVW[-2] and MAVW[-2] >= MAVW[-3]

    return {
        "values": MAVW,
        "latest": round(MAVW[-1], 6),
        "previous": round(MAVW[-2], 6),
        "signal": signal,
        "buy_signal": buy_signal,
        "sell_signal": sell_signal,
        "trend_slope": round(MAVW[-1] - MAVW[-2], 6),
        "lengths_used": {
            "fmal": fmal, "smal": smal, "tmal": tmal,
            "Fmal": Fmal, "Ftmal": Ftmal, "Smal": Smal,
        },
    }


def mavilim_w_classic(closes: list[float]) -> dict:
    """
    MavilimW önceki versiyonu — sabit Fibonacci dizisi: 3-5-8-13-21-34.
    Dinamik parametresiz, hızlı hesaplama.
    """
    M1    = _wma(closes, 3)
    M2    = _wma(M1, 5)
    M3    = _wma(M2, 8)
    M4    = _wma(M3, 13)
    M5    = _wma(M4, 21)
    MAVW2 = _wma(M5, 34)

    if not MAVW2:
        return {"values": [], "latest": None, "signal": "NEUTRAL",
                "error": "Yetersiz veri — en az 84 bar gerekli"}

    signal = "NEUTRAL"
    buy_signal = sell_signal = False
    if len(MAVW2) >= 2:
        signal = "BULLISH" if MAVW2[-1] > MAVW2[-2] else "BEARISH" if MAVW2[-1] < MAVW2[-2] else "NEUTRAL"
    if len(MAVW2) >= 3:
        buy_signal  = MAVW2[-1] > MAVW2[-2] and MAVW2[-2] <= MAVW2[-3]
        sell_signal = MAVW2[-1] < MAVW2[-2] and MAVW2[-2] >= MAVW2[-3]

    return {
        "values": MAVW2,
        "latest": round(MAVW2[-1], 6),
        "signal": signal,
        "buy_signal": buy_signal,
        "sell_signal": sell_signal,
        "version": "classic_fibonacci_3-5-8-13-21-34",
    }
