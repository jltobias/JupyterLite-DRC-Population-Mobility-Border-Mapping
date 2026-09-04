"""Append runnable HDX Ebola case/death loading and visualizations to notebooks."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = sorted((ROOT / "contents" / "notebooks").glob("*.ipynb")) + sorted(
    (ROOT / "contents" / "storymaps").glob("*.ipynb")
)
EBOLA_URL = "https://raw.githubusercontent.com/jltobias/JupyterLite-DRC-Population-Mobility-Border-Mapping/main/data/ebola/drc_ebola_cases_consolidated.csv"


def md_cell() -> dict:
    return {
        "cell_type": "markdown",
        "id": "hdx-ebola-analysis",
        "metadata": {},
        "source": [
            "## HDX Ebola cases and deaths\n",
            "The following cells load the complete HDX/INRB-UMIE CSV for dated case/death summaries. The mapped layer is a locality subset because the source CSV does not include coordinates; do not interpret these summaries as risk estimates or infer transmission from mobility."
        ],
    }


def code_cell(identifier: str, source: str) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "id": identifier,
        "metadata": {},
        "outputs": [],
        "source": [line + "\n" for line in source.splitlines()[:-1]] + [source.splitlines()[-1]],
    }


cells = [
    code_cell("load-hdx-ebola", f"""import pandas as pd\n\nebola_url = '{EBOLA_URL}'\nebola = pd.read_csv(ebola_url, parse_dates=['reference_date'])\nebola = ebola[ebola['measure'].isin(['cases', 'deaths'])].copy()\nebola[['location_name', 'reference_date', 'measure', 'case_classification', 'time_period', 'value']].head()"""),
    code_cell("plot-ebola-timeseries", """import matplotlib.pyplot as plt\n\nweekly = ebola.groupby(['reference_date', 'measure'], as_index=False)['value'].sum().pivot(index='reference_date', columns='measure', values='value').fillna(0)\nweekly.plot(figsize=(10, 4), color={'cases': '#d73027', 'deaths': '#542788'}, title='HDX DRC Ebola cases and deaths over time')\nplt.ylabel('Reported cumulative value')\nplt.xlabel('Reference date')\nplt.grid(alpha=0.25)\nplt.tight_layout()\nplt.show()"""),
    code_cell("plot-ebola-locations", """import matplotlib.pyplot as plt\n\nlatest_date = ebola['reference_date'].max()\nlatest = ebola[ebola['reference_date'].eq(latest_date)].groupby(['location_name', 'measure'], dropna=False)['value'].sum().unstack(fill_value=0)\nlatest.sort_values('cases', ascending=True).tail(15).plot.barh(y=['cases', 'deaths'], figsize=(9, 6), color=['#d73027', '#542788'], title=f'Latest HDX Ebola values by locality ({latest_date.date()})')\nplt.xlabel('Reported cumulative value')\nplt.tight_layout()\nplt.show()"""),
]


for path in NOTEBOOKS:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    if any(cell.get("id") == "load-hdx-ebola" for cell in notebook["cells"]):
        continue
    notebook["cells"].append(md_cell())
    notebook["cells"].extend(cells)
    path.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(path.relative_to(ROOT), "updated")
