"""
Technical Analysis MCP Server — FastMCP ile kurulmuş gösterge havuzu.
Tüm agentlar bu server'ı ortak tool kaynağı olarak kullanır.
"""

from fastmcp import FastMCP
from indicators import (
    rsi, stochastic, macd, roc, williams_r, cci,
    sma, ema, bollinger_bands, adx, parabolic_sar,
    obv, vwap, chaikin_money_flow, money_flow_index,
    support_resistance_zones, check_sr_breakout,
    mavilim_w, mavilim_w_classic,
    reversal_signals, natr_adx_dashboard,
)

mcp = FastMCP("technical-analysis")


# ─── MOMENTUM ────────────────────────────────────────────────────────────────

@mcp.tool()
def calculate_rsi(closes: list[float], period: int = 14) -> dict:
    """
    RSI (Relative Strength Index) hesaplar.
    Dönüş: {values: [...], overbought: 70, oversold: 30}
    Uzunluk: len(closes) - period
    """
    values = rsi(closes, period)
    return {
        "values": values,
        "latest": values[-1] if values else None,
        "overbought_threshold": 70,
        "oversold_threshold": 30,
        "signal": (
            "OVERBOUGHT" if values and values[-1] > 70
            else "OVERSOLD" if values and values[-1] < 30
            else "NEUTRAL"
        ),
    }


@mcp.tool()
def calculate_stochastic(
    highs: list[float],
    lows: list[float],
    closes: list[float],
    k_period: int = 14,
    d_period: int = 3,
) -> dict:
    """
    Stochastic Oscillator %K ve %D hesaplar.
    Dönüş: {k: [...], d: [...], signal: "OVERBOUGHT|OVERSOLD|NEUTRAL"}
    """
    result = stochastic(highs, lows, closes, k_period, d_period)
    latest_k = result["k"][-1] if result["k"] else None
    latest_d = result["d"][-1] if result["d"] else None
    signal = (
        "OVERBOUGHT" if latest_k and latest_k > 80
        else "OVERSOLD" if latest_k and latest_k < 20
        else "NEUTRAL"
    )
    return {**result, "latest_k": latest_k, "latest_d": latest_d, "signal": signal}


@mcp.tool()
def calculate_macd(
    closes: list[float],
    fast_period: int = 12,
    slow_period: int = 26,
    signal_period: int = 9,
) -> dict:
    """
    MACD, Signal ve Histogram hesaplar.
    Crossover tespiti için histogram'ın işaret değişimini kontrol et.
    """
    result = macd(closes, fast_period, slow_period, signal_period)
    hist = result["histogram"]
    signal = "NEUTRAL"
    if len(hist) >= 2:
        if hist[-2] < 0 and hist[-1] >= 0:
            signal = "BULLISH_CROSSOVER"
        elif hist[-2] > 0 and hist[-1] <= 0:
            signal = "BEARISH_CROSSOVER"
        elif hist[-1] > 0:
            signal = "BULLISH"
        else:
            signal = "BEARISH"
    return {
        "macd": result["macd"],
        "signal_line": result["signal"],
        "histogram": hist,
        "latest_macd": result["macd"][-1] if result["macd"] else None,
        "latest_signal": result["signal"][-1] if result["signal"] else None,
        "latest_histogram": hist[-1] if hist else None,
        "signal": signal,
    }


@mcp.tool()
def calculate_roc(closes: list[float], period: int = 12) -> dict:
    """
    Rate of Change — fiyat momentum hızını ölçer.
    Dönüş: {values: [...], latest: float, signal: "POSITIVE|NEGATIVE"}
    """
    values = roc(closes, period)
    return {
        "values": values,
        "latest": values[-1] if values else None,
        "signal": "POSITIVE" if values and values[-1] > 0 else "NEGATIVE",
    }


@mcp.tool()
def calculate_williams_r(
    highs: list[float],
    lows: list[float],
    closes: list[float],
    period: int = 14,
) -> dict:
    """
    Williams %R — aşırı alım/satım bölgelerini gösterir (-100 ile 0 arası).
    Aşırı alım: > -20 | Aşırı satım: < -80
    """
    values = williams_r(highs, lows, closes, period)
    latest = values[-1] if values else None
    return {
        "values": values,
        "latest": latest,
        "signal": (
            "OVERBOUGHT" if latest and latest > -20
            else "OVERSOLD" if latest and latest < -80
            else "NEUTRAL"
        ),
    }


@mcp.tool()
def calculate_cci(
    highs: list[float],
    lows: list[float],
    closes: list[float],
    period: int = 20,
) -> dict:
    """
    CCI (Commodity Channel Index).
    Aşırı alım: > +100 | Aşırı satım: < -100
    """
    values = cci(highs, lows, closes, period)
    latest = values[-1] if values else None
    return {
        "values": values,
        "latest": latest,
        "signal": (
            "OVERBOUGHT" if latest and latest > 100
            else "OVERSOLD" if latest and latest < -100
            else "NEUTRAL"
        ),
    }


