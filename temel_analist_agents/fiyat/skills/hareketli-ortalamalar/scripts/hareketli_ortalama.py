"""
EMA ve SMA hesaplayıcı.

Kullanım:
    python hareketli_ortalama.py --data '[{"tarih":"2026-01-01","kapanis":100.0},...]'
"""
import json, math, argparse, sys


def sma(fiyatlar: list[float], periyot: int) -> list[float | None]:
    sonuc = [None] * len(fiyatlar)
    for i in range(periyot - 1, len(fiyatlar)):
        sonuc[i] = sum(fiyatlar[i - periyot + 1:i + 1]) / periyot
    return sonuc


def ema(fiyatlar: list[float], periyot: int) -> list[float | None]:
    k = 2 / (periyot + 1)
    sonuc = [None] * len(fiyatlar)
    ilk_sma = sum(fiyatlar[:periyot]) / periyot
    sonuc[periyot - 1] = ilk_sma
    for i in range(periyot, len(fiyatlar)):
        sonuc[i] = fiyatlar[i] * k + sonuc[i - 1] * (1 - k)
    return sonuc


def egim_yuzde(dizi: list[float | None], gun: int = 5) -> float | None:
    gecerli = [x for x in dizi if x is not None]
    if len(gecerli) < gun + 1:
        return None
    return (gecerli[-1] - gecerli[-gun - 1]) / gecerli[-gun - 1] * 100


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True)
    args = parser.parse_args()

    try:
        veri = json.loads(args.data)
    except json.JSONDecodeError as e:
        print(json.dumps({"hata": str(e)}))
        sys.exit(1)

    fiyatlar = [d["kapanis"] for d in veri]
    son_fiyat = fiyatlar[-1]

    ema20 = ema(fiyatlar, 20)
    ema50 = ema(fiyatlar, 50)
    sma200 = sma(fiyatlar, 200)

    e20 = next((x for x in reversed(ema20) if x), None)
    e50 = next((x for x in reversed(ema50) if x), None)
    s200 = next((x for x in reversed(sma200) if x), None)

    def uzaklik(ho):
        return round((son_fiyat - ho) / ho * 100, 2) if ho else None

    dizilis = None
    if e20 and e50 and s200:
        if e20 > e50 > s200:
            dizilis = "BOĞA (EMA20 > EMA50 > SMA200)"
        elif e20 < e50 < s200:
            dizilis = "AYI (EMA20 < EMA50 < SMA200)"
        else:
            dizilis = "KARISIK"

    print(json.dumps({
        "son_fiyat": round(son_fiyat, 2),
        "EMA20": round(e20, 2) if e20 else None,
        "EMA50": round(e50, 2) if e50 else None,
        "SMA200": round(s200, 2) if s200 else None,
        "EMA20_uzaklik_yuzde": uzaklik(e20),
        "EMA50_uzaklik_yuzde": uzaklik(e50),
        "SMA200_uzaklik_yuzde": uzaklik(s200),
        "EMA20_egim_5g": round(egim_yuzde(ema20), 3) if egim_yuzde(ema20) else None,
        "EMA50_egim_5g": round(egim_yuzde(ema50), 3) if egim_yuzde(ema50) else None,
        "dizilis": dizilis,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
