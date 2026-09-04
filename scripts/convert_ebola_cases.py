"""Create a mapped subset of the HDX Ebola cases/deaths CSV."""

import csv
import json
import sys
from collections import defaultdict
from pathlib import Path


LOCATIONS = {
    "Bunia": (30.25, 1.56),
    "Mongbalu": (30.02, 1.95),
    "Rwampara": (30.31, 1.55),
    "Butembo": (29.29, 0.13),
    "Goma": (29.23, -1.68),
    "Katwa": (29.37, 0.13),
    "Nyakunde": (29.78, 1.26),
    "Beni": (29.47, 0.49),
    "Aru": (30.83, 2.86),
    "Mahagi": (30.99, 2.15),
    "Mambasa": (29.18, 1.56),
    "Isiro": (27.62, 2.77),
    "Makiso-Kisangani": (25.19, 0.52),
}


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("usage: convert_ebola_cases.py INPUT.csv OUTPUT.geojson")
    latest = defaultdict(list)
    with Path(sys.argv[1]).open(encoding="utf-8-sig", newline="") as stream:
        for row in csv.DictReader(stream):
            name = row.get("location_name")
            if name not in LOCATIONS or row.get("measure") not in {"cases", "deaths"}:
                continue
            key = (name, row["measure"])
            latest[key].append(row)

    features = []
    for name, (lon, lat) in LOCATIONS.items():
        values = {"cases": 0, "deaths": 0}
        dates = []
        for measure in values:
            rows = latest.get((name, measure), [])
            if not rows:
                continue
            latest_date = max(row["reference_date"] for row in rows)
            selected = [row for row in rows if row["reference_date"] == latest_date]
            values[measure] = sum(float(row["value"] or 0) for row in selected)
            dates.append(latest_date)
        if not dates:
            continue
        features.append({
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [lon, lat]},
            "properties": {
                "location_name": name,
                "cases": values["cases"],
                "deaths": values["deaths"],
                "reference_date": max(dates),
                "source": "HDX / INRB-UMIE",
                "source_url": "https://data.humdata.org/dataset/republique-democratique-du-congo-cas-et-deces-d-ebola",
                "coordinate_note": "Approximate locality coordinate added for mapping; source CSV has no coordinates.",
            },
        })
    output = {"type": "FeatureCollection", "name": "DRC Ebola cases and deaths (HDX mapped subset)", "features": features}
    Path(sys.argv[2]).write_text(json.dumps(output, separators=(",", ":")), encoding="utf-8")
    print(f"wrote {len(features)} mapped localities")


if __name__ == "__main__":
    main()