# ─── TREND ───────────────────────────────────────────────────────────────────

@mcp.tool()
def calculate_sma(closes: list[float], period: int = 20) -> dict:
    """Basit Hareketli Ortalama (SMA) hesaplar."""
    values = sma(closes, period)
    return {
        "values": values,
        "latest": values[-1] if values else None,
        "price_vs_sma": (
            "ABOVE" if values and closes[-1] > values[-1]
            else "BELOW" if values and closes[-1] < values[-1]
            else "AT"
        ),
    }


@mcp.tool()
def calculate_ema(closes: list[float], period: int = 20) -> dict:
    """Üstel Hareketli Ortalama (EMA) hesaplar."""
    values = ema(closes, period)
    return {
        "values": values,
        "latest": values[-1] if values else None,
        "price_vs_ema": (
            "ABOVE" if values and closes[-1] > values[-1]
            else "BELOW" if values and closes[-1] < values[-1]
            else "AT"
        ),
    }


@mcp.tool()
def calculate_ema_crossover(
    closes: list[float],
    fast_period: int = 9,
    slow_period: int = 21,
) -> dict:
    """
    İki EMA arasındaki crossover'ı tespit eder.
    Dönüş: {fast_ema, slow_ema, signal: "GOLDEN_CROSS|DEATH_CROSS|BULLISH|BEARISH"}
    """
    fast = ema(closes, fast_period)
    slow = ema(closes, slow_period)
    offset = len(fast) - len(slow)
    aligned_fast = fast[offset:]

    signal = "NEUTRAL"
    if len(aligned_fast) >= 2 and len(slow) >= 2:
        prev_diff = aligned_fast[-2] - slow[-2]
        curr_diff = aligned_fast[-1] - slow[-1]
        if prev_diff <= 0 and curr_diff > 0:
            signal = "GOLDEN_CROSS"
        elif prev_diff >= 0 and curr_diff < 0:
            signal = "DEATH_CROSS"
        elif curr_diff > 0:
            signal = "BULLISH"
        else:
            signal = "BEARISH"

    return {
        "fast_ema": fast,
        "slow_ema": slow,
        "latest_fast": fast[-1] if fast else None,
        "latest_slow": slow[-1] if slow else None,
        "signal": signal,
    }


@mcp.tool()
def calculate_bollinger_bands(
    closes: list[float],
    period: int = 20,
    std_multiplier: float = 2.0,
) -> dict:
    """
    Bollinger Bands hesaplar.
    Dönüş: {upper, middle, lower, bandwidth, percent_b, signal}
    """
    bands = bollinger_bands(closes, period, std_multiplier)
    upper = bands["upper"]
    middle = bands["middle"]
    lower = bands["lower"]

    latest_close = closes[-1]
    latest_upper = upper[-1] if upper else None
    latest_lower = lower[-1] if lower else None
    latest_middle = middle[-1] if middle else None

    bandwidth = (
        (latest_upper - latest_lower) / latest_middle * 100
        if latest_upper and latest_lower and latest_middle
        else None
    )
    percent_b = (
        (latest_close - latest_lower) / (latest_upper - latest_lower)
        if latest_upper and latest_lower and (latest_upper - latest_lower) != 0
        else None
    )
    signal = (
        "UPPER_TOUCH" if percent_b and percent_b >= 1.0
        else "LOWER_TOUCH" if percent_b and percent_b <= 0.0
        else "SQUEEZE" if bandwidth and bandwidth < 5.0
        else "NEUTRAL"
    )

    return {
        "upper": upper,
        "middle": middle,
        "lower": lower,
        "latest_upper": latest_upper,
        "latest_middle": latest_middle,
        "latest_lower": latest_lower,
        "bandwidth": bandwidth,
        "percent_b": percent_b,
        "signal": signal,
    }


@mcp.tool()
def calculate_adx(
    highs: list[float],
    lows: list[float],
    closes: list[float],
    period: int = 14,
) -> dict:
    """
    ADX (Average Directional Index) — trend gücünü ölçer.
    ADX > 25: güçlü trend | ADX < 20: yatay piyasa
    """
    result = adx(highs, lows, closes, period)
    adx_vals = result["adx"]
    plus = result["plus_di"]
    minus = result["minus_di"]
    latest_adx = adx_vals[-1] if adx_vals else None
    trend_strength = (
        "STRONG_TREND" if latest_adx and latest_adx > 25
        else "WEAK_TREND" if latest_adx and latest_adx > 20
        else "NO_TREND"
    )
    direction = (
        "BULLISH" if plus and minus and plus[-1] > minus[-1]
        else "BEARISH"
    )
    return {
        "adx": adx_vals,
        "plus_di": plus,
        "minus_di": minus,
        "latest_adx": latest_adx,
        "latest_plus_di": plus[-1] if plus else None,
        "latest_minus_di": minus[-1] if minus else None,
        "trend_strength": trend_strength,
        "direction": direction,
    }


