# Data drop zone

Put dated, licensed provider extracts here before running analysis. Do not commit personal data or precise sensitive locations.

`drc-mobility-demo.geojson` is an illustrative layer used by the GeoLibre Web and MapLibre demonstrations; it is not an official estimate.

Suggested layout:

- `iom_dtm/` - DTM flow monitoring, displacement tracking, or mobility tracking extracts.
- `worldpop/` - WorldPop raster or tabular population estimates.
- `unhcr/` - refugee, returnee, asylum-seeker, and IDP situation snapshots.
- `health/` - WHO, national ministry, or HDX health and outbreak layers.
- `osm/` - OpenStreetMap or HOT exports for facilities, roads, airports, and bus stations.
- `boundaries/` - Natural Earth or another documented administrative/border source.

Every file should have a companion note with provider, dataset title, URL, retrieval date, reference period, license, and any transformations.

The browser demonstrations use the public [healthsites.io Ituri DRC export](https://raw.githubusercontent.com/healthsites/drc-ebola-2026/master/healthsites_ituri_drc.geojson), exported 2026-06-01 and licensed ODbL 1.0. The Healthsites API requires an API key for refreshed downloads; never put that key in a public map URL.

The browser demonstrations use GADM 4.1 level-1 GeoJSON endpoints for COD, UGA, RWA, BDI, SSD, ZMB, TZA, CAF, COG, and AGO. GADM data are freely available for academic and other non-commercial use; redistribution and commercial use require permission. See the [GADM data page](https://gadm.org/data.html).

The Pages workflow converts the current [African Bat Database Figshare record](https://figshare.com/articles/dataset/African_Bat_Database/26363308) CSV (version 6, updated 2026-08-05) into `data/african-bat-database.geojson` at deploy time. The dataset is CC BY 4.0; cite Monadjem et al. (2024) and retain the Figshare DOI `10.6084/m9.figshare.26363308.v6`.
