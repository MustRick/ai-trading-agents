"""Portföy risk metrikleri: Günlük limit, Portfolio Heat, VaR, Max Drawdown"""

import math


def daily_loss_limit(
    portfolio_value: float,
    daily_risk_pct: float = 2.0,
    already_lost_today: float = 0.0,
) -> dict:
    """
    Günlük maksimum zarar limiti ve kalan risk bütçesi.
    Ana paranın günde en fazla ne kadar kaybedilebileceğini belirler.
    """
    max_loss = portfolio_value * daily_risk_pct / 100
    remaining_budget = max(0.0, max_loss - already_lost_today)
    used_pct = already_lost_today / max_loss * 100 if max_loss > 0 else 0

    status = (
        "LIMIT_BREACHED" if already_lost_today >= max_loss
        else "CRITICAL" if used_pct >= 80
        else "WARNING" if used_pct >= 50
        else "SAFE"
    )

    return {
        "portfolio_value": portfolio_value,
        "daily_risk_pct": daily_risk_pct,
        "max_daily_loss": round(max_loss, 2),
        "already_lost_today": round(already_lost_today, 2),
        "remaining_budget": round(remaining_budget, 2),
        "used_pct": round(used_pct, 1),
        "status": status,
        "action": (
            "STOP_TRADING_TODAY" if status == "LIMIT_BREACHED"
            else "NO_NEW_POSITIONS" if status == "CRITICAL"
            else "REDUCE_SIZE" if status == "WARNING"
            else "NORMAL"
        ),
    }


def portfolio_heat(
    portfolio_value: float,
    positions: list[dict],
    max_heat_pct: float = 6.0,
) -> dict:
    """
    Toplam portföy ısısı: tüm açık pozisyonların stop'a kadar olan toplam riski.
    positions: [{"symbol": str, "entry": float, "stop": float, "shares": float, "current": float}]
    max_heat_pct: portföyün maksimum kaçı riskle açık olabilir (varsayılan %6)
    """
    total_risk = 0.0
    total_pnl = 0.0
    details = []

    for pos in positions:
        open_risk = abs(pos["entry"] - pos["stop"]) * pos["shares"]
        unrealized_pnl = (pos["current"] - pos["entry"]) * pos["shares"]
        position_value = pos["current"] * pos["shares"]
        risk_pct = open_risk / portfolio_value * 100

        total_risk += open_risk
        total_pnl += unrealized_pnl

        details.append({
            "symbol": pos["symbol"],
            "open_risk": round(open_risk, 2),
            "open_risk_pct": round(risk_pct, 2),
            "position_value": round(position_value, 2),
            "unrealized_pnl": round(unrealized_pnl, 2),
            "at_risk": "YES" if unrealized_pnl < 0 else "PROTECTED",
        })

    heat_pct = total_risk / portfolio_value * 100
    capacity_remaining = max(0.0, max_heat_pct - heat_pct)

    return {
        "portfolio_value": portfolio_value,
        "total_open_risk": round(total_risk, 2),
        "heat_pct": round(heat_pct, 2),
        "max_heat_pct": max_heat_pct,
        "capacity_remaining_pct": round(capacity_remaining, 2),
        "total_unrealized_pnl": round(total_pnl, 2),
        "position_count": len(positions),
        "positions": details,
        "status": (
            "OVERHEATED" if heat_pct > max_heat_pct
            else "NEAR_LIMIT" if heat_pct > max_heat_pct * 0.8
            else "NORMAL"
        ),
        "new_position_allowed": heat_pct < max_heat_pct,
    }


def parametric_var(
    portfolio_value: float,
    daily_returns: list[float],
    confidence_level: float = 0.95,
) -> dict:
    """
    Parametrik VaR (Value at Risk) — normal dağılım varsayımıyla.
    daily_returns: günlük getiriler ondalıklı (0.01 = %1 kazanç, -0.02 = %2 kayıp)
    """
    if len(daily_returns) < 20:
        return {"error": "Güvenilir VaR için en az 20 günlük veri gerekli"}

    n = len(daily_returns)
    mean = sum(daily_returns) / n
    variance = sum((r - mean) ** 2 for r in daily_returns) / n
    std_dev = math.sqrt(variance)

    z_table = {0.90: 1.282, 0.95: 1.645, 0.99: 2.326}
    z = z_table.get(confidence_level, 1.645)

    var_pct = abs(mean - z * std_dev)
    var_tl = portfolio_value * var_pct
    cvar_pct = var_pct * 1.25  # basit CVaR tahmini

    return {
        "confidence_level": confidence_level,
        "var_pct": round(var_pct * 100, 2),
        "var_tl": round(var_tl, 2),
        "cvar_pct": round(cvar_pct * 100, 2),
        "mean_daily_return_pct": round(mean * 100, 3),
        "daily_volatility_pct": round(std_dev * 100, 2),
        "data_points": n,
        "interpretation": (
            f"%{int(confidence_level * 100)} güven düzeyinde "
            f"günlük maksimum kayıp: %{round(var_pct * 100, 2)} "
            f"({round(var_tl, 2):,.0f} TL)"
        ),
        "risk_level": (
            "HIGH" if var_pct > 0.03
            else "MEDIUM" if var_pct > 0.015
            else "LOW"
        ),
    }