@mcp.tool()
def calculate_parabolic_sar(
    highs: list[float],
    lows: list[float],
    af_step: float = 0.02,
    af_max: float = 0.2,
) -> dict:
    """
    Parabolic SAR — trailing stop ve trend yönü için.
    Fiyat SAR'ın üstündeyse uptrend, altındaysa downtrend.
    """
    values = parabolic_sar(highs, lows, af_step, af_max)
    closes_last = (highs[-1] + lows[-1]) / 2
    latest_sar = values[-1] if values else None
    return {
        "values": values,
        "latest_sar": latest_sar,
        "signal": "UPTREND" if latest_sar and closes_last > latest_sar else "DOWNTREND",
    }


# ─── VOLUME ──────────────────────────────────────────────────────────────────

@mcp.tool()
def calculate_obv(closes: list[float], volumes: list[float]) -> dict:
    """
    OBV (On Balance Volume) — hacim akışının yönünü gösterir.
    OBV fiyatla uyumlu değilse divergence sinyali.
    """
    values = obv(closes, volumes)
    trend = "NEUTRAL"
    if len(values) >= 10:
        if values[-1] > values[-10]:
            trend = "ACCUMULATION"
        elif values[-1] < values[-10]:
            trend = "DISTRIBUTION"
    return {"values": values, "latest": values[-1] if values else None, "trend": trend}


@mcp.tool()
def calculate_vwap(
    highs: list[float],
    lows: list[float],
    closes: list[float],
    volumes: list[float],
) -> dict:
    """
    VWAP (Volume Weighted Average Price) — adil değer referansı.
    Kurumsal alımlar genellikle VWAP civarında gerçekleşir.
    """
    values = vwap(highs, lows, closes, volumes)
    latest_vwap = values[-1] if values else None
    return {
        "values": values,
        "latest_vwap": latest_vwap,
        "price_vs_vwap": (
            "ABOVE" if latest_vwap and closes[-1] > latest_vwap
            else "BELOW" if latest_vwap and closes[-1] < latest_vwap
            else "AT"
        ),
    }


@mcp.tool()
def calculate_cmf(
    highs: list[float],
    lows: list[float],
    closes: list[float],
    volumes: list[float],
    period: int = 20,
) -> dict:
    """
    Chaikin Money Flow — para akışı yönünü ölçer.
    CMF > 0: alım baskısı | CMF < 0: satış baskısı
    """
    values = chaikin_money_flow(highs, lows, closes, volumes, period)
    latest = values[-1] if values else None
    return {
        "values": values,
        "latest": latest,
        "signal": (
            "BUYING_PRESSURE" if latest and latest > 0.1
            else "SELLING_PRESSURE" if latest and latest < -0.1
            else "NEUTRAL"
        ),
    }


@mcp.tool()
def calculate_mfi(
    highs: list[float],
    lows: list[float],
    closes: list[float],
    volumes: list[float],
    period: int = 14,
) -> dict:
    """
    MFI (Money Flow Index) — hacim ağırlıklı RSI.
    Aşırı alım: > 80 | Aşırı satım: < 20
    """
    values = money_flow_index(highs, lows, closes, volumes, period)
    latest = values[-1] if values else None
    return {
        "values": values,
        "latest": latest,
        "signal": (
            "OVERBOUGHT" if latest and latest > 80
            else "OVERSOLD" if latest and latest < 20
            else "NEUTRAL"
        ),
    }


# ─── DESTEK / DİRENÇ BÖLGELERİ (SRv2) ──────────────────────────────────────

