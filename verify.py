"""CP1 verification: check data/raw/*.tif against the export contract.

Usage (repo root, venv active):
    pip install rasterio numpy matplotlib
    python -m gee.verify
Writes data/preview_cp1.png and prints PASS/FAIL per check.
"""
import json
from pathlib import Path

import matplotlib
import numpy as np
import rasterio
from rasterio.warp import transform

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from acquire import json_block  # noqa: E402

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "data" / "raw"
aoi = json_block(ROOT / "docs" / "aoi.md")
cfg = json_block(ROOT / "docs" / "datasources.md")
exp = cfg["export"]
n_bands = len(cfg["s2"]["bands"]) + 1  # + valid_count

fails = []


def check(ok, msg):
    print(("PASS  " if ok else "FAIL  ") + msg)
    if not ok:
        fails.append(msg)



def stretch(band):
    band = np.asarray(band, dtype=np.float32)
    valid = np.isfinite(band)

    if not valid.any():
        return np.zeros(band.shape, dtype=np.float32)

    low, high = np.percentile(band[valid], [2, 98])

    if high <= low:
        return np.zeros(band.shape, dtype=np.float32)

    result = np.zeros(band.shape, dtype=np.float32)
    result[valid] = np.clip(
        (band[valid] - low) / (high - low), 0, 1
    )

    return result


with rasterio.open(RAW / "dem.tif") as d:
    dem = d.read(1)
    grid = (d.shape, d.transform, d.crs)
    dem_crs, dem_tf = d.crs, d.transform
footprint = np.isfinite(dem) & (dem > 0)
check(footprint.mean() > 0.5, f"DEM footprint covers {footprint.mean():.0%} of the raster")
check(str(dem_crs).endswith("32643"), f"DEM CRS = {dem_crs}")
check(abs(dem_tf.a) == exp["scale_m"], f"DEM pixel size = {abs(dem_tf.a)} m")
print(f"      DEM elevation range: {dem[footprint].min():.0f}..{dem[footprint].max():.0f} m")

x, y = transform("EPSG:4326", dem_crs, [aoi["event_point_wgs84"][0]], [aoi["event_point_wgs84"][1]])
er, ec = rasterio.transform.rowcol(dem_tf, x[0], y[0])

fig, ax = plt.subplots(2, 3, figsize=(15, 10))
ax[1, 2].imshow(np.where(footprint, dem, np.nan), cmap="gray")
ax[1, 2].set_title("DEM")

for i, key in enumerate(("T1", "T2")):
    with rasterio.open(RAW / f"s2_{key}.tif") as s:
        arr = s.read().astype("float32")
        same = (s.shape, s.transform, s.crs) == grid
        crs_ok = str(s.crs).endswith("32643")
    bands = json.loads((RAW / f"s2_{key}.bands.json").read_text())
    check(arr.shape[0] == n_bands, f"{key}: {arr.shape[0]} bands (expected {n_bands})")
    check(len(bands) == arr.shape[0], f"{key}: sidecar lists {len(bands)} bands")
    check(same and crs_ok, f"{key}: same grid/CRS as DEM")
    vc = arr[-1]
    nodata = ((vc == 0) & footprint).sum() / footprint.sum()
    check(nodata < 0.05, f"{key}: {nodata:.1%} of in-AOI pixels have no clean observation")
    print(f"      {key}: valid_count median {np.median(vc[footprint]):.0f}, max {vc.max():.0f}")
    refl = arr[:-1][:, footprint]
    check(0 <= np.nanmin(refl) and np.nanmax(refl) < 1.5,
          f"{key}: reflectance range {np.nanmin(refl):.3f}..{np.nanmax(refl):.3f}")
    # true colour = B4,B3,B2 -> band positions 4,3,2 (1-based)
    rgb = np.dstack([stretch(arr[3]), stretch(arr[2]), stretch(arr[1])])
    rgb[~footprint] = 1
    ax[0, i].imshow(rgb)
    ax[0, i].plot(ec, er, "r+", ms=18, mew=2)
    ax[0, i].set_title(f"{key} true colour (B4,B3,B2); red + = event point")
    ax[1, i].imshow(np.where(footprint, vc, np.nan), cmap="viridis")
    ax[1, i].set_title(f"{key} valid_count (clean observations per pixel)")
ax[0, 2].axis("off")
ax[0, 2].text(0, 0.5, "Zoom in on the red + in both\ntrue-colour panels and compare.", fontsize=12)

out = ROOT / "data" / "preview_cp1.png"
fig.tight_layout()
fig.savefig(out, dpi=110)
print(f"\nPreview written to {out}")
print("ALL CHECKS PASSED" if not fails else f"{len(fails)} CHECK(S) FAILED")
