param(
  [string]$PagesBase = 'https://jltobias.github.io/JupyterLite-DRC-Population-Mobility-Border-Mapping/'
)

$chromeCandidates = @(
  "$env:ProgramFiles\Google\Chrome\Application\chrome.exe",
  "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe",
  "$env:LocalAppData\Google\Chrome\Application\chrome.exe"
)
$chrome = $chromeCandidates | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
if (-not $chrome) {
  throw 'Google Chrome was not found. Install Chrome or update the path in this script.'
}

$paths = @(
  'lab/index.html?path=notebooks/01_data_inventory.ipynb',
  'lab/index.html?path=notebooks/02_mobility_flowmap.ipynb',
  'lab/index.html?path=notebooks/03_health_access_layers.ipynb',
  'lab/index.html?path=notebooks/04_maplibre_experience.ipynb',
  'lab/index.html?path=storymaps/drc-ebola-mobility-storymap.ipynb',
  'lab/index.html?path=storymaps/ebola-weekly-map-tour.ipynb',
  'maps/drc-mobility-map.html',
  'maps/maplibre-drc-mobility.html'
)
$urls = $paths | ForEach-Object { $PagesBase.TrimEnd('/') + '/' + $_ }
Start-Process -FilePath $chrome -ArgumentList $urls
