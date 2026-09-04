"""Create a mapped locality subset from the openAFRICA Ebola health-zone CSV."""

import csv
import json
import sys
from collections import defaultdict
from pathlib import Path


LOCATIONS = {
    "Bunia": (30.25, 1.56), "Mongbwalu": (30.02, 1.95), "Rwampara": (30.31, 1.55),
    "Butembo": (29.29, 0.13), "Goma": (29.23, -1.68), "Katwa": (29.37, 0.13),
    "Nyankunde": (29.78, 1.26), "Beni": (29.47, 0.49), "Aru": (30.83, 2.86),
    "Mambasa": (29.18, 1.56), "Isiro": (27.62, 2.77), "Makiso": (25.19, 0.52),
}


def number(value: str) -> float:
    return float(value) if value and value.strip() else 0.0


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("usage: convert_openafrica_ebola.py INPUT.csv OUTPUT.geojson")
    latest = defaultdict(list)
    with Path(sys.argv[1]).open(encoding="utf-8-sig", newline="") as stream:
        for row in csv.DictReader(stream):
            if row.get("Health Zone") in LOCATIONS:
                latest[row["Health Zone"]].append(row)
    features = []
    for name, (lon, lat) in LOCATIONS.items():
        rows = latest.get(name, [])
        if not rows:
            continue
        date = max(row["Date"] for row in rows)
        selected = [row for row in rows if row["Date"] == date]
        features.append({
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [lon, lat]},
            "properties": {
                "health_zone": name,
                "province": selected[0].get("Province"),
                "confirmed_cases": sum(number(row.get("Confirmed Cases", "")) for row in selected),
                "confirmed_deaths": sum(number(row.get("Confirmed Deaths", "")) for row in selected),
                "reference_date": date,
                "source": "openAFRICA / Ministère de la Santé Publique RDC",
                "source_url": "https://open.africa/dataset/ebola-case-figures-2026",
                "coordinate_note": "Approximate locality coordinate added for mapping; source CSV has no coordinates.",
            },
        })
    output = {"type": "FeatureCollection", "name": "openAFRICA Ebola case figures (mapped subset)", "features": features}
    Path(sys.argv[2]).write_text(json.dumps(output, separators=(",", ":")), encoding="utf-8")
    print(f"wrote {len(features)} mapped health zones")


if __name__ == "__main__":
    main()
