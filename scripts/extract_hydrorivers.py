"""Extract the DRC/Great Lakes window from the official HydroRIVERS Africa shapefile."""

import json
import sys
from pathlib import Path

import shapefile


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("usage: extract_hydrorivers.py INPUT.shp OUTPUT.geojson")

    reader = shapefile.Reader(sys.argv[1])
    field_names = [field[0] for field in reader.fields[1:]]
    # DRC, South Sudan, Uganda, Rwanda, Burundi, Tanzania, Zambia, CAR,
    # Republic of the Congo, and Angola context.
    extent = (12.0, -14.0, 36.0, 6.0)
    features = []
    for record, shape in zip(reader.records(), reader.shapes()):
        attributes = dict(zip(field_names, record))
        # Keep the navigable/main network suitable for an interactive browser
        # map. The complete Africa download contains hundreds of thousands of
        # reaches and is intentionally not bundled into this repository.
        if (attributes.get("ORD_STRA") or 0) < 3 and (attributes.get("CATCH_SKM") or 0) < 1000:
            continue
        min_x, min_y, max_x, max_y = shape.bbox
        if max_x < extent[0] or min_x > extent[2] or max_y < extent[1] or min_y > extent[3]:
            continue
        properties = attributes
        parts = list(shape.parts) + [len(shape.points)]
        lines = [shape.points[start:end] for start, end in zip(parts, parts[1:])]
        geometry = {"type": "LineString", "coordinates": lines[0]} if len(lines) == 1 else {
            "type": "MultiLineString",
            "coordinates": lines,
        }
        features.append({"type": "Feature", "properties": properties, "geometry": geometry})

    output = {
        "type": "FeatureCollection",
        "name": "HydroRIVERS_v10_af_DRC_Great_Lakes",
        "features": features,
    }
    Path(sys.argv[2]).write_text(json.dumps(output, separators=(",", ":")), encoding="utf-8")
    print(f"wrote {len(features)} river reaches")


if __name__ == "__main__":
    main()
