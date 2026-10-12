"""
Altman Z-Skoru hesaplayıcı (halka açık şirketler için orijinal 1968 modeli).

Formül: Z = 1.2·X1 + 1.4·X2 + 3.3·X3 + 0.6·X4 + 1.0·X5

Kullanım:
    python altman_z.py --data '{"donem_varlik":500,"toplam_varlik":2000,...}'

NOT: Bankalar ve finans şirketleri için bu model geçersizdir.
"""
import json
import argparse
import sys


def hesapla(d: dict) -> dict:
    try:
        tv = d["toplam_varlik"]
        if tv == 0:
            raise ValueError("toplam_varlik sıfır olamaz")

        # X1 = (Dönen Varlık - Kısa Vadeli Borç) / Toplam Varlık
        x1 = (d["donem_varlik"] - d["kisa_borc"]) / tv

        # X2 = Dağıtılmamış Kârlar / Toplam Varlık
        x2 = d["dagitilmamis_kar"] / tv

        # X3 = FAVÖK / Toplam Varlık
        x3 = d["favok"] / tv

        # X4 = Özkaynak Piyasa Değeri / Toplam Borç
        toplam_borc = d.get("toplam_borc", d.get("kisa_borc", 0) + d.get("uzun_borc", 0))
        x4 = d["piyasa_degeri"] / toplam_borc if toplam_borc > 0 else 0

        # X5 = Net Satış / Toplam Varlık
        x5 = d["net_satis"] / tv

        z = 1.2 * x1 + 1.4 * x2 + 3.3 * x3 + 0.6 * x4 + 1.0 * x5

        return {
            "hisse": d.get("hisse", "?"),
            "z_skor": round(z, 3),
            "yorum": _yorum(z),
            "bolge": _bolge(z),
            "bilesenler": {
                "X1_calisma_sermayesi": round(x1, 4),
                "X2_dagitilmamis_kar": round(x2, 4),
                "X3_favok_verim": round(x3, 4),
                "X4_piyasa_borc": round(x4, 4),
                "X5_varlik_devri": round(x5, 4),
            },
        }
    except KeyError as e:
        return {"hata": f"Eksik parametre: {e}"}
    except Exception as e:
        return {"hata": str(e)}


def _yorum(z: float) -> str:
    if z > 2.99:
        return "Güvenli Bölge"
    elif z > 1.81:
        return "Gri Bölge — Dikkat"
    else:
        return "Tehlike — İflas Riski"


def _bolge(z: float) -> str:
    if z > 2.99:
        return "güvenli"
    elif z > 1.81:
        return "gri"
    else:
        return "tehlike"


def main():
    parser = argparse.ArgumentParser(description="Altman Z-Skoru")
    parser.add_argument("--data", required=True, help="JSON finansal veri")
    args = parser.parse_args()

    try:
        data = json.loads(args.data)
    except json.JSONDecodeError as e:
        print(json.dumps({"hata": f"JSON parse hatası: {e}"}))
        sys.exit(1)

    sonuc = hesapla(data)
    print(json.dumps(sonuc, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
