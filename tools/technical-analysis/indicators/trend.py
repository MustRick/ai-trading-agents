"""Trend göstergeleri: SMA, EMA, Bollinger Bands, ADX, Parabolic SAR"""

import math


def sma(closes: list[float], period: int) -> list[float]:
    return [
        sum(closes[i - period + 1 : i + 1]) / period
        for i in range(period - 1, len(closes))
    ]


def ema(closes: list[float], period: int) -> list[float]:
    if len(closes) < period:
        return []
    k = 2.0 / (period + 1)
    result = [sum(closes[:period]) / period]
    for price in closes[period:]:
        result.append(price * k + result[-1] * (1 - k))
    return result


def bollinger_bands(
    closes: list[float],
    period: int = 20,
    std_multiplier: float = 2.0,
) -> dict[str, list[float]]:
    middle = sma(closes, period)
    upper, lower = [], []
    for i, m in enumerate(middle):
        window = closes[i : i + period]
        variance = sum((x - m) ** 2 for x in window) / period
        std = math.sqrt(variance)
        upper.append(m + std_multiplier * std)
        lower.append(m - std_multiplier * std)
    return {"upper": upper, "middle": middle, "lower": lower}


def adx(
    highs: list[float],
    lows: list[float],
    closes: list[float],
    period: int = 14,
) -> dict[str, list[float]]:
    tr_list, plus_dm, minus_dm = [], [], []
    for i in range(1, len(closes)):
        high_diff = highs[i] - highs[i - 1]
        low_diff = lows[i - 1] - lows[i]
        tr = max(
            highs[i] - lows[i],
            abs(highs[i] - closes[i - 1]),
            abs(lows[i] - closes[i - 1]),
        )
        tr_list.append(tr)
        plus_dm.append(high_diff if high_diff > low_diff and high_diff > 0 else 0.0)
        minus_dm.append(low_diff if low_diff > high_diff and low_diff > 0 else 0.0)

    def _wilder_smooth(data: list[float], period: int) -> list[float]:
        # Pine ta.rma ile uyumlu: ortalama başlangıç, 1/period ağırlıklı güncelleme
        result = [sum(data[:period]) / period]
        for i in range(period, len(data)):
            result.append((result[-1] * (period - 1) + data[i]) / period)
        return result

    atr = _wilder_smooth(tr_list, period)
    s_plus = _wilder_smooth(plus_dm, period)
    s_minus = _wilder_smooth(minus_dm, period)

    plus_di, minus_di, dx_list = [], [], []
    for i in range(len(atr)):
        pdi = 100.0 * s_plus[i] / atr[i] if atr[i] != 0 else 0.0
        mdi = 100.0 * s_minus[i] / atr[i] if atr[i] != 0 else 0.0
        plus_di.append(pdi)
        minus_di.append(mdi)
        denom = pdi + mdi
        dx_list.append(100.0 * abs(pdi - mdi) / denom if denom != 0 else 0.0)

    adx_values = _wilder_smooth(dx_list, period)
    offset = len(plus_di) - len(adx_values)
    return {
        "adx": adx_values,
        "plus_di": plus_di[offset:],
        "minus_di": minus_di[offset:],
    }


def parabolic_sar(
    highs: list[float],
    lows: list[float],
    af_step: float = 0.02,
    af_max: float = 0.2,
) -> list[float]:
    if len(highs) < 2:
        return []

    trend = 1  # 1 = uptrend, -1 = downtrend
    sar = lows[0]
    ep = highs[0]
    af = af_step
    result = [sar]

    for i in range(1, len(highs)):
        prev_sar = sar
        sar = prev_sar + af * (ep - prev_sar)

        if trend == 1:
            sar = min(sar, lows[i - 1], lows[max(0, i - 2)])
            if lows[i] < sar:
                trend = -1
                sar = ep
                ep = lows[i]
                af = af_step
            else:
                if highs[i] > ep:
                    ep = highs[i]
                    af = min(af + af_step, af_max)
        else:
            sar = max(sar, highs[i - 1], highs[max(0, i - 2)])
            if highs[i] > sar:
                trend = 1
                sar = ep
                ep = highs[i]
                af = af_step
            else:
                if lows[i] < ep:
                    ep = lows[i]
                    af = min(af + af_step, af_max)

        result.append(sar)

    return result
