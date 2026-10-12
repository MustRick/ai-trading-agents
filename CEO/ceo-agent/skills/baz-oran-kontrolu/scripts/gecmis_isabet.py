"""
Geçmiş isabet oranı hesaplayıcı.
signals.db (SQLite) üzerinden skor aralığına göre AL kararlarının ne kadarının
hedefine ulaştığını hesaplar.

Tablo şeması (beklenen):
  signals(id, sembol, tarih, kompozit_skor, karar, hedef_fiyat, kapaniş_fiyat, sonuc)
  sonuc: 'HIT' | 'MISS' | 'OPEN'
"""

import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DB_PATH = ROOT / "signals.db"


def isabet_orani(skor_alt: float, skor_ust: float, son_n_gun: int = 90) -> dict:
    if not DB_PATH.exists():
        return {
            "hata": f"signals.db bulunamadı: {DB_PATH}",
            "skor_araligi": f"{skor_alt}–{skor_ust}",
        }

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    cur.execute(
        """
        SELECT COUNT(*) as toplam,
               SUM(CASE WHEN sonuc = 'HIT' THEN 1 ELSE 0 END) as isabet
        FROM signals
        WHERE kompozit_skor BETWEEN ? AND ?
          AND sonuc IN ('HIT', 'MISS')
          AND tarih >= date('now', ? || ' days')
        """,
        (skor_alt, skor_ust, f"-{son_n_gun}"),
    )
    row = cur.fetchone()
    con.close()

    toplam = row[0] or 0
    isabet = row[1] or 0
    oran = round((isabet / toplam * 100), 1) if toplam > 0 else None

    return {
        "skor_araligi": f"{skor_alt}–{skor_ust}",
        "son_n_gun": son_n_gun,
        "toplam_sinyal": toplam,
        "isabet_sayisi": isabet,
        "isabet_orani_pct": oran,
        "yorum": (
            "Yetersiz veri" if toplam < 5
            else "Güçlü" if (oran or 0) >= 65
            else "Orta" if (oran or 0) >= 45
            else "Zayıf"
        ),
    }


if __name__ == "__main__":
    # Kullanım: python gecmis_isabet.py <skor_alt> <skor_ust> [son_n_gun]
    if len(sys.argv) < 3:
        print("Kullanım: gecmis_isabet.py <skor_alt> <skor_ust> [son_n_gun=90]")
        sys.exit(1)
    alt = float(sys.argv[1])
    ust = float(sys.argv[2])
    gun = int(sys.argv[3]) if len(sys.argv) > 3 else 90
    import json
    print(json.dumps(isabet_orani(alt, ust, gun), ensure_ascii=False, indent=2))
