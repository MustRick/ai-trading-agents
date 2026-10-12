"""
Reversal sinyalleri — Pine Script SRv2+EMA200+MavilimW+ATR/ADX+Reversal adaptasyonu.
Yapısal kırılım + EMA200 + RSI + ADX düşüşü + ATR spike filtrelerinin birleşimi.
Kaynak: LonesomeTheBlue — MPL 2.0
"""

import math


# ── İç yardımcılar ──────────────────────────────────────────────────────────

def _rsi(closes: list[float], period: int) -> list[float]:
    if len(closes) < period + 1:
        return []
    gains, losses = [], []
    for i in range(1, len(closes)):
        d = closes[i] - closes[i - 1]
        gains.append(max(d, 0.0))
        losses.append(max(-d, 0.0))
    ag = sum(gains[:period]) / period
    al = sum(losses[:period]) / period
    result = []
    for i in range(period, len(gains)):
        result.append(100.0 - 100.0 / (1.0 + ag / al) if al != 0 else 100.0)
        ag = (ag * (period - 1) + gains[i]) / period
        al = (al * (period - 1) + losses[i]) / period
    return result


def _ema(data: list[float], period: int) -> list[float]:
    if len(data) < period:
        return []
    k = 2.0 / (period + 1)
    result = [sum(data[:period]) / period]
    for v in data[period:]:
        result.append(v * k + result[-1] * (1 - k))
    return result


def _sma(data: list[float], period: int) -> list[float]:
    return [sum(data[i - period + 1:i + 1]) / period for i in range(period - 1, len(data))]


def _atr_series(highs, lows, closes, period):
    trs = [max(highs[i] - lows[i], abs(highs[i] - closes[i-1]), abs(lows[i] - closes[i-1]))
           for i in range(1, len(closes))]
    if len(trs) < period:
        return []
    val = sum(trs[:period]) / period
    result = [val]
    for tr in trs[period:]:
        val = (val * (period - 1) + tr) / period
        result.append(val)
    return result


def _adx_series(highs, lows, closes, period, smoothing):
    trs, pdm, mdm = [], [], []
    for i in range(1, len(closes)):
        hd = highs[i] - highs[i - 1]
        ld = lows[i - 1] - lows[i]
        trs.append(max(highs[i]-lows[i], abs(highs[i]-closes[i-1]), abs(lows[i]-closes[i-1])))
        pdm.append(hd if hd > ld and hd > 0 else 0.0)
        mdm.append(ld if ld > hd and ld > 0 else 0.0)

    def wilder(data, p):
        r = [sum(data[:p]) / p]
        for v in data[p:]:
            r.append((r[-1] * (p - 1) + v) / p)
        return r

    if len(trs) < period:
        return [], [], []
    atr_s = wilder(trs, period)
    sp    = wilder(pdm, period)
    sm    = wilder(mdm, period)
    pdi, mdi, dxl = [], [], []
    for i in range(len(atr_s)):
        p = 100 * sp[i] / atr_s[i] if atr_s[i] else 0.0
        m = 100 * sm[i] / atr_s[i] if atr_s[i] else 0.0
        pdi.append(p); mdi.append(m)
        denom = p + m
        dxl.append(100 * abs(p - m) / denom if denom else 0.0)
    if len(dxl) < smoothing:
        return [], [], []
    adx = wilder(dxl, smoothing)
    off = len(pdi) - len(adx)
    return adx, pdi[off:], mdi[off:]


def _pivot_high(src: list[float], left: int, right: int) -> list:
    result = [None] * len(src)
    for i in range(left, len(src) - right):
        if (all(src[i] >= src[i - j] for j in range(1, left + 1)) and
                all(src[i] >= src[i + j] for j in range(1, right + 1))):
            result[i] = src[i]
    return result


def _pivot_low(src: list[float], left: int, right: int) -> list:
    result = [None] * len(src)
    for i in range(left, len(src) - right):
        if (all(src[i] <= src[i - j] for j in range(1, left + 1)) and
                all(src[i] <= src[i + j] for j in range(1, right + 1))):
            result[i] = src[i]
    return result


