"""Convert the supplied WHYMAP WOKAM shapefiles to browser-ready GeoJSON."""

import json
from pathlib import Path

import shapefile


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "whymap" / "shp"
OUTPUT = ROOT / "data" / "whymap" / "geojson"

DATASETS = {
    "caves": "whymap_cave__v3_point",
    "karst": "whymap_karst__v1_poly",
    "non_exposed_karst": "whymap_nonExposedKarst__v1_point",
    "springs": "whymap_spring__v3_point",
}


def convert(name: str, stem: str) -> None:
    reader = shapefile.Reader(str(SOURCE / stem))
    fields = [field[0] for field in reader.fields[1:]]
    features = []
    for shape_record in reader.iterShapeRecords():
        properties = dict(zip(fields, shape_record.record))
        geometry = shape_record.shape.__geo_interface__
        features.append({"type": "Feature", "properties": properties, "geometry": geometry})
    output = OUTPUT / f"{name}.geojson"
    output.write_text(
        json.dumps(
            {
                "type": "FeatureCollection",
                "name": f"WHYMAP WOKAM {name}",
                "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}},
                "features": features,
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    print(f"{name}: {len(features)} features -> {output}")


OUTPUT.mkdir(parents=True, exist_ok=True)
for dataset_name, stem in DATASETS.items():
    convert(dataset_name, stem)
