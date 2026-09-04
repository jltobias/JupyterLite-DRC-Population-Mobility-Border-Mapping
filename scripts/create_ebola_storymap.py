"""Create the third narrative JupyterGIS-ready Ebola storymap notebook."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "contents" / "storymaps" / "drc-ebola-outbreak-storymap.ipynb"

def md(identifier, *lines):
    return {"cell_type": "markdown", "id": identifier, "metadata": {},
            "source": [line + "\n" for line in lines[:-1]] + [lines[-1]]}

def code(identifier, source):
    return {"cell_type": "code", "execution_count": None, "id": identifier,
            "metadata": {}, "outputs": [],
            "source": [line + "\n" for line in source.splitlines()[:-1]] + [source.splitlines()[-1]]}

cells = [
    md("title", "# DRC Ebola outbreak: a place-and-time storymap", "",
       "A guided JupyterGIS tour of reported Ebola observations, response geography, and local context. Move from the outbreak timeline to selected health zones, then open the same places in the project maps. This is a data-literacy and response-context story—not a transmission or individual-risk map."),
    md("how-to", "## How to use this tour", "",
       "Run the setup and tour cells from top to bottom. The interactive panel has Previous/Next navigation, a week slider, and a zone selector. The map points are approximate locality placements derived from the source CSV; they are not facility or patient coordinates."),
    md("sources", "## Evidence, provenance, and responsible interpretation", "",
       "The bundled line listing is the repository's consolidated HDX / INRB-UMIE extract. Keep the provider, source URL, reference date, case classification, cumulative time period, and quality notes with any export. For current interpretation, consult WHO Disease Outbreak News and DRC Ministry of Health reporting; the linked sources are starting points, not substitutes for verification."),
    code("setup", """import json
import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import HTML, IFrame, display

local_ebola_url = 'data/ebola/drc_ebola_cases_consolidated.csv'
remote_ebola_url = 'https://raw.githubusercontent.com/jltobias/JupyterLite-DRC-Population-Mobility-Border-Mapping/main/data/ebola/drc_ebola_cases_consolidated.csv'
try:
    ebola = pd.read_csv(local_ebola_url, parse_dates=['reference_date'])
    ebola_source = 'bundled repository copy'
except (FileNotFoundError, OSError):
    ebola = pd.read_csv(remote_ebola_url, parse_dates=['reference_date'])
    ebola_source = 'repository URL fallback'
ebola['value'] = pd.to_numeric(ebola['value'], errors='coerce').fillna(0)
ebola = ebola[ebola['measure'].isin(['cases', 'deaths', 'contacts'])].copy()
ebola['week'] = ebola['reference_date'].dt.to_period('W-SUN').apply(lambda p: p.start_time)
print(f'{len(ebola):,} rows loaded from {ebola_source}; {ebola["reference_date"].min().date()} to {ebola["reference_date"].max().date()}')"""),
    code("coordinates", """# Approximate locality coordinates for visual orientation only.
coords = {
    'Mongbalu': (30.02, 1.95), 'Bunia': (30.25, 1.56), 'Rwampara': (30.31, 1.55),
    'Beni': (29.47, 0.49), 'Butembo': (29.29, 0.13), 'Goma': (29.23, -1.68),
    'Aru': (30.83, 2.86), 'Mahagi': (30.99, 2.15), 'Mambasa': (29.18, 1.56),
    'Isiro': (27.62, 2.77), 'Kisangani': (25.19, 0.52),
}
mapped = ebola[ebola['location_name'].isin(coords)].copy()
mapped[['location_name', 'week', 'measure', 'value']].head()"""),
    md("frame-1", "## Frame 1 — The outbreak is a changing record", "",
       "The source is a time series of reported cumulative values. A point on the map means that a locality has a mapped representative coordinate; it does not mean every case occurred at that point. Begin by looking at the reporting cadence and the difference between cases, deaths, and contacts."),
    code("trend", """weekly = (mapped.groupby(['week', 'measure'], as_index=False)['value'].sum()
          .pivot(index='week', columns='measure', values='value').fillna(0).sort_index())
