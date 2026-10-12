"""
RSI hesaplayıcı + negatif diverjans tespiti.

Kullanım:
    python rsi.py --data '[{"tarih":"2026-01-01","kapanis":100.0},...]' --periyot 14
"""
import json, argparse, sys


def rsi_hesapla(fiyatlar: list[float], periyot: int = 14) -> list[float | None]:
    degisimler = [fiyatlar[i] - fiyatlar[i - 1] for i in range(1, len(fiyatlar))]
    kazanclar = [max(d, 0) for d in degisimler]
    kayiplar = [abs(min(d, 0)) for d in degisimler]

    sonuc = [None] * len(fiyatlar)
    if len(kazanclar) < periyot:
        return sonuc

    ort_kazanc = sum(kazanclar[:periyot]) / periyot
    ort_kayip = sum(kayiplar[:periyot]) / periyot

    for i in range(periyot, len(kazanclar)):
        ort_kazanc = (ort_kazanc * (periyot - 1) + kazanclar[i]) / periyot
        ort_kayip = (ort_kayip * (periyot - 1) + kayiplar[i]) / periyot
        rs = ort_kazanc / ort_kayip if ort_kayip != 0 else float("inf")
        sonuc[i + 1] = 100 - (100 / (1 + rs))

    return sonuc


def divergans_kontrol(fiyatlar: list[float], rsi_dizi: list[float | None], pencere: int = 14) -> str:
    gecerli_rsi = [(i, r) for i, r in enumerate(rsi_dizi) if r is not None]
    if len(gecerli_rsi) < pencere:
        return "Yeterli veri yok"

    son = gecerli_rsi[-pencere:]
    fiyat_son = [fiyatlar[i] for i, _ in son]
    rsi_son = [r for _, r in son]

    fiyat_artiyor = fiyat_son[-1] > max(fiyat_son[:-1])
    rsi_azaliyor = rsi_son[-1] < max(rsi_son[:-1])

    fiyat_azaliyor = fiyat_son[-1] < min(fiyat_son[:-1])
    rsi_artiyor = rsi_son[-1] > min(rsi_son[:-1])

    if fiyat_artiyor and rsi_azaliyor:
        return "NEGATİF DİVERJANS — Güç kaybı sinyali"
    elif fiyat_azaliyor and rsi_artiyor:
        return "POZİTİF DİVERJANS — Toparlanma sinyali"
    return "Yok"


def bolge(rsi: float) -> str:
    if rsi > 70: return "Aşırı Alım"
    if rsi > 50: return "Boğa Bölgesi"
    if rsi > 30: return "Ayı Bölgesi"
    return "Aşırı Satım"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True)
    parser.add_argument("--periyot", type=int, default=14)
    args = parser.parse_args()

    try:
        veri = json.loads(args.data)
    except json.JSONDecodeError as e:
        print(json.dumps({"hata": str(e)}))
        sys.exit(1)

    fiyatlar = [d["kapanis"] for d in veri]
    rsi_dizi = rsi_hesapla(fiyatlar, args.periyot)
    son_rsi = next((r for r in reversed(rsi_dizi) if r is not None), None)

    print(json.dumps({
        "rsi": round(son_rsi, 2) if son_rsi else None,
        "bolge": bolge(son_rsi) if son_rsi else None,
        "divergans": divergans_kontrol(fiyatlar, rsi_dizi),
        "periyot": args.periyot,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
