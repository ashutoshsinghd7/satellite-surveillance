# Data sources — GEE acquisition (CP1)

Single source of truth for dataset IDs, date windows and the export contract. Code reads the JSON block below.

```json
{
  "s2": {
    "collection": "COPERNICUS/S2_SR_HARMONIZED",
    "bands": ["B1","B2","B3","B4","B5","B6","B7","B8","B8A","B9","B11","B12"],
    "reflectance_scale": 0.0001,
    "max_scene_cloud_pct": 60,
    "scl_mask_classes": [1, 3, 8, 9, 10],
    "composite": "median"
  },
  "dem": {"collection": "COPERNICUS/DEM/GLO30", "band": "DEM", "export_band_name": "elevation"},
  "export": {"crs": "EPSG:32643", "scale_m": 20, "format": "GeoTIFF", "dtype": "float32", "out_dir": "data/raw"}
}
```

## Run config (read by gee/acquire.py)
`aoi` must match `name` in docs/aoi.md. `end` is inclusive.

```yaml
aoi: kali_dhank_barwas

t1:
  start: 2021-04-15
  end: 2021-05-31

t2:
  start: 2021-10-01
  end: 2021-11-15

```
## Export contract (CP2 / CP3 / CP4 consume this)
- Files in `data/raw/`: `s2_T1.tif`, `s2_T2.tif`, `dem.tif`, each with a `<name>.bands.json` sidecar listing band order (GeoTIFF band names are not preserved by GEE downloads).
- `s2_T1.tif` / `s2_T2.tif`: 13 bands = the 12 bands above in that order + `valid_count` (number of unmasked observations per pixel; 0 means no data, not "no change"). Reflectance 0–1, float32.
- `dem.tif`: 1 band `elevation`, metres, float32, same grid as the composites.
- All three: EPSG:32643 (UTM 43N), 20 m, identical extent.
- Resampling: GEE default (nearest) when going 10 m -> 20 m; acceptable for the prototype.
- Band set includes B1 and B9 (and excludes B10) so CP4 can feed TerraMind; CP4's owner should confirm the exact band list it needs.

## Notes
- Cloud mask: SCL classes 1 (saturated), 3 (cloud shadow), 8/9 (cloud), 10 (cirrus). Snow (11) is kept for NDSI.
- Slope (CP2): the Copernicus DEM mosaic loses its projection; `acquire.py` restores it with `setDefaultProjection` so `ee.Terrain.slope()` works server-side.
- Window caveat: the event is 2021-07-30. T1/T2 must straddle it (T1 before, T2 after) or the pipeline has no change to detect. The 2025 windows above both fall years after the event, so the scar is present in both composites; use them only for pipeline/plumbing tests, not for validation. For validation use e.g. T1 2021-04-15..2021-05-31 and T2 2021-10-01..2021-11-15.
- T1 (Apr–May) vs T2 (Oct–Nov) differ in vegetation season; AOI-local outlier thresholds should absorb a broad NDVI rise. Log the final window decision in DECISIONS.md.

