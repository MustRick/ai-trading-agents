"""
Piotroski F-Skoru hesaplayıcı (9 noktalı sistem).

Kullanım:
    python piotroski_f.py --data '{"roa":0.05,"roa_prev":0.03,...}'

Tüm parametreler Fintables'tan gelen finansal veriden türetilir.
"""
import json
import argparse
import sys


def hesapla(d: dict) -> dict:
    skorlar = {}

    # ── Karlılık Grubu (F1–F4) ──────────────────────────────────────────────
    # F1: ROA pozitif mi?
    skorlar["F1_roa_pozitif"] = 1 if d.get("roa", 0) > 0 else 0

    # F2: Faaliyetlerden nakit akışı pozitif mi?
    skorlar["F2_nakit_akisi_pozitif"] = 1 if d.get("cfo", 0) > 0 else 0

    # F3: ROA arttı mı?
    skorlar["F3_roa_artis"] = 1 if d.get("roa", 0) > d.get("roa_prev", 0) else 0

    # F4: Tahakkuk kalitesi — CFO / Toplam Varlık > ROA
    cfo = d.get("cfo", 0)
    toplam_varlik = d.get("toplam_varlik", 1)
    skorlar["F4_tahakkuk_kalitesi"] = 1 if (cfo / toplam_varlik) > d.get("roa", 0) else 0

    # ── Kaldıraç / Likidite Grubu (F5–F7) ───────────────────────────────────
    # F5: Uzun vadeli borç/varlık oranı azaldı mı?
    skorlar["F5_borc_azaldi"] = 1 if d.get("uzun_borc_oran", 1) < d.get("uzun_borc_oran_prev", 1) else 0

    # F6: Cari oran arttı mı?
    skorlar["F6_cari_oran_artis"] = 1 if d.get("cari_oran", 0) > d.get("cari_oran_prev", 0) else 0

    # F7: Yeni hisse ihracı yapılmadı mı?
    skorlar["F7_seyreltme_yok"] = 1 if not d.get("yeni_hisse_ihrac", False) else 0

    # ── Verimlilik Grubu (F8–F9) ────────────────────────────────────────────
    # F8: Brüt kar marjı arttı mı?
    skorlar["F8_brut_marj_artis"] = 1 if d.get("brut_marj", 0) > d.get("brut_marj_prev", 0) else 0

    # F9: Varlık devir hızı arttı mı?
    skorlar["F9_varlik_devri_artis"] = 1 if d.get("varlik_devri", 0) > d.get("varlik_devri_prev", 0) else 0

    toplam = sum(skorlar.values())

    return {
        "hisse": d.get("hisse", "?"),
        "f_skor": toplam,
        "detay": skorlar,
        "yorum": _yorum(toplam),
        "gruplar": {
            "karlilik": sum(v for k, v in skorlar.items() if k.startswith("F1") or k.startswith("F2") or k.startswith("F3") or k.startswith("F4")),
            "kaldirac": sum(v for k, v in skorlar.items() if k.startswith("F5") or k.startswith("F6") or k.startswith("F7")),
            "verimlilik": sum(v for k, v in skorlar.items() if k.startswith("F8") or k.startswith("F9")),
        },
    }


def _yorum(skor: int) -> str:
    if skor >= 7:
        return "Güçlü"
    elif skor >= 5:
        return "Ortalama"
    else:
        return "Zayıf"


def main():
    parser = argparse.ArgumentParser(description="Piotroski F-Skoru")
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
