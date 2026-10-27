# Decisions

## Environment
- Python <3.12.3>, rasterio <1.5.2>, GDAL <3.12.2> — Windows, venv + pip.
  Why: recorded because geospatial defaults change between releases.

## Coordinate system
- All processing in EPSG:25832 (ETRS89 / UTM 32N).
  Why: metric, and it's the native CRS of the Danish data.s