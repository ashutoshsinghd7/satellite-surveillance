# GeoAgis

were building GeoAgis, an AI system that fuses optical and SAR satellite imagery over difficult, remote terrain—starting with the Himalayas—to continuously detect change, assess terrain and environmental hazards, and deliver interpreted, confidence-rated intelligence. Physical and drone surveillance in high-altitude terrain is unreliable because of cold, snowfall, cloud cover, rugged terrain, battery limits, and restricted access; satellite imagery helps cover those gaps, but the volume is too large to review manually. The goal is to move from raw imagery to detected change to interpreted, confidence-rated intelligence rather than stopping at image classification.

## Current status

The macro project is in the concept phase. I'm actively building a 3–4 day optical-only prototype as a running web app, not a notebook. The prototype is scoped to one 10–15 km AOI anchored on a documented Himalayan landslide event.

## Setup and run

> To be filled in as each step is built.

1. Create and activate a Python virtual environment.
2. Install dependencies from `requirements.txt`.
3. Authenticate Google Earth Engine.
4. Run the FastAPI application.
5. Open the Leaflet/folium web interface.

## Prototype scope

**In scope:** optical-only (Sentinel-2) pipeline via GEE on one 10–15 km AOI with a documented landslide event. NDVI/NDSI delta + slope filter + TerraMind (frozen, zero-shot) → heuristic score per grid cell → SQLite → FastAPI/GeoJSON → Leaflet/folium map with before/after true-color imagery.

## Explicitly out of scope

- **SAR** — adds a whole separate preprocessing chain (speckle filtering, different calibration). Validate the optical baseline works at all before adding a second sensor's complexity.
- **Fine-tuning TerraMind's U-Net decoder** — requires labeled data you don't have. TerraMind is used frozen/zero-shot only.
- **Human review write-back loop** — nice-to-have, not demo-critical.
- **Multi-timestamp trend analysis** — T1/T2 pairwise only, no time series.

See `CONTEXT.md`, `PROTOTYPE.MD`, and `DECISIONS.md` for the source-of-truth context, prototype plan, and closed decisions.
