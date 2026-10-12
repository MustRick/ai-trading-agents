"""
Kompozit skor hesaplayıcı.
memory.md'deki departman ağırlıklarını okur; her departmanın sinyal notunu alır.
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]  # ceo-agent/
MEMORY = ROOT / "memory.md"

# Sinyal → ham puan
SIGNAL_SCORE = {
    "AL":    100,
    "NÖTR":   50,
    "SAT":     0,
    "VETO": None,  # özel durum
}

# memory.md'den ağırlıkları oku (yoksa varsayılan)
DEFAULT_WEIGHTS = {
    "temel":       0.35,
    "teknik":      0.30,
    "haber":       0.15,
    "risk-portfoy": 0.20,
}


def parse_weights(memory_text: str) -> dict:
    weights = {}
    pattern = re.compile(r"(temel|teknik|haber|risk-portfoy)[^\d]*:\s*%(\d+)", re.IGNORECASE)
    for match in pattern.finditer(memory_text):
        dept = match.group(1).lower()
        pct = int(match.group(2)) / 100
        weights[dept] = pct
    return weights if len(weights) == 4 else DEFAULT_WEIGHTS


def compute(signals: dict) -> dict:
    """
    signals: {"temel": "AL", "teknik": "NÖTR", "haber": "AL", "risk-portfoy": "NÖTR"}
    """
    # VETO kontrolü
    if signals.get("risk-portfoy", "").upper() == "VETO":
        return {"skor": 0, "karar": "VETO", "detay": signals}

    memory_text = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else ""
    weights = parse_weights(memory_text)

    skor = 0.0
    for dept, sinyal in signals.items():
        puan = SIGNAL_SCORE.get(sinyal.upper())
        if puan is None:
            return {"skor": 0, "karar": "VETO", "detay": signals}
        agirlik = weights.get(dept.lower(), 0)
        skor += puan * agirlik

    # Risk-Portföy negatif sinyal 2× ağırlık taşır (memory.md kuralı)
    rp_sinyal = signals.get("risk-portfoy", "NÖTR").upper()
    if rp_sinyal == "SAT":
        rp_agirlik = weights.get("risk-portfoy", 0.20)
        skor -= SIGNAL_SCORE["AL"] * rp_agirlik  # ekstra ceza

    skor = max(0, min(100, round(skor, 1)))

    if skor >= 75:
        karar = "Güçlü Al"
    elif skor >= 55:
        karar = "Koşullu Al"
    elif skor >= 40:
        karar = "İzle"
    else:
        karar = "Geç"

    return {"skor": skor, "karar": karar, "detay": signals}


if __name__ == "__main__":
    # Kullanım: python kompozit_skor.py '{"temel":"AL","teknik":"NÖTR","haber":"AL","risk-portfoy":"NÖTR"}'
    if len(sys.argv) < 2:
        print("Kullanım: kompozit_skor.py '<JSON sinyal dict>'")
        sys.exit(1)
    signals = json.loads(sys.argv[1])
    sonuc = compute(signals)
    print(json.dumps(sonuc, ensure_ascii=False, indent=2))
