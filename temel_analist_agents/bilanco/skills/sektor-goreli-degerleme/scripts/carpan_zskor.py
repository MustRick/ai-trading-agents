"""
Sektör içi çarpan z-skoru ve persentil hesaplayıcı.

Kullanım:
    python carpan_zskor.py --hisse GARAN --carpan fk --akranlar '[{"kod":"AKBNK","deger":7.2},...]'

Fintables agent tarafından akran verisi JSON olarak sağlanır.
"""
import json
import math
import argparse
import sys


def z_skor(deger: float, ortalama: float, std: float) -> float:
    if std == 0:
        return 0.0
    return (deger - ortalama) / std


def persentil_yaklas(z: float) -> float:
    """Standart normal CDF yaklaşımı (Abramowitz & Stegun)."""
    t = 1.0 / (1.0 + 0.2316419 * abs(z))
    poly = t * (0.319381530 + t * (-0.356563782 + t * (1.781477937 + t * (-1.821255978 + t * 1.330274429))))
    p = 1.0 - (1.0 / math.sqrt(2 * math.pi)) * math.exp(-0.5 * z * z) * poly
    return p if z >= 0 else 1.0 - p


def yorum(z: float) -> str:
    if z < -1.5:
        return "Çok Ucuz"
    elif z < -1.0:
        return "Ucuz"
    elif z < -0.5:
        return "Hafif Ucuz"
    elif z <= 0.5:
        return "Ortalama"
    elif z <= 1.0:
        return "Hafif Pahalı"
    elif z <= 1.5:
        return "Pahalı"
    else:
        return "Çok Pahalı"


def analiz_et(hisse_kodu: str, hisse_deger: float, akranlar: list[dict], carpan_adi: str) -> dict:
    degerler = [a["deger"] for a in akranlar if a.get("deger") is not None and a["deger"] > 0]

    if len(degerler) < 3:
        return {"hata": f"Yeterli akran yok ({len(degerler)} < 3)"}

    n = len(degerler)
    ort = sum(degerler) / n
    varyans = sum((x - ort) ** 2 for x in degerler) / n
    std = math.sqrt(varyans)

    degerler_sirali = sorted(degerler)
    medyan = degerler_sirali[n // 2] if n % 2 == 1 else (degerler_sirali[n // 2 - 1] + degerler_sirali[n // 2]) / 2

    z = z_skor(hisse_deger, medyan, std)
    pct = persentil_yaklas(z) * 100

    return {
        "hisse": hisse_kodu,
        "carpan": carpan_adi,
        "deger": round(hisse_deger, 2),
        "medyan": round(medyan, 2),
        "ortalama": round(ort, 2),
        "std": round(std, 2),
        "z_skor": round(z, 3),
        "persentil": round(pct, 1),
        "yorum": yorum(z),
        "akran_sayisi": n,
    }


def main():
    parser = argparse.ArgumentParser(description="Sektör çarpan z-skoru")
    parser.add_argument("--hisse", required=True, help="Hedef hisse kodu")
    parser.add_argument("--deger", type=float, required=True, help="Hedef hissenin çarpan değeri")
    parser.add_argument("--carpan", required=True, help="Çarpan adı (fk, pddd, fdfavok)")
    parser.add_argument("--akranlar", required=True, help='JSON: [{"kod":"X","deger":7.2},...]')
    args = parser.parse_args()

    try:
        akranlar = json.loads(args.akranlar)
    except json.JSONDecodeError as e:
        print(json.dumps({"hata": f"JSON parse hatası: {e}"}))
        sys.exit(1)

    sonuc = analiz_et(args.hisse, args.deger, akranlar, args.carpan)
    print(json.dumps(sonuc, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
