"""Create a portable JupyterGIS story-map project (.jGIS)."""
import json
import math
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "contents" / "storymaps" / "drc-ebola-outbreak-storymap.jGIS"

def uid():
    return str(uuid.uuid4())

def mercator(lon, lat):
    radius = 6378137.0
    x = radius * math.radians(lon)
    y = radius * math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))
    return x, y

osm_source = uid()
ebola_source = uid()
osm_layer = uid()
ebola_layer = uid()
stops = [
    ("Mongbalu", 30.02, 1.95, "Ituri reporting cluster", "Review the locality series alongside dated response and mobility evidence."),
    ("Bunia", 30.25, 1.56, "Ituri provincial context", "Use the urban and referral context to ask what access data cover the same period."),
    ("Beni", 29.47, 0.49, "North Kivu corridor", "Compare weekly reported values without inferring transmission from adjacency."),
    ("Butembo", 29.29, 0.13, "North Kivu health-service context", "Verify facilities and service availability against a dated provider extract."),
    ("Goma", 29.23, -1.68, "Cross-border preparedness context", "A city context stop—not a claim about case location or individual risk."),
    ("Aru", 30.83, 2.86, "Northern border-facing context", "Pair reported observations with verified border, displacement, and mobility data."),
]

layers = {}
sources = {}
layer_tree = [osm_layer, ebola_layer]
sources[osm_source] = {
    "name": "OpenStreetMap.Mapnik",
    "parameters": {"attribution": "(C) OpenStreetMap contributors", "bounds": [],
                   "htmlAttribution": "", "interpolate": False, "maxZoom": 19.0,
                   "minZoom": 0.0, "provider": "OpenStreetMap",
                   "url": "https://tile.openstreetmap.org/{z}/{x}/{y}.png",
                   "urlParameters": {}, "useProxy": False},
    "type": "RasterSource",
}
sources[ebola_source] = {
    "name": "DRC Ebola reported values",
    "parameters": {"httpHeaders": "", "path": "data/ebola/drc-ebola-cases-deaths.geojson",
                   "useProxy": False},
    "type": "GeoJSONSource",
}
layers[osm_layer] = {"name": "OpenStreetMap.Mapnik", "parameters": {"opacity": 1.0, "source": osm_source},
                     "type": "RasterLayer", "visible": True}
layers[ebola_layer] = {
    "name": "Ebola reported values — approximate localities",
    "parameters": {"opacity": 0.9, "source": ebola_source,
                   "symbologyState": {}, "color": {"circle-fill-color": "#c0392b",
                   "circle-radius": 7.0, "circle-stroke-color": "#ffffff",
                   "circle-stroke-width": 1.5}},
    "type": "VectorLayer", "visible": True,
}

segments = []
for name, lon, lat, chapter, note in stops:
    x, y = mercator(lon, lat)
    segment = uid()
    layer_tree.append(segment)
    layers[segment] = {
        "name": name,
        "parameters": {
            "content": {
                "contentMode": "map",
                "markdown": f"**{chapter}.** {note}\\n\\nReported values are cumulative provider observations. Coordinates are approximate locality placements, not patient or facility locations. See the notebook for weekly charts, source fields, and Google Maps context links.",
                "title": name,
            },
            "extent": [x - 150000, y - 150000, x + 150000, y + 150000],
            "layerOverride": [],
            "transition": {"time": 1.5, "type": "smooth"},
            "zoom": 7.2,
        },
        "type": "StorySegmentLayer", "visible": True,
    }
    segments.append(segment)

west, south = mercator(24.0, -4.0)
east, north = mercator(34.0, 4.5)
project = {
    "layerTree": layer_tree, "layers": layers, "metadata": {
        "title": "DRC Ebola outbreak — place and time",
        "dataNote": "HDX / INRB-UMIE reported cumulative values; approximate locality coordinates.",
        "source": "https://data.humdata.org/dataset/republique-democratique-du-congo-cas-et-deces-d-ebola",
    },
    "options": {"bearing": 0.0, "extent": [west, south, east, north],
                "latitude": 1.0, "longitude": 29.8, "pitch": 0.0,
                "projection": "EPSG:3857", "zoom": 6.0},
    "schemaVersion": "0.6.0", "sources": sources,
    "stories": {uid(): {"presentationBgColor": "#241b1e",
                         "presentationTextColor": "#f6eee5",
                         "showGradient": True, "storySegments": segments,
                         "storyType": "guided",
                         "title": "DRC Ebola outbreak: place and time"}},
    "viewState": {},
}
OUT.write_text(json.dumps(project, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(OUT.relative_to(ROOT), "created with", len(segments), "guided segments")