@mcp.tool()
def calculate_sr_zones(
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
    SRv2: Pivot noktaları kümeleyerek Destek/Direnç bölgelerini hesaplar.
    Her bölge için: orta fiyat, üst/alt sınır, güç (kaç pivot), mesafe %.
    prd: pivot tespiti için sol/sağ bar sayısı (4-30)
    channel_width_pct: kümeleme tolerans genişliği (fiyat aralığının %kaçı)
    maxnumsr: kaç bölge dönsün (en güçlü N)
    min_strength: minimum kaç pivot içermeli
    """
    zones = support_resistance_zones(
        highs, lows, closes, prd, maxnumpp, channel_width_pct, maxnumsr, min_strength
    )
    latest = closes[-1]
    nearest_resistance = next((z for z in zones if z["type"] == "RESISTANCE"), None)
    nearest_support    = next((z for z in zones if z["type"] == "SUPPORT"), None)
    return {
        "zones": zones,
        "zone_count": len(zones),
        "nearest_resistance": nearest_resistance,
        "nearest_support": nearest_support,
        "current_price": latest,
        "summary": (
            f"{len(zones)} S/R bölgesi | "
            f"En yakın direnç: "
            f"{round(nearest_resistance['mid'], 4)} ({nearest_resistance['distance_pct']}%)"
            if nearest_resistance else "direnç yok"
        ) + " | " + (
            f"En yakın destek: "
            f"{round(nearest_support['mid'], 4)} ({nearest_support['distance_pct']}%)"
            if nearest_support else "destek yok"
        ) if zones else "S/R bölgesi bulunamadı (yetersiz pivot)",
    }


@mcp.tool()
def check_sr_level_break(
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
    Son kapanışın bir S/R bölgesini kırıp kırmadığını kontrol eder.
    crossed_over = True: Direnç kırıldı (bullish kırılım)
    crossed_under = True: Destek kırıldı (bearish kırılım)
    Pine Script crossed_over / crossed_under mantığının Python karşılığı.
    """
    result = check_sr_breakout(
        highs, lows, closes, prd, maxnumpp, channel_width_pct, maxnumsr, min_strength
    )
    signal = (
        "RESISTANCE_BROKEN" if result["crossed_over"] else
        "SUPPORT_BROKEN"    if result["crossed_under"] else
        "NO_BREAK"
    )
    return {**result, "signal": signal}


# ─── MAVİLİMW ────────────────────────────────────────────────────────────────

@mcp.tool()
def calculate_mavilim_w(
    closes: list[float],
    fmal: int = 3,
    smal: int = 5,
) -> dict:
    """
    MavilimW: Kivanç Özbilgiç'in çok katmanlı WMA cascade göstergesi.
    6 kademe WMA uygular: fmal → smal → (fmal+smal) → ... → toplam uzunluk.
    Mavi/yukarı = bullish, Kırmızı/aşağı = bearish.
    BUY sinyal: trend yönü düşüşten yükselişe döndü.
    SELL sinyal: trend yönü yükselişten düşüşe döndü.
    Varsayılan fmal=3, smal=5 → toplam Fibonacci dizisi: 3-5-8-13-21-34
    """
    result = mavilim_w(closes, fmal, smal)
    if "error" in result:
        return result
    return {
        "latest_mavw": result["latest"],
        "previous_mavw": result["previous"],
        "signal": result["signal"],
        "buy_signal": result["buy_signal"],
        "sell_signal": result["sell_signal"],
        "trend_slope": result["trend_slope"],
        "lengths": result["lengths_used"],
        "alert": (
            "🔵 MAVW BUY — trend düşüşten yükselişe döndü"  if result["buy_signal"]  else
            "🔴 MAVW SELL — trend yükselişten düşüşe döndü" if result["sell_signal"] else
            None
        ),
    }


# ─── REVERSAL SİNYALLERİ ─────────────────────────────────────────────────────

@mcp.tool()
def calculate_reversal_signals(
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
    Reversal sinyal dedektörü — Pine Script Reversal bölümünün tam Python karşılığı.

    LONG  (REV↑): Yapısal pivot HIGH kırıldı + EMA200 üstü + RSI>mid + ADX düşüyor + ATR spike
    SHORT (REV↓): Yapısal pivot LOW  kırıldı + EMA200 altı + RSI<mid + ADX düşüyor + ATR spike

    current_state.setup_summary:
      LONG_READY   → tüm filtreler uyumlu, kırılım gerçekleşti
      SHORT_READY  → tüm filtreler uyumlu, kırılım gerçekleşti
      BULL_FILTER_MET → koşullar hazır, kırılım bekleniyor
      BEAR_FILTER_MET → koşullar hazır, kırılım bekleniyor
      NO_SETUP     → henüz koşul yok
    """
    return reversal_signals(
        highs, lows, closes,
        rsi_len, rsi_mid, ema_len,
        rev_pivot_l, rev_pivot_r,
        adx_len, adx_smoothing, adx_min, adx_fall_bars,
        atr_len, atr_spike_mult, atr_spike_only_on_break,
    )


@mcp.tool()
def calculate_natr_adx_dashboard(
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
    ATR/ADX özet tablosu: Pine Script'teki middle-right table'ın Python karşılığı.
    ATR değeri, NATR% (normalize), ADX gücü (WEAK/MEDIUM/STRONG), trend yönü (▲/▼/■).
    adx_weak_thr: bu değerin altı = zayıf trend
    adx_strong_thr: bu değerin üstü = güçlü trend
    """
    return natr_adx_dashboard(
        highs, lows, closes,
        atr_len, atr_mult, adx_len, adx_smoothing,
        adx_weak_thr, adx_strong_thr,
    )


if __name__ == "__main__":
    mcp.run()
