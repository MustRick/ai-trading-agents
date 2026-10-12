"""
Risk Management MCP Server — Sermaye koruma ve pozisyon yönetimi araç havuzu.
Cüzdan Agent'ın birincil tool kaynağıdır.
"""

from fastmcp import FastMCP
from calculators import (
    fixed_fractional, kelly_criterion, volatility_adjusted, max_allocation_check,
    calculate_atr, percentage_stop, atr_stop, chandelier_exit,
    support_resistance_stop, trailing_stop_update,
    daily_loss_limit, portfolio_heat, parametric_var,
    max_drawdown, risk_reward_ratio, position_limit_check,
)

mcp = FastMCP("risk-management")


# ─── POZİSYON BOYUTLAMA ──────────────────────────────────────────────────────

@mcp.tool()
def size_fixed_fractional(
    portfolio_value: float,
    risk_pct: float,
    entry_price: float,
    stop_price: float,
) -> dict:
    """
    Sabit kesir yöntemi ile pozisyon boyutu hesaplar.
    Portföyün risk_pct kadarını (örn: %1) riske at, stop mesafesine göre adet belirle.
    En güvenli ve yaygın kullanılan yöntemdir.
    """
    result = fixed_fractional(portfolio_value, risk_pct, entry_price, stop_price)
    result["method_name"] = "Fixed Fractional"
    result["summary"] = (
        f"{portfolio_value:,.0f} TL portföyde %{risk_pct} risk = "
        f"{result.get('risk_amount', 0):,.0f} TL riske atılır → "
        f"{result.get('shares', 0):.1f} adet "
        f"(%{result.get('pct_of_portfolio', 0):.1f} portföy ağırlığı)"
    )
    return result


@mcp.tool()
def size_kelly(
    win_rate: float,
    win_loss_ratio: float,
    portfolio_value: float,
    kelly_fraction: float = 0.25,
) -> dict:
    """
    Kelly Kriteri ile optimal pozisyon boyutu.
    win_rate: geçmiş kazanma oranı (0.55 = %55)
    win_loss_ratio: ort. kazanç / ort. kayıp (1.8 = kazanç 1.8x kayıptan büyük)
    kelly_fraction: güvenlik için 0.25 (quarter-Kelly) önerilir
    """
    result = kelly_criterion(win_rate, win_loss_ratio, portfolio_value, kelly_fraction)
    result["method_name"] = "Kelly Criterion"
    return result


@mcp.tool()
def size_volatility_adjusted(
    portfolio_value: float,
    risk_pct: float,
    highs: list[float],
    lows: list[float],
    closes: list[float],
    entry_price: float,
    atr_multiplier: float = 2.0,
) -> dict:
    """
    Volatilite bazlı pozisyon boyutu: ATR'yi stop mesafesi olarak kullanır.
    Yüksek volatilite → otomatik daha küçük pozisyon. En dinamik yöntemdir.
    """
    atr_data = calculate_atr(highs, lows, closes)
    if "error" in atr_data:
        return atr_data
    result = volatility_adjusted(portfolio_value, risk_pct, atr_data["atr"], entry_price, atr_multiplier)
    result["atr_data"] = atr_data
    result["method_name"] = "Volatility Adjusted"
    return result


@mcp.tool()
def check_max_allocation(
    portfolio_value: float,
    position_value: float,
    max_single_position_pct: float = 10.0,
) -> dict:
    """
    Tek bir hisseye ayrılan paranın portföy limitini aşıp aşmadığını kontrol eder.
    Onay verirse APPROVED, aşıyorsa ne kadar düşürülmesi gerektiğini söyler.
    """
    return max_allocation_check(portfolio_value, position_value, max_single_position_pct)


# ─── STOP LOSS ───────────────────────────────────────────────────────────────

@mcp.tool()
def stop_atr(
    highs: list[float],
    lows: list[float],
    closes: list[float],
    entry_price: float,
    atr_multiplier: float = 2.0,
    direction: str = "long",
) -> dict:
    """
    ATR bazlı stop loss seviyesi — volatiliteye göre dinamik, whipsaw'a karşı dayanıklı.
    Çarpan: agresif = 1.5, standart = 2.0, geniş = 3.0
    """
    atr_data = calculate_atr(highs, lows, closes)
    if "error" in atr_data:
        return atr_data
    result = atr_stop(entry_price, atr_data["atr"], atr_multiplier, direction)
    result["atr_info"] = atr_data
    return result


@mcp.tool()
def stop_percentage(
    entry_price: float,
    stop_pct: float,
    direction: str = "long",
) -> dict:
    """
    Yüzde tabanlı stop loss (örn: girişten %5 aşağısı).
    Hızlı hesaplama için kullanılır; ATR bazlı kadar dinamik değildir.
    """
    return percentage_stop(entry_price, stop_pct, direction)


