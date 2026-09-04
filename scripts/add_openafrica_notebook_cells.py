"""Append openAFRICA Ebola data loading and comparison visualizations."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = sorted((ROOT / "contents" / "notebooks").glob("*.ipynb")) + sorted(
    (ROOT / "contents" / "storymaps").glob("*.ipynb")
)
BASE = "https://raw.githubusercontent.com/jltobias/JupyterLite-DRC-Population-Mobility-Border-Mapping/main/data/openafrica/"


def cell(kind, identifier, source):
    result = {"cell_type": kind, "id": identifier, "metadata": {}, "source": [line + "\n" for line in source.splitlines()[:-1]] + [source.splitlines()[-1]]}
    if kind == "code":
        result.update({"execution_count": None, "outputs": []})
    return result


new_cells = [
    cell("markdown", "openafrica-ebola-analysis", "## openAFRICA Ebola case figures\nLoad the national and health-zone CSV resources from openAFRICA, retain their publication/reference dates, and compare them with HDX only after checking definitions and reporting periods."),
    cell("code", "load-openafrica-ebola", f"""import pandas as pd

openafrica_national_url = '{BASE}drc_national_timeseries.csv'
openafrica_zones_url = '{BASE}drc_zones_timeseries.csv'
local_openafrica_national_url = 'data/openafrica/drc_national_timeseries.csv'
local_openafrica_zones_url = 'data/openafrica/drc_zones_timeseries.csv'
try:
    openafrica_national = pd.read_csv(local_openafrica_national_url, parse_dates=['Report_date', 'Publication_date'])
    openafrica_zones = pd.read_csv(local_openafrica_zones_url, parse_dates=['Date'])
    openafrica_source = 'bundled repository copies'
except (FileNotFoundError, OSError):
    openafrica_national = pd.read_csv(openafrica_national_url, parse_dates=['Report_date', 'Publication_date'])
    openafrica_zones = pd.read_csv(openafrica_zones_url, parse_dates=['Date'])
    openafrica_source = 'repository URL fallback'
print('Loaded openAFRICA data from', openafrica_source)
openafrica_national.head(), openafrica_zones.head()"""),
    cell("code", "plot-openafrica-national", """import matplotlib.pyplot as plt\n\nopenafrica_national.set_index('Report_date')[['Confirmed', 'Deaths']].plot(figsize=(10, 4), color=['#fc8d59', '#9e0142'], title='openAFRICA national Ebola case figures')\nplt.ylabel('Reported cumulative value')\nplt.xlabel('Report date')\nplt.grid(alpha=0.25)\nplt.tight_layout()\nplt.show()"""),
    cell("code", "plot-openafrica-zones", """latest_openafrica_date = openafrica_zones['Date'].max()\nlatest_openafrica_zones = openafrica_zones[openafrica_zones['Date'].eq(latest_openafrica_date)].copy()\nlatest_openafrica_zones.set_index('Health Zone')[['Confirmed Cases', 'Confirmed Deaths']].sort_values('Confirmed Cases').tail(15).plot.barh(figsize=(9, 6), color=['#fc8d59', '#9e0142'], title=f'openAFRICA health-zone figures ({latest_openafrica_date.date()})')\nplt.xlabel('Reported cumulative value')\nplt.tight_layout()\nplt.show()"""),
    cell("code", "analyze-openafrica-cfr", """latest_national = openafrica_national.sort_values('Report_date').iloc[-1]\nopenafrica_summary = {'report_date': latest_national['Report_date'].date().isoformat(), 'confirmed': latest_national['Confirmed'], 'deaths': latest_national['Deaths'], 'cfr_pct': latest_national['cfr_pct'], 'status': latest_national['Status']}\nopenafrica_summary"""),
]

for path in NOTEBOOKS:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    existing = {c.get("id"): c for c in notebook["cells"]}
    if "load-openafrica-ebola" in existing:
        replacement = next(c for c in new_cells if c.get("id") == "load-openafrica-ebola")
        target = existing["load-openafrica-ebola"]
        target.clear()
        target.update(replacement)
        changed = True
    else:
        notebook["cells"].extend(new_cells)
        changed = True
    if not changed:
        continue
    path.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(path.relative_to(ROOT), "updated")
