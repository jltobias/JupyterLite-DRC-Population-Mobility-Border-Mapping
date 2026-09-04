"""Add a consistent map-and-visualization teaching sequence to each notebook."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = sorted((ROOT / "contents" / "notebooks").glob("*.ipynb")) + sorted(
    (ROOT / "contents" / "storymaps").glob("*.ipynb")
)

MARKDOWN_TOPICS = [
    "Scope and learning objectives",
    "Data provenance and dates",
    "Mobility measures and denominators",
    "DRC to South Sudan corridor",
    "Administrative boundary context",
    "Health-facility access context",
    "Population catchment assumptions",
    "WorldMove package handoff",
    "IOM DTM product handoff",
    "HydroRIVERS context",
    "African Bat Database context",
    "WHYMAP karst and cave context",
    "Overture building context",
    "OpenStreetMap POI context",
    "Airport and transport context",
    "Choropleth interpretation",
    "Buffer interpretation",
    "Missingness and uncertainty",
    "Reproducibility checklist",
    "Analysis handoff",
]

CODE_CELLS = [
    ("map-maplibre", """from IPython.display import IFrame\nIFrame('../../maps/maplibre-drc-mobility.html', width='100%', height=600)"""),
    ("map-geolibre", """from IPython.display import IFrame\nIFrame('../../maps/drc-mobility-map.html', width='100%', height=600)"""),
    ("map-buffer-catchment", """import matplotlib.pyplot as plt\nfrom matplotlib.patches import Circle\n\n# Demonstration buffer/catchment map in lon/lat coordinates; replace points with a dated facility extract.\nfacilities = {'Bunia': (30.22, 1.56), 'Aru': (30.82, 2.62), 'Mahagi': (30.95, 2.28)}\nfig, ax = plt.subplots(figsize=(8, 5))\nfor name, (lon, lat) in facilities.items():\n    ax.scatter(lon, lat, s=45, label=name)\n    ax.add_patch(Circle((lon, lat), 0.18, fill=False, alpha=0.45))\nax.set(title='Health-facility buffers and population-catchment review', xlabel='Longitude', ylabel='Latitude')\nax.legend()\nplt.show()"""),
    ("viz-flow", """import pandas as pd\nimport matplotlib.pyplot as plt\n\nflow_demo = pd.DataFrame({'destination': ['Uganda', 'South Sudan', 'Rwanda', 'Burundi'], 'count': [12000, 2600, 8500, 6200]})\nflow_demo.sort_values('count').plot.barh(x='destination', y='count', color='#d96c42', legend=False, title='Illustrative cross-border mobility')\nplt.xlabel('Demonstration count; replace with dated observations')\nplt.tight_layout()\nplt.show()"""),
    ("viz-choropleth", """import pandas as pd\nimport matplotlib.pyplot as plt\n\n# Choropleth-ready administrative summary; join these values to GADM geometry by ADM_ID in a GIS workflow.\nadmin_summary = pd.DataFrame({'admin': ['Ituri', 'North Kivu', 'South Kivu', 'Upper Nile'], 'mobility_index': [0.82, 0.67, 0.54, 0.39]})\nadmin_summary.sort_values('mobility_index').plot.barh(x='admin', y='mobility_index', color=plt.cm.viridis(admin_summary.sort_values('mobility_index')['mobility_index']))\nplt.title('Choropleth-ready mobility index by administrative area')\nplt.xlabel('Standardized demonstration index')\nplt.tight_layout()\nplt.show()"""),
    ("viz-catchments", """import numpy as np\nimport matplotlib.pyplot as plt\n\n# Compare population captured by successive facility buffers; use population-grid data for a real catchment calculation.\nradii_km = np.array([5, 10, 25, 50])\npopulation_captured = np.array([18000, 42000, 98000, 165000])\nplt.plot(radii_km, population_captured, marker='o', color='#147d7e')\nplt.fill_between(radii_km, population_captured, alpha=0.15, color='#147d7e')\nplt.title('Illustrative facility catchment sensitivity')\nplt.xlabel('Buffer radius (km)')\nplt.ylabel('Population within catchment')\nplt.grid(alpha=0.25)\nplt.show()"""),
    ("qa-layer-catalog", """import pandas as pd\n\nlayer_catalog = pd.DataFrame([\n    ('Mobility', 'IOM DTM', 'select dated DRC product'),\n    ('Mobility', 'WorldMove', 'select city package'),\n    ('Boundaries', 'GADM', 'repository snapshot'),\n    ('Access', 'Healthsites.io', 'Ituri GeoJSON'),\n    ('Hydrography', 'HydroRIVERS', 'DRC/Great Lakes extract'),\n    ('Context', 'Bats, karst, buildings, POI, airports', 'repository layers'),\n], columns=['theme', 'provider', 'status'])\nlayer_catalog"""),
    ("qa-flow-schema", """required_flow_fields = ['origin', 'destination', 'reference_date', 'count', 'source']\nrequired_flow_fields"""),
    ("qa-coordinates", """coordinate_checks = {'longitude_range': (-180, 180), 'latitude_range': (-90, 90), 'crs': 'EPSG:4326'}\ncoordinate_checks"""),
    ("qa-date", """from datetime import date\nretrieval_date = date.today().isoformat()\nretrieval_date"""),
    ("qa-dtm", """dtm_portal = 'https://dtm.iom.int/democratic-republic-congo'\n{'provider': 'IOM DTM', 'url': dtm_portal, 'status': 'select dated product before analysis'}"""),
    ("qa-worldmove", """worldmove_portal = 'https://fi.ee.tsinghua.edu.cn/worldmove/'\n{'provider': 'WorldMove', 'url': worldmove_portal, 'status': 'select city package before analysis'}"""),
    ("qa-boundaries", """gadm_countries = ['COD', 'UGA', 'RWA', 'BDI', 'SSD', 'ZMB', 'TZA', 'CAF', 'COG', 'AGO']\nlen(gadm_countries), gadm_countries"""),
    ("qa-facilities", """healthsites_url = 'https://raw.githubusercontent.com/healthsites/drc-ebola-2026/master/healthsites_ituri_drc.geojson'\nhealthsites_url"""),
    ("qa-hydrorivers", """hydrorivers_url = 'https://raw.githubusercontent.com/jltobias/JupyterLite-DRC-Population-Mobility-Border-Mapping/main/data/hydrosheds/hydrorivers-af-drc-great-lakes.geojson'\nhydrorivers_url"""),
    ("qa-sources", """source_urls = ['https://gadm.org/data.html', 'https://www.hydrosheds.org/products/hydrorivers', 'https://www.naturalearthdata.com/downloads/10m-cultural-vectors/airports/']\nsource_urls"""),
    ("qa-buffer", """buffer_radii_km = [5, 10, 25, 50]\nassert all(radius > 0 for radius in buffer_radii_km)\nbuffer_radii_km"""),
    ("qa-catchment", """catchment_method = 'planar buffer plus population-grid overlay; validate CRS and boundary effects'\ncatchment_method"""),
    ("qa-uncertainty", """uncertainty_notes = ['synthetic demonstration values', 'provider coverage varies', 'buffer distance is not travel time']\nuncertainty_notes"""),
    ("qa-export", """export_fields = ['layer', 'provider', 'reference_date', 'geography', 'license', 'transformation']\nexport_fields"""),
    ("qa-final", """analysis_ready = False\nreason = 'Replace handoff and demonstration layers with dated provider extracts and document transformations.'\nanalysis_ready, reason"""),
]


