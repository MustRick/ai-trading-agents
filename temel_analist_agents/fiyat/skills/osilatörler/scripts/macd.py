"""
MACD hesaplayıcı (12, 26, 9).

Kullanım:
    python macd.py --data '[{"tarih":"2026-01-01","kapanis":100.0},...]'
"""
import json, argparse, sys


def ema(fiyatlar: list[float], periyot: int) -> list[float | None]:
    k = 2 / (periyot + 1)
    sonuc = [None] * len(fiyatlar)
    if len(fiyatlar) < periyot:
        return sonuc
    sonuc[periyot - 1] = sum(fiyatlar[:periyot]) / periyot
    for i in range(periyot, len(fiyatlar)):
        sonuc[i] = fiyatlar[i] * k + sonuc[i - 1] * (1 - k)
    return sonuc


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True)
    parser.add_argument("--hizli", type=int, default=12)
    parser.add_argument("--yavas", type=int, default=26)
    parser.add_argument("--sinyal", type=int, default=9)
    args = parser.parse_args()

    try:
        veri = json.loads(args.data)
    except json.JSONDecodeError as e:
        print(json.dumps({"hata": str(e)}))
        sys.exit(1)

    fiyatlar = [d["kapanis"] for d in veri]
    ema_h = ema(fiyatlar, args.hizli)
    ema_y = ema(fiyatlar, args.yavas)

    macd_dizi = [
        (h - y) if h is not None and y is not None else None
        for h, y in zip(ema_h, ema_y)
    ]

    gecerli_macd = [m for m in macd_dizi if m is not None]
    if len(gecerli_macd) < args.sinyal:
        print(json.dumps({"hata": "Yetersiz veri"}))
        sys.exit(1)

    sinyal_dizi = ema(gecerli_macd, args.sinyal)
    son_macd = gecerli_macd[-1]
    son_sinyal = next((s for s in reversed(sinyal_dizi) if s is not None), None)
    histogram = son_macd - son_sinyal if son_sinyal else None

    onceki_macd = gecerli_macd[-2] if len(gecerli_macd) >= 2 else None
    onceki_sinyal_idx = len([s for s in sinyal_dizi if s is not None]) - 2
    onceki_sinyal = ([s for s in sinyal_dizi if s is not None][onceki_sinyal_idx]
                     if onceki_sinyal_idx >= 0 else None)

    kesisim = None
    if onceki_macd is not None and onceki_sinyal is not None and son_sinyal is not None:
        if onceki_macd < onceki_sinyal and son_macd > son_sinyal:
            kesisim = "YUKARI KESİŞİM — Pozitif sinyal"
        elif onceki_macd > onceki_sinyal and son_macd < son_sinyal:
            kesisim = "AŞAĞI KESİŞİM — Negatif sinyal"

    print(json.dumps({
        "macd": round(son_macd, 4),
        "sinyal": round(son_sinyal, 4) if son_sinyal else None,
        "histogram": round(histogram, 4) if histogram else None,
        "momentum": "Pozitif" if son_macd > 0 else "Negatif",
        "macd_vs_sinyal": "MACD > Sinyal" if son_sinyal and son_macd > son_sinyal else "MACD < Sinyal",
        "kesisim": kesisim,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
