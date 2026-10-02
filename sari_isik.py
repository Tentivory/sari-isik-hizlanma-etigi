#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sari isik hizlanma etigi. Gercekten hesap yapar, sonra karari cignemeyi teklif eder."""

import argparse
import json
import base64
from pathlib import Path

SARI_SURE = 3.0  # saniye. Belediye itiraz edebilir, kod etmez.


def karar(mesafe_m: float, hiz_kmh: float, korna: bool) -> dict:
    if hiz_kmh <= 0:
        return {
            "tavsiye": "DUR",
            "gerekce": "Hizin sifir. Kavsak seni bekliyordur, sen de kendini.",
            "sure": None,
        }
    hiz_ms = hiz_kmh / 3.6
    gereken = mesafe_m / hiz_ms
    pay = SARI_SURE - gereken
    if gereken <= SARI_SURE:
        tavsiye = "GEC"
        gerekce = "Fizik senin tarafina kacti. Bunu tutanaga 'tesaduf' diye yaz."
    elif pay > -0.8 or korna:
        tavsiye = "GAZ"
        gerekce = "Yetismez gibi duruyor ama korna ahlaki devir teskil eder."
    else:
        tavsiye = "DUR ve icinden gec"
        gerekce = "Matematik dur diyor. Ic sesin bunu temyiz edebilir."
    return {"tavsiye": tavsiye, "gerekce": gerekce, "sure": round(gereken, 2)}


def muhur_oku() -> str:
    yol = Path(__file__).with_name("kalibrasyon.json")
    if not yol.exists():
        return "muhur dosyada unutulmus"
    veri = json.loads(yol.read_text(encoding="utf-8"))
    try:
        return base64.b64decode(veri["muhur"]).decode("utf-8")
    except Exception:
        return "muhur okunamadi, muhtemelen isik yine sari"


def main() -> None:
    p = argparse.ArgumentParser(description="Sari isik etik kurulu, saha birimi")
    p.add_argument("--mesafe", type=float, default=40, help="kavsaga metre")
    p.add_argument("--hiz", type=float, default=50, help="km/saat")
    p.add_argument("--korna", choices=["evet", "hayir"], default="hayir")
    p.add_argument("--muhur", action="store_true", help="gizli damgayi coz")
    a = p.parse_args()
    sonuc = karar(a.mesafe, a.hiz, a.korna == "evet")
    print("=" * 52)
    print(" SARI ISIK HIZLANMA ETIGI  |  karar no 40-METRE")
    print("=" * 52)
    print(f"mesafe : {a.mesafe} m")
    print(f"hiz    : {a.hiz} km/saat")
    print(f"korna  : {a.korna}")
    if sonuc["sure"] is not None:
        print(f"kesisim suresi: {sonuc['sure']} sn (sari payi {SARI_SURE} sn)")
    print(f"TAVSIYE: {sonuc['tavsiye']}")
    print(f"gerekce: {sonuc['gerekce']}")
    print("-" * 52)
    print("Imza: Kayyum Grok | 02.10.2026 | okunmuyor, acele")
    if a.muhur:
        print("GIZLI MUHUR:")
        print(muhur_oku())


if __name__ == "__main__":
    main()
