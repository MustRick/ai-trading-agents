"""Pozisyon boyutu hesaplayıcılar: Fixed Fractional, Kelly, Volatilite Bazlı"""

import math


def fixed_fractional(
    portfolio_value: float,
    risk_pct: float,
    entry_price: float,
    stop_price: float,
) -> dict:
    """
    Sabit kesir yöntemi: portföyün risk_pct kadarını riske at.
    En yaygın ve güvenli pozisyon boyutlama yöntemidir.
    """
    risk_amount = portfolio_value * risk_pct / 100
    stop_distance = abs(entry_price - stop_price)
    if stop_distance == 0:
        return {"error": "Stop mesafesi sıfır olamaz — önce stop seviyesi belirle"}

    shares = risk_amount / stop_distance
    position_value = shares * entry_price
    pct_of_portfolio = position_value / portfolio_value * 100

    return {
        "shares": round(shares, 2),
        "position_value": round(position_value, 2),
        "pct_of_portfolio": round(pct_of_portfolio, 2),
        "risk_amount": round(risk_amount, 2),
        "risk_pct": risk_pct,
        "stop_distance": round(stop_distance, 2),
        "warning": "OVERSIZED" if pct_of_portfolio > 15 else None,
    }


def kelly_criterion(
    win_rate: float,
    win_loss_ratio: float,
    portfolio_value: float,
    kelly_fraction: float = 0.25,
) -> dict:
    """
    Kelly Kriteri: istatistiksel edge'e göre optimal boyut.
    kelly_fraction: güvenlik için tam Kelly'nin kaçta biri kullanılacak (varsayılan: 1/4)
    win_rate: kazanma oranı 0-1 arası (örn: 0.55)
    win_loss_ratio: ort. kazanç / ort. kayıp oranı (örn: 1.8)
    """
    if win_loss_ratio <= 0:
        return {"error": "Win/Loss oranı pozitif olmalı"}

    full_kelly = win_rate - (1 - win_rate) / win_loss_ratio
    full_kelly = max(0.0, full_kelly)
    adjusted_kelly = full_kelly * kelly_fraction
    adjusted_kelly = min(adjusted_kelly, 0.20)  # maksimum %20 koruma

    position_value = portfolio_value * adjusted_kelly
    expected_value = win_rate * win_loss_ratio - (1 - win_rate)

    return {
        "full_kelly_pct": round(full_kelly * 100, 2),
        "adjusted_kelly_pct": round(adjusted_kelly * 100, 2),
        "position_value": round(position_value, 2),
        "expected_value_per_risk": round(expected_value, 3),
        "edge": "POSITIVE" if expected_value > 0 else "NEGATIVE",
        "note": f"Tam Kelly'nin {int(kelly_fraction * 100)}%'i kullanıldı",
    }


def volatility_adjusted(
    portfolio_value: float,
    risk_pct: float,
    atr: float,
    entry_price: float,
    atr_multiplier: float = 2.0,
) -> dict:
    """
    Volatilite bazlı boyutlama: ATR stop mesafesini kullanır.
    Yüksek volatiliteli hisselere otomatik olarak daha az para ayrılır.
    """
    if atr <= 0:
        return {"error": "ATR pozitif olmalı"}

    risk_amount = portfolio_value * risk_pct / 100
    stop_distance = atr * atr_multiplier
    stop_price = entry_price - stop_distance
    shares = risk_amount / stop_distance
    position_value = shares * entry_price
    pct_of_portfolio = position_value / portfolio_value * 100
    atr_pct = atr / entry_price * 100

    return {
        "shares": round(shares, 2),
        "position_value": round(position_value, 2),
        "pct_of_portfolio": round(pct_of_portfolio, 2),
        "atr_stop_price": round(stop_price, 2),
        "stop_distance": round(stop_distance, 2),
        "atr": round(atr, 2),
        "atr_pct_of_price": round(atr_pct, 2),
        "risk_amount": round(risk_amount, 2),
        "volatility_class": (
            "HIGH" if atr_pct > 3 else "MEDIUM" if atr_pct > 1.5 else "LOW"
        ),
    }


def max_allocation_check(
    portfolio_value: float,
    position_value: float,
    max_single_position_pct: float = 10.0,
) -> dict:
    """
    Tek hisseye ayrılan paranın portföy limitini aşıp aşmadığını kontrol eder.
    Varsayılan: tek hisse maksimum %10 portföy ağırlığı.
    """
    actual_pct = position_value / portfolio_value * 100
    within_limit = actual_pct <= max_single_position_pct
    adjusted_value = portfolio_value * max_single_position_pct / 100

    return {
        "requested_value": round(position_value, 2),
        "requested_pct": round(actual_pct, 2),
        "max_allowed_pct": max_single_position_pct,
        "max_allowed_value": round(adjusted_value, 2),
        "within_limit": within_limit,
        "action": "APPROVED" if within_limit else "REDUCE_TO_LIMIT",
        "reduction_needed": round(position_value - adjusted_value, 2) if not within_limit else 0,
    }
