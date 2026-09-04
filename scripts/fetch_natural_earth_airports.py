"""Download Natural Earth 10m airports and write a browser-ready GeoJSON file."""

import json
import zipfile
from io import BytesIO
from pathlib import Path
from urllib.request import Request, urlopen

import shapefile

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "natural-earth" / "airports-10m.geojson"
URL = "https://naturalearth.s3.amazonaws.com/10m_cultural/ne_10m_airports.zip"

request = Request(URL, headers={"User-Agent": "DRC-mobility-mapping/1.0"})
with zipfile.ZipFile(BytesIO(urlopen(request).read())) as archive:
    shape_name = next(name for name in archive.namelist() if name.endswith("ne_10m_airports.shp"))
    stem = shape_name[:-4]
    reader = shapefile.Reader(
        shp=BytesIO(archive.read(shape_name)),
        shx=BytesIO(archive.read(stem + ".shx")),
        dbf=BytesIO(archive.read(stem + ".dbf")),
    )
    fields = [field[0] for field in reader.fields[1:]]
    features = []
    for shape_record in reader.iterShapeRecords():
        properties = dict(zip(fields, shape_record.record))
        geometry = shape_record.shape.__geo_interface__
        features.append({"type": "Feature", "properties": properties, "geometry": geometry})

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text(
    json.dumps({"type": "FeatureCollection", "name": "Natural Earth 10m airports", "features": features}, ensure_ascii=False),
    encoding="utf-8",
)
print(f"Wrote {len(features)} airports to {OUTPUT}")