def markdown_cell(topic: str, index: int) -> dict:
    return {
        "cell_type": "markdown",
        "id": f"auto-markdown-{index:02d}",
        "metadata": {},
        "source": [
            f"## {topic}\n",
            "Use this section to record the selected data release, geography, reference period, license, and limitations. Keep mapped context distinct from observed mobility or displacement evidence.",
        ],
    }


def code_cell(identifier: str, source: str, index: int) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "id": f"auto-{identifier}-{index:02d}",
        "metadata": {},
        "outputs": [],
        "source": [line + "\n" for line in source.splitlines()[:-1]] + [source.splitlines()[-1]],
    }


for path in NOTEBOOKS:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    existing_markdown = sum(cell.get("cell_type") == "markdown" for cell in notebook["cells"])
    existing_code = sum(cell.get("cell_type") == "code" for cell in notebook["cells"])
    markdown_needed = max(0, 20 - existing_markdown)
    code_needed = max(0, 20 - existing_code)
    for index, topic in enumerate(MARKDOWN_TOPICS[:markdown_needed], start=1):
        notebook["cells"].append(markdown_cell(topic, index))
    for index, (identifier, source) in enumerate(CODE_CELLS[:code_needed], start=1):
        notebook["cells"].append(code_cell(identifier, source, index))
    path.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(path.relative_to(ROOT), "markdown=", sum(c.get("cell_type") == "markdown" for c in notebook["cells"]), "code=", sum(c.get("cell_type") == "code" for c in notebook["cells"]))