ax = weekly.plot(figsize=(11, 4), color={'cases': '#c0392b', 'deaths': '#4b1f6f', 'contacts': '#167d8d'}, linewidth=2)
ax.set_title('Mapped subset: reported cumulative values by epidemiological week')
ax.set_xlabel('Week beginning'); ax.set_ylabel('Reported cumulative value')
ax.grid(alpha=0.22); plt.tight_layout(); plt.show()"""),
    md("frame-2", "## Frame 2 — Follow the geography", "",
       "The six stops below are a narrative route through the mapped subset: the Ituri reporting cluster, the Beni–Butembo corridor, the Goma context, and the northern border-facing Aru/Mahagi area. Use the zone selector to compare places; do not infer a route of infection from geographic adjacency."),
    code("story-data", """story_stops = [
    {'name': 'Mongbalu', 'chapter': 'Ituri', 'note': 'A gold-mining and transport context in the Ituri reporting cluster.'},
    {'name': 'Bunia', 'chapter': 'Ituri', 'note': 'Provincial urban and referral context; compare the reporting series with access layers.'},
    {'name': 'Beni', 'chapter': 'North Kivu', 'note': 'A corridor stop for reviewing weekly change and response connectivity.'},
    {'name': 'Butembo', 'chapter': 'North Kivu', 'note': 'Urban health-service context; verify facilities against a dated provider extract.'},
    {'name': 'Goma', 'chapter': 'North Kivu', 'note': 'A major city and cross-border preparedness context, not a case-location claim.'},
    {'name': 'Aru', 'chapter': 'Ituri border context', 'note': 'Northern border-facing context; pair with verified border and mobility observations.'},
]
latest = (mapped.sort_values('reference_date').groupby(['location_name', 'measure'], as_index=False).tail(1)
          .pivot(index='location_name', columns='measure', values='value').fillna(0))
for stop in story_stops:
    vals = latest.loc[stop['name']] if stop['name'] in latest.index else pd.Series()
    stop.update({'lon': coords[stop['name']][0], 'lat': coords[stop['name']][1],
                 'cases': float(vals.get('cases', 0)), 'deaths': float(vals.get('deaths', 0)),
                 'contacts': float(vals.get('contacts', 0))})
