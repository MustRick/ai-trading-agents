"""
Seçici sonuçlarını temizleme ve yapılandırma yardımcıları.
parse_html / fetcher_get css_results çıktısını işlemek için kullanılır.
"""

from __future__ import annotations
import re
from typing import Any


def clean_results(values: list[str], strip: bool = True, drop_empty: bool = True) -> list[str]:
    """Seçici sonuçlarından boşlukları ve gereksiz karakterleri temizle."""
    out: list[str] = []
    for v in values:
        text = str(v)
        if strip:
            text = re.sub(r"\s+", " ", text).strip()
        if drop_empty and not text:
            continue
        out.append(text)
    return out


def zip_columns(columns: dict[str, list[str]], fill: Any = None) -> list[dict[str, Any]]:
    """
    Paralel seçici listelerini sözlük listesine dönüştür.

    Örnek:
        zip_columns({"ad": ["A", "B"], "fiyat": ["10", "20"]})
        → [{"ad": "A", "fiyat": "10"}, {"ad": "B", "fiyat": "20"}]
    """
    if not columns:
        return []
    max_len = max(len(v) for v in columns.values())
    rows: list[dict[str, Any]] = []
    for i in range(max_len):
        row: dict[str, Any] = {}
        for key, vals in columns.items():
            row[key] = vals[i] if i < len(vals) else fill
        rows.append(row)
    return rows


def extract_numbers(text: str) -> list[float]:
    """Bir metin dizisinden sayısal değerleri çıkar (fiyat, oran, vb.)."""
    pattern = r"[\d]+[.,]?[\d]*"
    matches = re.findall(pattern, text.replace(",", "."))
    results: list[float] = []
    for m in matches:
        try:
            results.append(float(m))
        except ValueError:
            pass
    return results


def first_number(text: str) -> float | None:
    """Metindeki ilk sayısal değeri döndür."""
    nums = extract_numbers(text)
    return nums[0] if nums else None


def deduplicate(items: list[dict], key: str) -> list[dict]:
    """Belirli bir alana göre tekrar eden kayıtları kaldır."""
    seen: set[Any] = set()
    out: list[dict] = []
    for item in items:
        val = item.get(key)
        if val not in seen:
            seen.add(val)
            out.append(item)
    return out


def flatten_css_results(css_results: dict[str, list[str]]) -> dict[str, list[str]]:
    """css_results dict'ini temizlenmiş haliyle döndür."""
    return {selector: clean_results(values) for selector, values in css_results.items()}
