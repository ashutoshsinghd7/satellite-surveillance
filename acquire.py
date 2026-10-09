"""CP1 - GEE imagery acquisition.

Reads docs/aoi.md and docs/datasources.md (single sources of truth), builds two
cloud-masked Sentinel-2 median composites (T1/T2) plus the Copernicus DEM, and
downloads them as GeoTIFFs to data/raw/ on the contract grid.

Usage:
    export GEE_PROJECT=<your-gee-cloud-project>
    earthengine authenticate        # once
    python -m gee.acquire
"""
import json
import os
import re
from datetime import date, timedelta
from pathlib import Path

import ee
import requests
import yaml

ROOT = Path(__file__).resolve().parent


def fenced_block(md_path: Path, lang: str) -> str:
    text = md_path.read_text(encoding="utf-8")
    m = re.search(rf"```{lang}\n(.*?)\n```", text, re.S)
    if not m:
        raise ValueError(f"No ```{lang} block found in {md_path}")
    return m.group(1)


def json_block(md_path: Path) -> dict:
    return json.loads(fenced_block(md_path, "json"))


def yaml_block(md_path: Path) -> dict:
    return yaml.safe_load(fenced_block(md_path, "yaml"))


def end_exclusive(end) -> str:
    """Config `end` is inclusive; GEE filterDate end is exclusive."""
    d = end if isinstance(end, date) else date.fromisoformat(str(end))
    return (d + timedelta(days=1)).isoformat()


def s2_composite(aoi, start, end_excl, cfg):
    bands = cfg["s2"]["bands"]
    bad_classes = cfg["s2"]["scl_mask_classes"]

    def mask_scl(img):
        scl = img.select("SCL")
        bad = ee.Image(0)
        for c in bad_classes:
            bad = bad.Or(scl.eq(c))
        return img.updateMask(bad.Not())

    coll = (
        ee.ImageCollection(cfg["s2"]["collection"])
        .filterBounds(aoi)
        .filterDate(start, end_excl)
        .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", cfg["s2"]["max_scene_cloud_pct"]))
    )
    n = coll.size().getInfo()
    if n == 0:
        raise RuntimeError(f"No S2 scenes for {start}..{end_excl}; widen window or cloud filter")

    masked = coll.map(mask_scl)
    comp = masked.select(bands).median().multiply(cfg["s2"]["reflectance_scale"]).toFloat()
    valid = masked.select("B4").count().rename("valid_count").toFloat()
    return comp.addBands(valid).clip(aoi), n


def dem_image(aoi, cfg):
    coll = ee.ImageCollection(cfg["dem"]["collection"]).filterBounds(aoi).select(cfg["dem"]["band"])
    proj = coll.first().projection()  # mosaic() drops projection; restore for slope later
    dem = coll.mosaic().setDefaultProjection(proj).rename(cfg["dem"]["export_band_name"])
    return dem.toFloat().clip(aoi)


def download(img, name, region, export, band_names):
    out_dir = ROOT / export["out_dir"]
    out_dir.mkdir(parents=True, exist_ok=True)
    url = img.getDownloadURL({
        "region": region,
        "crs": export["crs"],
        "scale": export["scale_m"],
        "format": "GEO_TIFF",
    })
    resp = requests.get(url, timeout=600)
    resp.raise_for_status()
    tif = out_dir / f"{name}.tif"
    tif.write_bytes(resp.content)
    (out_dir / f"{name}.bands.json").write_text(json.dumps(band_names, indent=2))
    print(f"wrote {tif} ({len(resp.content) / 1e6:.1f} MB), bands={len(band_names)}")


def main():
    ee.Initialize(project=os.environ.get("GEE_PROJECT"))
    aoi_cfg = json_block(ROOT / "docs" / "aoi.md")
    cfg = json_block(ROOT / "docs" / "datasources.md")
    run = yaml_block(ROOT / "docs" / "datasources.md")
    if run["aoi"] != aoi_cfg["name"]:
        raise ValueError(f"run config aoi '{run['aoi']}' != docs/aoi.md name '{aoi_cfg['name']}'")

    west, south, east, north = aoi_cfg["bbox_wgs84"]
    aoi = ee.Geometry.Rectangle([west, south, east, north])
    export = cfg["export"]

    for key in ("T1", "T2"):
        w = run[key.lower()]
        start, end_x = str(w["start"]), end_exclusive(w["end"])
        img, n = s2_composite(aoi, start, end_x, cfg)
        print(f"{key}: {n} scenes, {start}..{w['end']} inclusive")
        download(img, f"s2_{key}", aoi, export, cfg["s2"]["bands"] + ["valid_count"])

    download(dem_image(aoi, cfg), "dem", aoi, export, [cfg["dem"]["export_band_name"]])


if __name__ == "__main__":
    main()