story_stops"""),
    code("tour", r'''# Browser-safe interactive tour with no extra Python package dependencies.
weeks = sorted(str(pd.Timestamp(w).date()) for w in mapped['week'].dropna().unique())
zone_rows = []
for name in coords:
    for week in weeks:
        part = mapped[(mapped['location_name'].eq(name)) & (mapped['week'].eq(pd.Timestamp(week)))]
        vals = part.groupby('measure')['value'].sum()
        zone_rows.append({'name': name, 'week': week, 'cases': float(vals.get('cases', 0)),
                          'deaths': float(vals.get('deaths', 0)), 'contacts': float(vals.get('contacts', 0)),
                          'lon': coords[name][0], 'lat': coords[name][1]})
payload = json.dumps({'stops': story_stops, 'rows': zone_rows, 'weeks': weeks})
tour_html = """<style>
.ebola-tour{font:14px system-ui,sans-serif;color:#18232b;background:#f7f4ed;border:1px solid #d6cec0;border-radius:14px;padding:18px;max-width:1050px}
.ebola-tour h3{margin:0 0 5px;color:#6e1d27}.ebola-tour .controls{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin:14px 0}
.ebola-tour button,.ebola-tour select{font:inherit;padding:7px 10px;border:1px solid #9e8f80;border-radius:7px;background:white}
.ebola-tour .grid{display:grid;grid-template-columns:minmax(260px,1fr) minmax(270px,1fr);gap:18px}.ebola-tour .map{background:#e8eee8;border-radius:10px;min-height:330px;padding:8px}
.ebola-tour svg{width:100%;height:315px}.ebola-tour .panel{background:white;border-radius:10px;padding:15px}.ebola-tour .metric{display:inline-block;margin:8px 8px 4px 0;padding:8px 10px;background:#f2e5dc;border-radius:7px}
.ebola-tour small{color:#5d6567}.ebola-tour a{color:#125c70}</style>
<div class="ebola-tour"><h3 id="et-title"></h3><small id="et-subtitle"></small><div class="controls">
<button id="et-prev">← Previous</button><button id="et-next">Next →</button><label>Week <input id="et-week" type="range" min="0" value="0"></label><select id="et-zone"></select><span id="et-count"></span></div>
<div class="grid"><div class="map"><svg id="et-map" viewBox="0 0 600 330" role="img" aria-label="Approximate locality map"></svg></div><div class="panel"><div id="et-copy"></div><div id="et-metrics"></div>
<p><a id="et-street" target="_blank" rel="noopener">Open Google Maps ground context ↗</a></p><small>Coordinates are approximate locality placements. Street View availability and imagery dates vary; imagery is contextual only.</small></div></div></div>
<script>
const etData = PAYLOAD; let etStop=0,etWeek=0;
const $=id=>document.getElementById(id);
const esc=s=>String(s).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;"}[c]));
function project(lon,lat){return [((lon-24)/10)*600,((4-lat)/8)*330]}
function render(){let s=etData.stops[etStop],w=etData.weeks[etWeek],r=etData.rows.find(x=>x.name===s.name&&x.week===w)||{cases:0,deaths:0,contacts:0};
  $("et-title").textContent=(etStop+1)+". "+s.name+" — "+s.chapter;$("et-subtitle").textContent="Week beginning "+w+" · "+s.note;
  $("et-week").value=etWeek;$("et-count").textContent="stop "+(etStop+1)+" / "+etData.stops.length;$("et-zone").value=s.name;
  $("et-copy").innerHTML="<p><b>What to notice:</b> compare this week with the full trend above, then inspect the source line listing below.</p><p><b>Interpretation:</b> reported values reflect the provider's cumulative series and definitions; a zero here can mean no mapped row for that place/week.</p>";
  $("et-metrics").innerHTML=["cases","deaths","contacts"].map(k=>"<span class='metric'><b>"+k+"</b><br>"+Number(r[k]).toLocaleString()+"</span>").join("");
  $("et-street").href="https://www.google.com/maps/search/?api=1&query="+s.lat+","+s.lon;let svg=$("et-map");svg.innerHTML="<rect x='0' y='0' width='600' height='330' fill='#e8eee8'/>";
  etData.stops.forEach((p,i)=>{let [x,y]=project(p.lon,p.lat),active=i===etStop;svg.innerHTML+="<circle cx='"+x+"' cy='"+y+"' r='"+(active?10:5)+"' fill='"+(active?"#c0392b":"#167d8d")+"' stroke='white' stroke-width='2'/><text x='"+(x+8)+"' y='"+(y+4)+"' font-size='12' fill='#18232b'>"+esc(p.name)+"</text>"})}
etData.stops.forEach((s,i)=>$("et-zone").add(new Option(s.name,i)));$("et-week").max=etData.weeks.length-1;
$("et-prev").onclick=()=>{etStop=(etStop+etData.stops.length-1)%etData.stops.length;render()};$("et-next").onclick=()=>{etStop=(etStop+1)%etData.stops.length;render()};
$("et-week").oninput=e=>{etWeek=Number(e.target.value);render()};$("et-zone").onchange=e=>{etStop=Number(e.target.value);render()};render();
</script>""".replace('PAYLOAD', payload)
display(HTML(tour_html))'''),
    md("line-listing-note", "## Audit trail — the rows behind the tour", "Use this compact line listing to inspect the exact provider fields behind the selected places and weeks. Missing locality-week rows are not automatically zeros."),
    code("line-listing", """line_listing = (mapped[['location_name', 'reference_date', 'week', 'measure',
                              'case_classification', 'time_period', 'value', 'source', 'source_url']]
                .sort_values(['reference_date', 'location_name', 'measure']))
display(line_listing.head(60))"""),
    md("frame-3", "## Frame 3 — From a point to a response question", "",
       "A map becomes useful when it prompts a question that can be checked. For each stop, ask: what was the reporting period? which health facilities and transport links were actually available then? what border or displacement observations cover the same period? what uncertainty remains?"),
    code("comparison", """stop_names = [s['name'] for s in story_stops]
chart = latest.reindex(stop_names).fillna(0)[['cases', 'deaths']]
ax = chart.sort_values('cases').plot.barh(figsize=(9, 4), color=['#c0392b', '#4b1f6f'])
ax.set_title('Latest mapped-subset values for the story stops')
ax.set_xlabel('Reported cumulative value'); ax.set_ylabel('')
ax.grid(axis='x', alpha=0.2); plt.tight_layout(); plt.show()"""),
    md("frame-4", "## Frame 4 — Add facilities, imagery, and reporting carefully", "",
       "The project maps provide the spatial canvas. Use the Healthsites.io export, OpenStreetMap/Overpass points, and dated DTM or WorldMove products to add response context. Ground-view links can help explain roads, neighborhoods, and facility surroundings, while news and WHO links provide narrative context. None of these layers independently establishes exposure, transmission, or causality."),
    code("maps", """display(IFrame('../../maps/drc-mobility-map.html', width='100%', height=620))"""),
    code("jupytergis-api", """# Optional JupyterGIS Python API handoff (run in a JupyterGIS environment).
try:
    from jupytergis import GISDocument
    doc = GISDocument(latitude=1.0, longitude=29.8, zoom=6)
    await doc.ready()
    doc.add_geojson_layer(path='data/ebola/drc-ebola-cases-deaths.geojson',
                          name='DRC Ebola reported values — approximate localities')
    doc
except ImportError:
    print('JupyterGIS is not installed in this lightweight JupyterLite build. Open the notebook in JupyterGIS and run this cell there.')"""),
    md("jupytergis", "## JupyterGIS handoff", "",
       "Open this notebook in JupyterGIS and load 'data/ebola/drc-ebola-cases-deaths.geojson' as the outbreak observation layer. Style cases and deaths separately, keep the approximate-coordinate note in the layer metadata, and add only dated, documented facility, boundary, mobility, or displacement layers. The story frames above can serve as the slide/script outline for a JupyterGIS presentation."),
    code("jupytergis-layer", """jupytergis_layer = {
    'path': 'data/ebola/drc-ebola-cases-deaths.geojson',
    'name': 'DRC Ebola reported values — approximate locality points',
    'geometry': 'Point', 'time_field': 'reference_date',
    'style_suggestion': {'cases': '#c0392b', 'deaths': '#4b1f6f'},
    'coordinate_note': 'Approximate locality coordinate added for mapping; not a patient or facility location.',
}
jupytergis_layer"""),
    md("sources-end", "## Source links and publication checklist", "",
       "[HDX / INRB-UMIE case and death data](https://data.humdata.org/dataset/republique-democratique-du-congo-cas-et-deces-d-ebola) · [WHO DRC Ebola situation page](https://www.who.int/emergencies/situations/ebola-outbreak---drc-2026) · [WHO Disease Outbreak News](https://www.who.int/emergencies/disease-outbreak-news) · [Healthsites.io DRC export](https://raw.githubusercontent.com/healthsites/drc-ebola-2026/master/healthsites_ituri_drc.geojson) · [Google Maps](https://www.google.com/maps). Before publishing, record retrieval date, provider release, geography, license, coordinate uncertainty, and whether each value is cumulative, revised, suspected, or confirmed."),
]

notebook = {"cells": cells, "metadata": {"kernelspec": {"display_name": "Python (Pyodide)", "language": "python", "name": "python"}, "language_info": {"name": "python", "version": "3.11"}}, "nbformat": 4, "nbformat_minor": 5}
OUT.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print(OUT.relative_to(ROOT), "created with", len(cells), "cells")
