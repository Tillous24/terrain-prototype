import math
import rasterio
from rasterio.warp import transform as warp_xy
import numpy as np
from rasterio.transform import from_origin
from rasterio.warp import reproject, Resampling

def glo30_url(lon, lat):
    tile = (f"Copernicus_DSM_COG_10_N{math.floor(lat):02d}_00_"
             f"E{math.floor(lon):03d}_00_DEM")
    return f"https://copernicus-dem-30m.s3.amazonaws.com/{tile}/{tile}.tif"

url = glo30_url(10.57, 56.23) # Mols Bjerge
print(url)

with rasterio.open(url) as src:
    print("CRS      ", src.crs)
    print("size     ", src.width, "x", src.height)
    print("cell size", src.res)
    print("bounds   ", src.bounds)
    print("nodata   ", src.nodata)

CRS = "EPSG:25832" #EPSG:25832 flattens a strip of the Earth onto a grid in metres
RES = 30.0
SIZE = 4980.0 #4980.0/30=166

def box_bounds(lon, lat):
    # Transform lon/lat to CRS and round to nearest RES
    xs, ys = warp_xy("EPSG:4326", CRS, [lon], [lat])
    cx = round(xs[0] / RES) * RES
    cy = round(ys[0] / RES) * RES
    half = SIZE / 2
    return cx - half, cy - half, cx + half, cy + half   # xmin, ymin, xmax, ymax

print(box_bounds(10.57, 56.23))

#Cell height calculation
def read_box(lon, lat):
    xmin, ymin, xmax, ymax = box_bounds(lon, lat)
    n = int(SIZE / RES)
    dst = np.full((n, n), np.nan, dtype=np.float32)
    dst_transform = from_origin(xmin, ymax, RES, RES)
    with rasterio.open(glo30_url(lon, lat)) as src:
        reproject(
            source=rasterio.band(src, 1),
            destination=dst,
            dst_transform=dst_transform,
            dst_crs=CRS,
            dst_nodata=np.nan,
            resampling=Resampling.bilinear,
        )
    return dst

dem = read_box(10.57, 56.23)
print(dem.shape, "NaNs:", np.isnan(dem).sum(),
      "min:", np.nanmin(dem), "max:", np.nanmax(dem))