# ── Ana fonksiyon ────────────────────────────────────────────────────────────

def reversal_signals(
    highs: list[float],
    lows: list[float],
    closes: list[float],
    rsi_len: int = 7,
    rsi_mid: float = 50.0,
    ema_len: int = 200,
    rev_pivot_l: int = 3,
    rev_pivot_r: int = 3,
    adx_len: int = 14,
    adx_smoothing: int = 14,
    adx_min: float = 20.0,
    adx_fall_bars: int = 2,
    atr_len: int = 14,
    atr_spike_mult: float = 1.2,
    atr_spike_only_on_break: bool = True,
) -> dict:
    """
    Reversal sinyal dedektörü.

    LONG:  Fiyat son yapısal pivot HIGH'ı yukarı kırdı
           + EMA200 üstünde + RSI > mid + ADX > min ve düşüyor + ATR spike
    SHORT: Fiyat son yapısal pivot LOW'u aşağı kırdı
           + EMA200 altında + RSI < mid + ADX > min ve düşüyor + ATR spike

    Dönen yapı:
      signal_on_latest:              "LONG" | "SHORT" | "NONE"
      recent_long/short_signals:     Son 3 sinyal (kaç bar önce, fiyat, ADX, RSI)
      current_state:                 Mevcut filtre durumu — hangi koşullar hazır?
    """
    n = len(closes)

    rsi_vals = _rsi(closes, rsi_len)
    ema_vals = _ema(closes, ema_len)
    atr_vals = _atr_series(highs, lows, closes, atr_len)
    adx_vals, plus_di, minus_di = _adx_series(highs, lows, closes, adx_len, adx_smoothing)

    min_needed = ema_len + adx_len + adx_smoothing
    if not rsi_vals or not ema_vals or not atr_vals or not adx_vals:
        return {
            "error": f"Yetersiz veri — en az {min_needed} bar gerekli",
            "min_bars_required": min_needed,
        }

    # ATR SMA (atr_len period)
    atr_sma = _sma(atr_vals, atr_len)

    # Yapısal pivot serileri (reversal için ayrı prd)
    rev_ph = _pivot_high(highs, rev_pivot_l, rev_pivot_r)
    rev_pl = _pivot_low(lows, rev_pivot_l, rev_pivot_r)

    # lastRevPH / lastRevPL bar-by-bar simülasyonu
    lrph_series = [None] * n
    lrpl_series = [None] * n
    lrph = lrpl = None
    for i in range(n):
        if rev_ph[i] is not None:
            lrph = rev_ph[i]
        if rev_pl[i] is not None:
            lrpl = rev_pl[i]
        lrph_series[i] = lrph
        lrpl_series[i] = lrpl

    # İndikatörlerin uzunlukları (hepsi son bar = indeks -1 ile hizalı)
    adx_n   = len(adx_vals)    # en kısa → kısıtlayıcı
    rsi_off = n - len(rsi_vals)
    ema_off = n - len(ema_vals)
    atr_off = n - len(atr_vals)
    asm_off = n - len(atr_sma)

    long_signals  = []
    short_signals = []

    for k in range(adx_n):
        bar = n - adx_n + k
        if k < adx_fall_bars:
            continue

        # Hizalanmış değerler
        adx_k = adx_vals[k]
        rsi_k = rsi_vals[bar - rsi_off] if bar >= rsi_off else None
        ema_k = ema_vals[bar - ema_off] if bar >= ema_off else None
        atr_k = atr_vals[bar - atr_off] if bar >= atr_off else None
        asm_k = atr_sma[bar - asm_off] if bar >= asm_off and atr_sma else None

        if any(v is None for v in [rsi_k, ema_k, atr_k, asm_k]):
            continue

        # ADX düşüyor mu? (son adx_fall_bars bar boyunca)
        adx_falling = all(adx_vals[k - i] < adx_vals[k - i - 1] for i in range(adx_fall_bars))

        # ATR spike
        atr_spike = atr_k > asm_k * atr_spike_mult

        close_k  = closes[bar]
        lrph_k   = lrph_series[bar]
        lrpl_k   = lrpl_series[bar]
        break_up = lrph_k is not None and close_k > lrph_k
        break_dn = lrpl_k is not None and close_k < lrpl_k

        bear_filter = close_k < ema_k and rsi_k < rsi_mid and adx_k > adx_min and adx_falling
        bull_filter = close_k > ema_k and rsi_k > rsi_mid and adx_k > adx_min and adx_falling

        bear_atr_ok = (atr_spike if break_dn  else True) if atr_spike_only_on_break else atr_spike
        bull_atr_ok = (atr_spike if break_up else True) if atr_spike_only_on_break else atr_spike

        if break_dn and bear_filter and bear_atr_ok:
            short_signals.append({
                "bar_idx": bar,
                "bars_ago": n - 1 - bar,
                "price": round(close_k, 6),
                "broken_support": round(lrpl_k, 6),
                "rsi": round(rsi_k, 2),
                "adx": round(adx_k, 2),
                "atr_spike": atr_spike,
            })

        if break_up and bull_filter and bull_atr_ok:
            long_signals.append({
                "bar_idx": bar,
                "bars_ago": n - 1 - bar,
                "price": round(close_k, 6),
                "broken_resistance": round(lrph_k, 6),
                "rsi": round(rsi_k, 2),
                "adx": round(adx_k, 2),
                "atr_spike": atr_spike,
            })

    # Mevcut durum (son bar)
    latest_close = closes[-1]
    lat_rsi = rsi_vals[-1] if rsi_vals else None
    lat_ema = ema_vals[-1] if ema_vals else None
    lat_adx = adx_vals[-1] if adx_vals else None
    lat_pdi = plus_di[-1]  if plus_di  else None
    lat_mdi = minus_di[-1] if minus_di else None
    lat_atr = atr_vals[-1] if atr_vals else None
    lat_asm = atr_sma[-1]  if atr_sma  else None

    adx_falling_now = (
        all(adx_vals[-1 - i] < adx_vals[-2 - i] for i in range(adx_fall_bars))
        if len(adx_vals) > adx_fall_bars else False
    )
    atr_spike_now = lat_atr > lat_asm * atr_spike_mult if lat_atr and lat_asm else False
    break_up_now  = lrph_series[-1] is not None and latest_close > lrph_series[-1]
    break_dn_now  = lrpl_series[-1] is not None and latest_close < lrpl_series[-1]

    bull_f_now = bool(
        lat_ema and latest_close > lat_ema and
        lat_rsi and lat_rsi > rsi_mid and
        lat_adx and lat_adx > adx_min and
        adx_falling_now
    )
    bear_f_now = bool(
        lat_ema and latest_close < lat_ema and
        lat_rsi and lat_rsi < rsi_mid and
        lat_adx and lat_adx > adx_min and
        adx_falling_now
    )

    signal_now = "NONE"
    if long_signals  and long_signals[-1]["bars_ago"]  == 0:
        signal_now = "LONG"
    elif short_signals and short_signals[-1]["bars_ago"] == 0:
        signal_now = "SHORT"

    # Trend durumu (DI crossover)
    trend_state = "NEUTRAL"
    if lat_pdi and lat_mdi:
        trend_state = "POSITIVE" if lat_pdi > lat_mdi else "NEGATIVE"

    return {
        "signal_on_latest": signal_now,
        "latest_long_signal_bars_ago":  long_signals[-1]["bars_ago"]  if long_signals  else None,
        "latest_short_signal_bars_ago": short_signals[-1]["bars_ago"] if short_signals else None,
        "long_signals_total":  len(long_signals),
        "short_signals_total": len(short_signals),
        "recent_long_signals":  long_signals[-3:]  if long_signals  else [],
        "recent_short_signals": short_signals[-3:] if short_signals else [],
        "current_state": {
            "close": round(latest_close, 6),
            "ema200": round(lat_ema, 4) if lat_ema else None,
            "close_vs_ema200": "ABOVE" if lat_ema and latest_close > lat_ema else "BELOW",
            "rsi": round(lat_rsi, 2) if lat_rsi else None,
            "adx": round(lat_adx, 2) if lat_adx else None,
            "plus_di": round(lat_pdi, 2) if lat_pdi else None,
            "minus_di": round(lat_mdi, 2) if lat_mdi else None,
            "trend_direction": trend_state,
            "adx_falling": adx_falling_now,
            "atr": round(lat_atr, 4) if lat_atr else None,
            "natr_pct": round(lat_atr / latest_close * 100, 2) if lat_atr else None,
            "atr_spike": atr_spike_now,
            "last_pivot_high": round(lrph_series[-1], 4) if lrph_series[-1] else None,
            "last_pivot_low":  round(lrpl_series[-1], 4) if lrpl_series[-1] else None,
            "break_up": break_up_now,
            "break_down": break_dn_now,
            "bull_filter_ready": bull_f_now,
            "bear_filter_ready": bear_f_now,
            "setup_summary": (
                "LONG_READY"  if bull_f_now and break_up_now else
                "SHORT_READY" if bear_f_now and break_dn_now else
                "BULL_FILTER_MET" if bull_f_now else
                "BEAR_FILTER_MET" if bear_f_now else
                "NO_SETUP"
            ),
        },
    }


