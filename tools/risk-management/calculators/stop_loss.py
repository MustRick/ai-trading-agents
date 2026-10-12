"""Stop loss hesaplayıcılar: Yüzde, ATR, Chandelier Exit, Destek Bazlı"""


def calculate_atr(
    highs: list[float],
    lows: list[float],
    closes: list[float],
    period: int = 14,
) -> dict:
    """True Range ve ATR — stop loss hesaplamalarının temeli."""
    if len(closes) < period + 1:
        return {"error": f"En az {period + 1} bar gerekli"}

    tr_list = []
    for i in range(1, len(closes)):
        tr = max(
            highs[i] - lows[i],
            abs(highs[i] - closes[i - 1]),
            abs(lows[i] - closes[i - 1]),
        )
        tr_list.append(tr)

    atr = sum(tr_list[:period]) / period
    atr_values = [atr]
    for i in range(period, len(tr_list)):
        atr = (atr * (period - 1) + tr_list[i]) / period
        atr_values.append(atr)

    latest_atr = atr_values[-1]
    return {
        "atr": round(latest_atr, 4),
        "atr_pct": round(latest_atr / closes[-1] * 100, 2),
        "atr_values": atr_values,
        "volatility_class": (
            "HIGH" if latest_atr / closes[-1] > 0.03
            else "MEDIUM" if latest_atr / closes[-1] > 0.015
            else "LOW"
        ),
    }


def percentage_stop(
    entry_price: float,
    stop_pct: float,
    direction: str = "long",
) -> dict:
    """
    Yüzde tabanlı stop loss — basit ve tutarlı.
    direction: "long" veya "short"
    """
    if direction == "long":
        stop_price = entry_price * (1 - stop_pct / 100)
    else:
        stop_price = entry_price * (1 + stop_pct / 100)

    distance = abs(entry_price - stop_price)
    return {
        "stop_price": round(stop_price, 2),
        "distance": round(distance, 2),
        "distance_pct": stop_pct,
        "direction": direction,
        "method": "percentage",
    }


def atr_stop(
    entry_price: float,
    atr: float,
    multiplier: float = 2.0,
    direction: str = "long",
) -> dict:
    """
    ATR tabanlı stop — volatiliteye göre dinamik mesafe.
    Düşük volatilite = dar stop, yüksek volatilite = geniş stop (whipsaw'dan korur).
    """
    distance = atr * multiplier
    stop_price = (
        entry_price - distance if direction == "long" else entry_price + distance
    )
    return {
        "stop_price": round(stop_price, 2),
        "distance": round(distance, 2),
        "distance_pct": round(distance / entry_price * 100, 2),
        "atr": round(atr, 4),
        "multiplier": multiplier,
        "direction": direction,
        "method": "atr",
    }


def chandelier_exit(
    highs: list[float],
    lows: list[float],
    atr: float,
    multiplier: float = 3.0,
    period: int = 22,
    direction: str = "long",
) -> dict:
    """
    Chandelier Exit — en iyi trailing stop yöntemidir.
    Long: son N günün en yüksek noktasından ATR × çarpan aşağıda.
    Short: son N günün en düşük noktasından ATR × çarpan yukarıda.
    """
    window = min(period, len(highs))
    if direction == "long":
        extreme = max(highs[-window:])
        stop_price = extreme - multiplier * atr
    else:
        extreme = min(lows[-window:])
        stop_price = extreme + multiplier * atr

    return {
        "stop_price": round(stop_price, 2),
        "reference_extreme": round(extreme, 2),
        "atr": round(atr, 4),
        "multiplier": multiplier,
        "lookback_period": window,
        "direction": direction,
        "method": "chandelier_exit",
    }


def support_resistance_stop(
    entry_price: float,
    support_level: float,
    buffer_pct: float = 0.5,
    direction: str = "long",
) -> dict:
    """
    Destek/direnç bazlı stop — teknik seviyenin biraz altına koyar.
    buffer_pct: destek seviyesinin kaç % altına (uzun için) yerleştirilsin.
    """
    if direction == "long":
        stop_price = support_level * (1 - buffer_pct / 100)
    else:
        stop_price = support_level * (1 + buffer_pct / 100)

    distance = abs(entry_price - stop_price)
    distance_pct = distance / entry_price * 100

    risk_rating = (
        "TIGHT" if distance_pct < 2
        else "NORMAL" if distance_pct < 5
        else "WIDE"
    )

    return {
        "stop_price": round(stop_price, 2),
        "support_level": support_level,
        "buffer_pct": buffer_pct,
        "distance": round(distance, 2),
        "distance_pct": round(distance_pct, 2),
        "risk_rating": risk_rating,
        "method": "support_resistance",
        "warning": "WIDE_STOP_HIGH_RISK" if distance_pct > 7 else None,
    }


def trailing_stop_update(
    current_price: float,
    current_stop: float,
    trail_pct: float,
    direction: str = "long",
) -> dict:
    """
    Trailing stop güncelleme — fiyat lehimize hareket edince stop'u sürükle.
    Mevcut stop daha iyi konumdaysa değiştirme (sadece lehimize hareket eder).
    """
    if direction == "long":
        new_stop = current_price * (1 - trail_pct / 100)
        updated_stop = max(current_stop, new_stop)
        moved = updated_stop > current_stop
    else:
        new_stop = current_price * (1 + trail_pct / 100)
        updated_stop = min(current_stop, new_stop)
        moved = updated_stop < current_stop

    return {
        "previous_stop": round(current_stop, 2),
        "new_stop": round(updated_stop, 2),
        "stop_moved": moved,
        "trail_distance": round(abs(current_price - updated_stop), 2),
        "trail_pct": trail_pct,
        "locked_profit": round(abs(updated_stop - current_stop), 2) if moved else 0,
    }
