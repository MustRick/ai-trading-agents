"""
Destek/Direnç Bölgeleri — Pine Script SRv2 adaptasyonu.
Pivot noktalarını kümeleyerek S/R bölgeleri oluşturur.
Kaynak: LonesomeTheBlue — MPL 2.0
"""


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


def _get_sr_vals(pivot_vals: list, ind: int, cwidth: float):
    lo = pivot_vals[ind]
    hi = lo
    numpp = 0
    for y in range(len(pivot_vals)):
        cpp = pivot_vals[y]
        wdth = (hi - cpp) if cpp <= lo else (cpp - lo)
        if wdth <= cwidth:
            if cpp <= hi:
                lo = min(lo, cpp)
            else:
                hi = max(hi, cpp)
            numpp += 1
    return hi, lo, numpp


def _find_loc(sr_strength: list, strength: int) -> int:
    # S/R listesi azalan güç sırasında tutulur (güçlü başta)
    ret = len(sr_strength)
    for j in range(len(sr_strength)):
        i = len(sr_strength) - 1 - j
        if strength <= sr_strength[i]:
            break
        ret = i
    return ret


def _check_sr(
    sr_up: list, sr_dn: list, sr_str: list,
    hi: float, lo: float, strength: int,
) -> bool:
    for i in range(len(sr_up)):
        overlaps = (
            (sr_up[i] >= lo and sr_up[i] <= hi) or
            (sr_dn[i] >= lo and sr_dn[i] <= hi)
        )
        if overlaps:
            if strength >= sr_str[i]:
                sr_str.pop(i); sr_up.pop(i); sr_dn.pop(i)
            else:
                return False
            break
    return True


def support_resistance_zones(
    highs: list[float],
    lows: list[float],
    closes: list[float],
    prd: int = 10,
    maxnumpp: int = 20,
    channel_width_pct: int = 10,
    maxnumsr: int = 5,
    min_strength: int = 2,
) -> list[dict]:
    """
    SRv2 algoritması: pivot noktaları channel_width_pct toleransıyla kümelenir.
    Her S/R bölgesi için güç (kaç pivot içeriyor), orta nokta, üst/alt sınır döner.

    Dönen liste yakından uzağa sıralıdır.
    """
    n = len(closes)
    if n < prd * 2 + 1:
        return []

    ph = _pivot_high(highs, prd, prd)
    pl = _pivot_low(lows, prd, prd)

    lookback = min(300, n)
    cwidth = (max(highs[-lookback:]) - min(lows[-lookback:])) * channel_width_pct / 100

    pivot_vals: list[float] = []
    sr_up: list[float] = []
    sr_dn: list[float] = []
    sr_str: list[int] = []

    for bar in range(n):
        new_pivot = ph[bar] if ph[bar] is not None else (pl[bar] if pl[bar] is not None else None)
        if new_pivot is None:
            continue

        pivot_vals.insert(0, new_pivot)
        if len(pivot_vals) > maxnumpp:
            pivot_vals.pop()

        sr_up.clear(); sr_dn.clear(); sr_str.clear()
        for x in range(len(pivot_vals)):
            hi, lo, strength = _get_sr_vals(pivot_vals, x, cwidth)
            if _check_sr(sr_up, sr_dn, sr_str, hi, lo, strength):
                loc = _find_loc(sr_str, strength)
                if loc < maxnumsr and strength >= min_strength:
                    sr_str.insert(loc, strength)
                    sr_up.insert(loc, hi)
                    sr_dn.insert(loc, lo)
                    if len(sr_str) > maxnumsr:
                        sr_str.pop(); sr_up.pop(); sr_dn.pop()

    latest_close = closes[-1]
    zones = []
    for i in range(len(sr_up)):
        mid = (sr_up[i] + sr_dn[i]) / 2
        dist_pct = (mid - latest_close) / latest_close * 100
        zones.append({
            "mid": round(mid, 6),
            "hi": round(sr_up[i], 6),
            "lo": round(sr_dn[i], 6),
            "strength": sr_str[i],
            "type": "RESISTANCE" if mid >= latest_close else "SUPPORT",
            "distance_pct": round(dist_pct, 2),
        })

    zones.sort(key=lambda z: abs(z["distance_pct"]))
    return zones


def check_sr_breakout(
    highs: list[float],
    lows: list[float],
    closes: list[float],
    prd: int = 10,
    maxnumpp: int = 20,
    channel_width_pct: int = 10,
    maxnumsr: int = 5,
    min_strength: int = 2,
) -> dict:
    """
    Son kapanışın herhangi bir S/R bölgesini kırıp kırmadığını kontrol eder.
    Pine Script'in crossed_over / crossed_under mantığının Python karşılığı.
    """
    if len(closes) < 2:
        return {"crossed_over": False, "crossed_under": False, "zones": []}

    zones = support_resistance_zones(
        highs, lows, closes, prd, maxnumpp, channel_width_pct, maxnumsr, min_strength
    )
    prev_close = closes[-2]
    curr_close = closes[-1]

    crossed_over = any(prev_close <= z["mid"] < curr_close for z in zones)
    crossed_under = any(prev_close >= z["mid"] > curr_close for z in zones)

    broken_zones = []
    for z in zones:
        if prev_close <= z["mid"] < curr_close:
            broken_zones.append({**z, "break": "RESISTANCE_BROKEN"})
        elif prev_close >= z["mid"] > curr_close:
            broken_zones.append({**z, "break": "SUPPORT_BROKEN"})

    return {
        "crossed_over": crossed_over,
        "crossed_under": crossed_under,
        "broken_zones": broken_zones,
        "all_zones": zones,
    }
