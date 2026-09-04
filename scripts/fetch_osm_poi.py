"""Fetch a small, browser-ready OSM POI extract through Overpass."""

import json
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "osm" / "poi-goma-sample.geojson"
BBOX = "-1.69,29.225,-1.68,29.235"  # south, west, north, east
QUERY = f"""[out:json][timeout:60];
(nwr[\"amenity\"]({BBOX}); nwr[\"shop\"]({BBOX}); nwr[\"tourism\"]({BBOX});
 nwr[\"office\"]({BBOX}); nwr[\"public_transport\"]({BBOX}););
out center tags;"""


request = Request(
    "https://overpass-api.de/api/interpreter",
    data=urlencode({"data": QUERY}).encode("utf-8"),
    headers={"User-Agent": "DRC-mobility-mapping/1.0", "Accept": "application/json"},
)
payload = json.loads(urlopen(request).read().decode("utf-8"))
features = []
for element in payload.get("elements", []):
    tags = element.get("tags", {})
    if "lat" in element and "lon" in element:
        coordinates = [element["lon"], element["lat"]]
    elif element.get("center"):
        coordinates = [element["center"]["lon"], element["center"]["lat"]]
    else:
        continue
    properties = {"osm_id": element["id"], "osm_type": element["type"], **tags}
    features.append({"type": "Feature", "properties": properties, "geometry": {"type": "Point", "coordinates": coordinates}})

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text(json.dumps({"type": "FeatureCollection", "name": "OpenStreetMap POI — Goma sample", "features": features}, ensure_ascii=False), encoding="utf-8")
print(f"Wrote {len(features)} POI features to {OUTPUT}")
