"""
Fon risk-getiri metrikleri: Sharpe, Sortino, Max Drawdown, Calmar, VaR.

Kullanım:
    python risk_getiri.py --data '[{"tarih":"2026-01-01","birim_fiyat":1.05},...]' --risksiz 0.40
"""
import json, math, argparse, sys


def gunluk_getiriler(fiyatlar: list[float]) -> list[float]:
    return [(fiyatlar[i] - fiyatlar[i - 1]) / fiyatlar[i - 1] for i in range(1, len(fiyatlar))]


def volatilite_yillik(getiriler: list[float]) -> float:
    n = len(getiriler)
    ort = sum(getiriler) / n
    varyans = sum((g - ort) ** 2 for g in getiriler) / n
    return math.sqrt(varyans) * math.sqrt(252)


def max_drawdown(fiyatlar: list[float]) -> tuple[float, int, int]:
    zirve = fiyatlar[0]
    zirve_idx = 0
    max_dd = 0.0
    dd_baslangic = 0
    dd_bitis = 0
    for i, f in enumerate(fiyatlar):
        if f > zirve:
            zirve = f
            zirve_idx = i
        dd = (f - zirve) / zirve
        if dd < max_dd:
            max_dd = dd
            dd_baslangic = zirve_idx
            dd_bitis = i
    return max_dd, dd_baslangic, dd_bitis


def sharpe(getiriler: list[float], risksiz_yillik: float) -> float:
    risksiz_gunluk = (1 + risksiz_yillik) ** (1 / 252) - 1
    fazla = [g - risksiz_gunluk for g in getiriler]
    ort = sum(fazla) / len(fazla)
    std = math.sqrt(sum((f - ort) ** 2 for f in fazla) / len(fazla))
    return (ort / std) * math.sqrt(252) if std != 0 else 0.0


def sortino(getiriler: list[float], risksiz_yillik: float) -> float:
    risksiz_gunluk = (1 + risksiz_yillik) ** (1 / 252) - 1
    fazla = [g - risksiz_gunluk for g in getiriler]
    ort = sum(fazla) / len(fazla)
    asagi = [min(g, 0) for g in fazla]
    asagi_std = math.sqrt(sum(a ** 2 for a in asagi) / len(asagi))
    return (ort / asagi_std) * math.sqrt(252) if asagi_std != 0 else 0.0


def var_tarihi(getiriler: list[float], guven: float = 0.95) -> float:
    sirali = sorted(getiriler)
    idx = int((1 - guven) * len(sirali))
    return sirali[idx]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True)
    parser.add_argument("--risksiz", type=float, default=0.40, help="Yıllık risksiz faiz (0.40 = %40)")
    args = parser.parse_args()

    try:
        veri = json.loads(args.data)
    except json.JSONDecodeError as e:
        print(json.dumps({"hata": str(e)}))
        sys.exit(1)

    fiyatlar = [d["birim_fiyat"] for d in veri]
    getiriler = gunluk_getiriler(fiyatlar)

    if len(getiriler) < 20:
        print(json.dumps({"hata": "Minimum 20 gün veri gerekli"}))
        sys.exit(1)

    toplam_getiri = (fiyatlar[-1] - fiyatlar[0]) / fiyatlar[0]
    gun = len(fiyatlar)
    yillik_getiri = (1 + toplam_getiri) ** (252 / gun) - 1

    dd, dd_bas, dd_bit = max_drawdown(fiyatlar)
    s = sharpe(getiriler, args.risksiz)
    so = sortino(getiriler, args.risksiz)
    calmar = yillik_getiri / abs(dd) if dd != 0 else 0.0
    v = var_tarihi(getiriler)
    vol = volatilite_yillik(getiriler)

    print(json.dumps({
        "toplam_getiri_yuzde": round(toplam_getiri * 100, 2),
        "yillik_getiri_yuzde": round(yillik_getiri * 100, 2),
        "volatilite_yillik_yuzde": round(vol * 100, 2),
        "sharpe": round(s, 3),
        "sortino": round(so, 3),
        "max_drawdown_yuzde": round(dd * 100, 2),
        "max_drawdown_baslangic_idx": dd_bas,
        "max_drawdown_bitis_idx": dd_bit,
        "calmar": round(calmar, 3),
        "var_95_gunluk_yuzde": round(v * 100, 2),
        "gun_sayisi": gun,
        "risksiz_faiz_yuzde": round(args.risksiz * 100, 1),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
