"""
Bollinger Bantları, %B ve Squeeze tespiti.

Kullanım:
    python bollinger.py --data '[{"tarih":"2026-01-01","kapanis":100.0},...]'
"""
import json, math, argparse, sys


def bollinger(fiyatlar: list[float], periyot: int = 20, carpan: float = 2.0):
    sonuclar = []
    for i in range(len(fiyatlar)):
        if i < periyot - 1:
            sonuclar.append(None)
            continue
        pencere = fiyatlar[i - periyot + 1:i + 1]
        ort = sum(pencere) / periyot
        std = math.sqrt(sum((x - ort) ** 2 for x in pencere) / periyot)
        ust = ort + carpan * std
        alt = ort - carpan * std
        bant_genisligi = (ust - alt) / ort * 100
        b_yuzdesi = (fiyatlar[i] - alt) / (ust - alt) if ust != alt else 0.5
        sonuclar.append({
            "ort": round(ort, 2),
            "ust": round(ust, 2),
            "alt": round(alt, 2),
            "std": round(std, 4),
            "bant_genisligi": round(bant_genisligi, 2),
            "b_yuzdesi": round(b_yuzdesi, 4),
        })
    return sonuclar


def squeeze_tespit(band_genislikleri: list[float | None], pencere: int = 20) -> bool:
    gecerli = [g for g in band_genislikleri if g is not None]
    if len(gecerli) < pencere:
        return False
    son = gecerli[-pencere:]
    return gecerli[-1] == min(son)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True)
    parser.add_argument("--periyot", type=int, default=20)
    parser.add_argument("--carpan", type=float, default=2.0)
    args = parser.parse_args()

    try:
        veri = json.loads(args.data)
    except json.JSONDecodeError as e:
        print(json.dumps({"hata": str(e)}))
        sys.exit(1)

    fiyatlar = [d["kapanis"] for d in veri]
    bantlar = bollinger(fiyatlar, args.periyot, args.carpan)
    son = next((b for b in reversed(bantlar) if b), None)

    if not son:
        print(json.dumps({"hata": "Yetersiz veri"}))
        sys.exit(1)

    genislikler = [b["bant_genisligi"] if b else None for b in bantlar]
    squeeze = squeeze_tespit(genislikler)

    b_yorum = "Üst bantın üzerinde" if son["b_yuzdesi"] > 1 else \
              "Alt bantın altında" if son["b_yuzdesi"] < 0 else \
              "Orta bantta" if 0.4 < son["b_yuzdesi"] < 0.6 else \
              "Üst bant bölgesi" if son["b_yuzdesi"] >= 0.6 else "Alt bant bölgesi"

    print(json.dumps({
        **son,
        "squeeze": squeeze,
        "b_yorum": b_yorum,
        "son_fiyat": round(fiyatlar[-1], 2),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