def natr_adx_dashboard(
    highs: list[float],
    lows: list[float],
    closes: list[float],
    atr_len: int = 14,
    atr_mult: float = 1.0,
    adx_len: int = 14,
    adx_smoothing: int = 14,
    adx_weak_thr: float = 20.0,
    adx_strong_thr: float = 25.0,
) -> dict:
    """
    ATR/ADX tablo değerleri: NATR%, ATR×çarpan, ADX gücü ve trend yönü.
    Pine Script'teki middle-right table'ın Python karşılığı.
    """
    atr_vals = _atr_series(highs, lows, closes, atr_len)
    adx_vals, plus_di, minus_di = _adx_series(highs, lows, closes, adx_len, adx_smoothing)

    if not atr_vals or not adx_vals:
        return {"error": "Yetersiz veri"}

    lat_atr = atr_vals[-1]
    lat_adx = adx_vals[-1]
    lat_pdi = plus_di[-1]  if plus_di  else None
    lat_mdi = minus_di[-1] if minus_di else None
    natr    = lat_atr / closes[-1] * 100

    # DI crossover ile trend durumu
    trend_state = "NEUTRAL"
    if len(plus_di) >= 2 and len(minus_di) >= 2:
        pos_cross = plus_di[-1] > minus_di[-1] and plus_di[-2] <= minus_di[-2]
        neg_cross = plus_di[-1] < minus_di[-1] and plus_di[-2] >= minus_di[-2]
        if pos_cross:
            trend_state = "POSITIVE"
        elif neg_cross:
            trend_state = "NEGATIVE"
        elif lat_pdi and lat_mdi:
            trend_state = "POSITIVE" if lat_pdi > lat_mdi else "NEGATIVE"

    adx_class = (
        "WEAK"   if lat_adx < adx_weak_thr   else
        "MEDIUM" if lat_adx < adx_strong_thr  else
        "STRONG"
    )

    return {
        "atr": round(lat_atr * atr_mult, 4),
        "natr_pct": round(natr, 2),
        "atr_len": atr_len,
        "adx": round(lat_adx, 2),
        "adx_len": adx_len,
        "adx_strength": adx_class,
        "plus_di": round(lat_pdi, 2) if lat_pdi else None,
        "minus_di": round(lat_mdi, 2) if lat_mdi else None,
        "trend_direction": trend_state,
        "trend_symbol": "▲ POS" if trend_state == "POSITIVE" else "▼ NEG" if trend_state == "NEGATIVE" else "■ NEU",
        "interpretation": (
            f"ATR={round(lat_atr*atr_mult,4)} (%{round(natr,2)} NATR) | "
            f"ADX={round(lat_adx,2)} [{adx_class}] | "
            f"Trend={trend_state}"
        ),
    }
