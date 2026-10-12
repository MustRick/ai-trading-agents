"""Momentum göstergeleri: RSI, Stochastic, MACD, ROC, Williams %R, CCI"""

from typing import Optional


def rsi(closes: list[float], period: int = 14) -> list[float]:
    if len(closes) < period + 1:
        return []
    gains, losses = [], []
    for i in range(1, len(closes)):
        diff = closes[i] - closes[i - 1]
        gains.append(max(diff, 0.0))
        losses.append(max(-diff, 0.0))

    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period
    results = []

    for i in range(period, len(gains)):
        if avg_loss == 0:
            results.append(100.0)
        else:
            rs = avg_gain / avg_loss
            results.append(100.0 - 100.0 / (1.0 + rs))
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period

    return results


def stochastic(
    highs: list[float],
    lows: list[float],
    closes: list[float],
    k_period: int = 14,
    d_period: int = 3,
) -> dict[str, list[float]]:
    k_values = []
    for i in range(k_period - 1, len(closes)):
        window_high = max(highs[i - k_period + 1 : i + 1])
        window_low = min(lows[i - k_period + 1 : i + 1])
        denom = window_high - window_low
        k = 100.0 * (closes[i] - window_low) / denom if denom != 0 else 50.0
        k_values.append(k)

    d_values = []
    for i in range(d_period - 1, len(k_values)):
        d_values.append(sum(k_values[i - d_period + 1 : i + 1]) / d_period)

    return {"k": k_values, "d": d_values}


def macd(
    closes: list[float],
    fast_period: int = 12,
    slow_period: int = 26,
    signal_period: int = 9,
) -> dict[str, list[float]]:
    def _ema(data: list[float], period: int) -> list[float]:
        if len(data) < period:
            return []
        k = 2.0 / (period + 1)
        result = [sum(data[:period]) / period]
        for price in data[period:]:
            result.append(price * k + result[-1] * (1 - k))
        return result

    ema_fast = _ema(closes, fast_period)
    ema_slow = _ema(closes, slow_period)

    offset = slow_period - fast_period
    macd_line = [ema_fast[i + offset] - ema_slow[i] for i in range(len(ema_slow))]

    signal_line = _ema(macd_line, signal_period)
    offset2 = len(macd_line) - len(signal_line)
    histogram = [macd_line[i + offset2] - signal_line[i] for i in range(len(signal_line))]

    return {"macd": macd_line, "signal": signal_line, "histogram": histogram}


def roc(closes: list[float], period: int = 12) -> list[float]:
    result = []
    for i in range(period, len(closes)):
        base = closes[i - period]
        result.append(((closes[i] - base) / base) * 100.0 if base != 0 else 0.0)
    return result


def williams_r(
    highs: list[float],
    lows: list[float],
    closes: list[float],
    period: int = 14,
) -> list[float]:
    result = []
    for i in range(period - 1, len(closes)):
        hh = max(highs[i - period + 1 : i + 1])
        ll = min(lows[i - period + 1 : i + 1])
        denom = hh - ll
        wr = -100.0 * (hh - closes[i]) / denom if denom != 0 else -50.0
        result.append(wr)
    return result


def cci(
    highs: list[float],
    lows: list[float],
    closes: list[float],
    period: int = 20,
) -> list[float]:
    result = []
    for i in range(period - 1, len(closes)):
        tp_window = [
            (highs[j] + lows[j] + closes[j]) / 3.0
            for j in range(i - period + 1, i + 1)
        ]
        tp_mean = sum(tp_window) / period
        mean_dev = sum(abs(tp - tp_mean) for tp in tp_window) / period
        cci_val = (tp_window[-1] - tp_mean) / (0.015 * mean_dev) if mean_dev != 0 else 0.0
        result.append(cci_val)
    return result
