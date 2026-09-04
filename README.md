# DRC Population Mobility and Border Mapping

Browser-based notebooks, JupyterGIS-ready storymaps, MapLibre/GeoLibre maps, and flowmaps for exploring population mobility between the Democratic Republic of the Congo (DRC) and the Great Lakes region of Africa.

## Open the browser project

The links below are stable GitHub Pages targets. They become live after the repository's **Deploy browser workspace** action completes and GitHub Pages is configured to deploy from GitHub Actions.

- [JupyterLite workspace](https://jltobias.github.io/JupyterLite-DRC-Population-Mobility-Border-Mapping/lab/index.html)
- [Data inventory notebook](https://jltobias.github.io/JupyterLite-DRC-Population-Mobility-Border-Mapping/lab/index.html?path=notebooks/01_data_inventory.ipynb)
- [Mobility flowmap notebook](https://jltobias.github.io/JupyterLite-DRC-Population-Mobility-Border-Mapping/lab/index.html?path=notebooks/02_mobility_flowmap.ipynb)
- [Health and access notebook](https://jltobias.github.io/JupyterLite-DRC-Population-Mobility-Border-Mapping/lab/index.html?path=notebooks/03_health_access_layers.ipynb)
- [JupyterGIS storymap storyboard](https://jltobias.github.io/JupyterLite-DRC-Population-Mobility-Border-Mapping/lab/index.html?path=storymaps/drc-ebola-mobility-storymap.ipynb)
- [GeoLibre Web mobility map](https://jltobias.github.io/JupyterLite-DRC-Population-Mobility-Border-Mapping/maps/drc-mobility-map.html)
- [MapLibre GL JS notebook](https://jltobias.github.io/JupyterLite-DRC-Population-Mobility-Border-Mapping/lab/index.html?path=notebooks/04_maplibre_experience.ipynb)
- [Repository contents](https://github.com/jltobias/JupyterLite-DRC-Population-Mobility-Border-Mapping/tree/main/contents)

## Geographic and analytical scope

The project covers DRC and Uganda, Rwanda, Burundi, South Sudan, Zambia, Tanzania, Central African Republic, Republic of the Congo, and Angola. It is designed for monthly or event-based comparisons of origin, destination, route, population exposure, displacement, and access to services.

The 2026 health context is an active research theme: WHO reports a Bundibugyo virus disease outbreak in DRC and Uganda, with sustained transmission and cross-border preparedness needs. Use the latest WHO and national Ministry of Health reporting; never treat this repository's demo layer as a case or risk dataset.

## What is in this repository

- `contents/notebooks/01_data_inventory.ipynb` — source inventory and provenance checklist.
- `contents/notebooks/02_mobility_flowmap.ipynb` — browser-runnable flowmap example using explicitly synthetic values.
- `contents/notebooks/03_health_access_layers.ipynb` — Overpass query starter and metadata fields for health, shelter, and transport layers.
- `contents/storymaps/drc-ebola-mobility-storymap.ipynb` — JupyterGIS-ready narrative storyboard.
- `maps/drc-mobility-map.html` — launcher for the hosted GeoLibre Web app with the DRC demonstration GeoJSON.
- `maps/maplibre-drc-mobility.html` — standalone MapLibre GL JS map used by the MapLibre notebook.
- `data/README.md` — safe data-ingestion rules and suggested folder layout.
- `.github/workflows/deploy-pages.yml` — automatic JupyterLite + static-map deployment.

## Important data and safety rules

The included map and notebook flow values are **demonstration data only**. They are present so the browser interface can be inspected immediately; they are not IOM, WorldPop, WHO, UNHCR, or government estimates. Add a dated provider extract before publishing an analytical result.

For every layer, preserve `source`, `source_url`, `reference_period`, `retrieved_on`, `measurement_type`, geography, methodology, and uncertainty. Do not publish personal data, precise sensitive locations, inferred nationality, infection status, or individual movement. Mobility association does not establish transmission.

## Local use

Serve the repository root with a static web server and open `maps/drc-mobility-map.html`. To build the notebook workspace locally:

```powershell
python -m pip install jupyterlite-core jupyterlite-pyodide-kernel
jupyter lite build --contents contents --output-dir dist
```

Copy `maps/` into `dist/` before serving. The GitHub Actions workflow performs this build on pushes to `main`.

## References and data sources

These are the authoritative starting points used by the notebooks and planned analytical layers. Record the exact dataset version and download date in each output.

1. International Organization for Migration, Displacement Tracking Matrix (DTM): [DTM DRC country page](https://dtm.iom.int/democratic-republic-congo) and [DTM flow-monitoring library](https://dtm.iom.int/taxonomy/term/4). Use flow monitoring, mobility tracking, displacement tracking, and site-assessment products where available.
2. WorldPop, University of Southampton: [WorldPop data portal](https://www.worldpop.org/). Use gridded population estimates and document raster year, resolution, and aggregation method.
3. Humanitarian Data Exchange: [HDX](https://data.humdata.org/). Use country, boundary, humanitarian, and OCHA-managed layers with their individual licenses.
4. UNHCR: [Operational Data Portal](https://data.unhcr.org/). Use refugee, asylum-seeker, returnee, and displacement situation datasets.
5. WHO: [DRC 2026 Ebola situation page](https://www.who.int/emergencies/situations/ebola-outbreak---drc-2026), [Disease Outbreak News](https://www.who.int/emergencies/disease-outbreak-news), and [WHO AFRO Ebola updates](https://www.afro.who.int/health-topics/ebola-disease/outbreak-drc-26). Use only dated, verified outbreak information.
6. OpenStreetMap and Overpass API: [OpenStreetMap](https://www.openstreetmap.org/) and [Overpass API](https://overpass-api.de/). Potential layers include health facilities, roads, border crossings, airports, bus stops, and places. Follow ODbL attribution and completeness limitations.
7. Humanitarian OpenStreetMap Team: [HOT Export Tool](https://export.hotosm.org/). Use humanitarian mapping extracts where available and retain the export date.
8. Natural Earth: [Natural Earth data](https://www.naturalearthdata.com/). Use public-domain small-scale country boundaries and cartographic reference layers.
9. GeoNames: [GeoNames](https://www.geonames.org/). Use gazetteer and place-name context for geographic joins.

## License and attribution

Code and original documentation are MIT-licensed unless a future license file states otherwise. External data remains under each provider's license and terms. Retain provider attribution, version/date, and redistribution restrictions for all additions to `data/`.