def max_drawdown(equity_curve: list[float]) -> dict:
    """
    Equity eğrisindeki maksimum drawdown ve mevcut drawdown durumu.
    equity_curve: portföy değerlerinin zaman serisi
    """
    if len(equity_curve) < 2:
        return {"error": "En az 2 veri noktası gerekli"}

    peak = equity_curve[0]
    peak_idx = 0
    max_dd = 0.0
    trough_idx = 0

    for i, value in enumerate(equity_curve):
        if value > peak:
            peak = value
            peak_idx = i
        dd = (peak - value) / peak if peak > 0 else 0
        if dd > max_dd:
            max_dd = dd
            trough_idx = i

    current_peak = max(equity_curve)
    current_dd = (current_peak - equity_curve[-1]) / current_peak if current_peak > 0 else 0
    recovery_needed = (1 / (1 - max_dd) - 1) * 100 if max_dd < 1 else float("inf")

    return {
        "max_drawdown_pct": round(max_dd * 100, 2),
        "max_drawdown_tl": round(peak * max_dd, 2),
        "peak_value": round(peak, 2),
        "trough_value": round(equity_curve[trough_idx], 2),
        "current_drawdown_pct": round(current_dd * 100, 2),
        "current_value": round(equity_curve[-1], 2),
        "recovery_needed_pct": round(recovery_needed, 2),
        "status": (
            "SEVERE" if max_dd > 0.20
            else "MODERATE" if max_dd > 0.10
            else "MILD" if max_dd > 0.05
            else "NORMAL"
        ),
    }


def risk_reward_ratio(
    entry_price: float,
    stop_price: float,
    target_price: float,
    win_rate: float = 0.50,
) -> dict:
    """
    Risk/ödül oranı ve beklenen değer hesabı.
    win_rate: geçmiş veriye dayalı tahmini kazanma oranı (0-1)
    """
    risk = abs(entry_price - stop_price)
    reward = abs(target_price - entry_price)
    if risk == 0:
        return {"error": "Risk sıfır olamaz"}

    rr = reward / risk
    expected_value = win_rate * reward - (1 - win_rate) * risk
    ev_per_risk = expected_value / risk

    return {
        "risk": round(risk, 2),
        "reward": round(reward, 2),
        "ratio": round(rr, 2),
        "expected_value": round(expected_value, 2),
        "ev_per_risk_unit": round(ev_per_risk, 3),
        "rating": (
            "EXCELLENT" if rr >= 3.0
            else "GOOD" if rr >= 2.0
            else "ACCEPTABLE" if rr >= 1.5
            else "POOR"
        ),
        "positive_ev": expected_value > 0,
        "minimum_win_rate_to_breakeven": round(risk / (risk + reward) * 100, 1),
    }


def position_limit_check(
    portfolio_value: float,
    existing_positions: list[dict],
    new_position_value: float,
    max_positions: int = 10,
    max_single_pct: float = 10.0,
    max_sector_pct: float = 25.0,
    new_sector: str = "unknown",
) -> dict:
    """
    Yeni pozisyon açılabilir mi? Portföy kurallarını kontrol eder.
    existing_positions: [{"symbol": str, "value": float, "sector": str}]
    """
    checks = {}

    # Pozisyon sayısı limiti
    checks["position_count"] = {
        "current": len(existing_positions),
        "limit": max_positions,
        "passed": len(existing_positions) < max_positions,
    }

    # Tek hisse limiti
    new_pct = new_position_value / portfolio_value * 100
    checks["single_position_limit"] = {
        "requested_pct": round(new_pct, 2),
        "limit_pct": max_single_pct,
        "passed": new_pct <= max_single_pct,
    }

    # Sektör limiti
    sector_value = sum(
        p["value"] for p in existing_positions if p.get("sector") == new_sector
    )
    sector_pct = (sector_value + new_position_value) / portfolio_value * 100
    checks["sector_limit"] = {
        "sector": new_sector,
        "projected_sector_pct": round(sector_pct, 2),
        "limit_pct": max_sector_pct,
        "passed": sector_pct <= max_sector_pct,
    }

    all_passed = all(c["passed"] for c in checks.values())

    return {
        "approved": all_passed,
        "checks": checks,
        "action": "PROCEED" if all_passed else "BLOCKED",
        "blocking_rules": [k for k, v in checks.items() if not v["passed"]],
    }
