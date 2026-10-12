"""Hacim göstergeleri: OBV, VWAP, Chaikin Money Flow, Money Flow Index"""


def obv(closes: list[float], volumes: list[float]) -> list[float]:
    result = [0.0]
    for i in range(1, len(closes)):
        if closes[i] > closes[i - 1]:
            result.append(result[-1] + volumes[i])
        elif closes[i] < closes[i - 1]:
            result.append(result[-1] - volumes[i])
        else:
            result.append(result[-1])
    return result


def vwap(
    highs: list[float],
    lows: list[float],
    closes: list[float],
    volumes: list[float],
) -> list[float]:
    result = []
    cum_tp_vol = 0.0
    cum_vol = 0.0
    for i in range(len(closes)):
        tp = (highs[i] + lows[i] + closes[i]) / 3.0
        cum_tp_vol += tp * volumes[i]
        cum_vol += volumes[i]
        result.append(cum_tp_vol / cum_vol if cum_vol != 0 else tp)
    return result


def chaikin_money_flow(
    highs: list[float],
    lows: list[float],
    closes: list[float],
    volumes: list[float],
    period: int = 20,
) -> list[float]:
    mfv = []
    for i in range(len(closes)):
        denom = highs[i] - lows[i]
        if denom == 0:
            mfv.append(0.0)
        else:
            mfm = ((closes[i] - lows[i]) - (highs[i] - closes[i])) / denom
            mfv.append(mfm * volumes[i])

    result = []
    for i in range(period - 1, len(closes)):
        vol_sum = sum(volumes[i - period + 1 : i + 1])
        mfv_sum = sum(mfv[i - period + 1 : i + 1])
        result.append(mfv_sum / vol_sum if vol_sum != 0 else 0.0)
    return result


def money_flow_index(
    highs: list[float],
    lows: list[float],
    closes: list[float],
    volumes: list[float],
    period: int = 14,
) -> list[float]:
    tp = [(highs[i] + lows[i] + closes[i]) / 3.0 for i in range(len(closes))]
    raw_mf = [tp[i] * volumes[i] for i in range(len(tp))]

    result = []
    for i in range(period, len(tp)):
        pos_mf = sum(
            raw_mf[j] for j in range(i - period + 1, i + 1) if tp[j] > tp[j - 1]
        )
        neg_mf = sum(
            raw_mf[j] for j in range(i - period + 1, i + 1) if tp[j] < tp[j - 1]
        )
        if neg_mf == 0:
            result.append(100.0)
        else:
            mfr = pos_mf / neg_mf
            result.append(100.0 - 100.0 / (1.0 + mfr))
    return result