@mcp.tool()
def stop_chandelier(
    highs: list[float],
    lows: list[float],
    closes: list[float],
    multiplier: float = 3.0,
    period: int = 22,
    direction: str = "long",
) -> dict:
    """
    Chandelier Exit — en güvenilir trailing stop yöntemi.
    Son N günün zirvesinden (long) ATR × çarpan mesafesinde stop tutar.
    """
    atr_data = calculate_atr(highs, lows, closes)
    if "error" in atr_data:
        return atr_data
    return chandelier_exit(highs, lows, atr_data["atr"], multiplier, period, direction)


@mcp.tool()
def stop_support_level(
    entry_price: float,
    support_level: float,
    buffer_pct: float = 0.5,
    direction: str = "long",
) -> dict:
    """
    Destek/direnç seviyesi bazlı stop — teknik analizle belirlenen seviyeleri kullanır.
    buffer_pct: desteğin kaç % ötesine yerleştirilsin (fakeout'tan korunmak için).
    """
    return support_resistance_stop(entry_price, support_level, buffer_pct, direction)


@mcp.tool()
def update_trailing_stop(
    current_price: float,
    current_stop: float,
    trail_pct: float,
    direction: str = "long",
) -> dict:
    """
    Trailing stop'u günceller. Fiyat lehimize hareket ettikçe stop da sürüklenir.
    Stop hiçbir zaman geriye gitmez — yalnızca kâr kilitler.
    """
    return trailing_stop_update(current_price, current_stop, trail_pct, direction)


# ─── PORTFÖY RİSK METRİKLERİ ─────────────────────────────────────────────────

@mcp.tool()
def check_daily_loss_limit(
    portfolio_value: float,
    daily_risk_pct: float = 2.0,
    already_lost_today: float = 0.0,
) -> dict:
    """
    Günlük maksimum zarar limiti kontrolü.
    Ana paranın günde en fazla kaybedebileceği miktarı ve kalan bütçeyi gösterir.
    daily_risk_pct: portföyün kaçı günlük limit (varsayılan %2)
    already_lost_today: bugün zaten kaybedilen miktar (TL)
    """
    return daily_loss_limit(portfolio_value, daily_risk_pct, already_lost_today)


@mcp.tool()
def check_portfolio_heat(
    portfolio_value: float,
    positions: list[dict],
    max_heat_pct: float = 6.0,
) -> dict:
    """
    Tüm açık pozisyonların toplam riskini (portföy ısısı) hesaplar.
    positions: [{"symbol": "XYZ", "entry": 100.0, "stop": 95.0, "shares": 100, "current": 102.0}]
    max_heat_pct: portföyde eş zamanlı açık tutulabilecek maksimum risk yüzdesi
    """
    return portfolio_heat(portfolio_value, positions, max_heat_pct)


@mcp.tool()
def calculate_var(
    portfolio_value: float,
    daily_returns: list[float],
    confidence_level: float = 0.95,
) -> dict:
    """
    Parametrik VaR (Value at Risk): belirli güven düzeyinde günlük maksimum beklenen kayıp.
    daily_returns: günlük getiriler ondalıklı (0.01 = %1, -0.02 = %-2)
    confidence_level: 0.90, 0.95 veya 0.99
    """
    return parametric_var(portfolio_value, daily_returns, confidence_level)


@mcp.tool()
def calculate_max_drawdown(equity_curve: list[float]) -> dict:
    """
    Portföy equity eğrisindeki maksimum drawdown ve mevcut drawdown durumu.
    equity_curve: portföy toplam değerinin tarihsel listesi
    """
    return max_drawdown(equity_curve)


@mcp.tool()
def evaluate_risk_reward(
    entry_price: float,
    stop_price: float,
    target_price: float,
    win_rate: float = 0.50,
) -> dict:
    """
    Risk/ödül oranı ve beklenen değer hesabı.
    Minimum öneri: R:R ≥ 2:1. R:R < 1.5 ise işleme girme.
    """
    return risk_reward_ratio(entry_price, stop_price, target_price, win_rate)


@mcp.tool()
def check_new_position_limits(
    portfolio_value: float,
    existing_positions: list[dict],
    new_position_value: float,
    max_positions: int = 10,
    max_single_pct: float = 10.0,
    max_sector_pct: float = 25.0,
    new_sector: str = "unknown",
) -> dict:
    """
    Yeni bir pozisyon portföy kurallarını ihlal ediyor mu?
    Pozisyon sayısı, tek hisse ve sektör limitlerini kontrol eder.
    existing_positions: [{"symbol": str, "value": float, "sector": str}]
    """
    return position_limit_check(
        portfolio_value, existing_positions, new_position_value,
        max_positions, max_single_pct, max_sector_pct, new_sector
    )


if __name__ == "__main__":
    mcp.run()
