"""Prefer the bundled HDX Ebola CSV in JupyterLite notebooks."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
URL = "https://raw.githubusercontent.com/jltobias/JupyterLite-DRC-Population-Mobility-Border-Mapping/main/data/ebola/drc_ebola_cases_consolidated.csv"
LOCAL = "data/ebola/drc_ebola_cases_consolidated.csv"


for path in sorted((ROOT / "contents" / "notebooks").glob("*.ipynb")) + sorted((ROOT / "contents" / "storymaps").glob("*.ipynb")):
    notebook = json.loads(path.read_text(encoding="utf-8"))
    changed = False
    for cell in notebook["cells"]:
        if cell.get("cell_type") != "code":
            continue
        source = "".join(cell.get("source", []))
        if URL not in source or "local_ebola_url" in source:
            continue
        source = source.replace(
            f"ebola_url = '{URL}'\nebola = pd.read_csv(ebola_url, parse_dates=['reference_date'])",
            f"ebola_url = '{URL}'\nlocal_ebola_url = '{LOCAL}'\ntry:\n    ebola = pd.read_csv(local_ebola_url, parse_dates=['reference_date'])\n    ebola_source = 'bundled JupyterLite contents copy'\nexcept (FileNotFoundError, OSError):\n    ebola = pd.read_csv(ebola_url, parse_dates=['reference_date'])\n    ebola_source = 'repository URL fallback'",
        )
        source = source.replace(
            f"ebola_url = '{URL}'\nebola = pd.read_csv(ebola_url, parse_dates=['reference_date'])",
            f"ebola_url = '{URL}'\nlocal_ebola_url = '{LOCAL}'\ntry:\n    ebola = pd.read_csv(local_ebola_url, parse_dates=['reference_date'])\n    ebola_source = 'bundled JupyterLite contents copy'\nexcept (FileNotFoundError, OSError):\n    ebola = pd.read_csv(ebola_url, parse_dates=['reference_date'])\n    ebola_source = 'repository URL fallback'",
        )
        cell["source"] = [line + "\n" for line in source.splitlines()[:-1]] + [source.splitlines()[-1]]
        changed = True
    if changed:
        path.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        print(path.relative_to(ROOT), "updated")
