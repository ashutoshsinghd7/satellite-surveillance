# GeoAgis Prototype

I'm building an AI system that fuses optical and SAR satellite imagery over difficult, remote terrain to continuously detect change, assess terrain and environmental hazards, and deliver interpretable, confidence-rated intelligence to decision-makers—not stopping at image classification, but turning raw imagery into actionable intelligence. The core problem I'm solving: physical and drone surveillance in high-altitude terrain (starting with the Himalayas) is unreliable due to cloud cover, snow, cold, restricted access, and battery limits, while satellites can cover these gaps—but imagery volume is far too large to review manually.

**Current Status:** The macro project is in concept phase. I'm actively building a 3–4 day optical-only prototype as a running web app (not a notebook), scoped to a single area of interest with a documented landslide event.

## Setup & Run (to be filled in as each step is built)

### Prerequisites
- Python 3.9+
- Google Earth Engine account with authentication

### Installation
- Create a virtual environment: `python -m venv venv`
- Activate it: `source venv/bin/activate` (or `venv\Scripts\activate` on Windows)
- Install dependencies: `pip install -r requirements.txt`
- Authenticate with Google Earth Engine: `earthengine authenticate`

### Running the App
- Start the FastAPI backend: `uvicorn api.main:app --reload`
- Open the webapp: navigate to `http://localhost:8000` and open `webapp/map.html`

## What This Prototype Does

Optical-only (Sentinel-2) pipeline via Google Earth Engine on one 10–15 km area of interest anchored on a documented Himalayan landslide event. It computes NDVI/NDSI delta + applies a slope filter + uses TerraMind (frozen, zero-shot only) as a fourth independent evidence signal → produces a heuristic priority score per grid cell → stores results in SQLite → serves them via FastAPI as GeoJSON → displays them on a Leaflet/folium web map with before/after true-color imagery.

## Explicitly Out of Scope (This Prototype)

- **SAR** — adds a whole separate preprocessing chain (speckle filtering, different calibration). Validate the optical baseline works at all before adding a second sensor's complexity.
- **Fine-tuning TerraMind's U-Net decoder** — requires labeled data we don't have. TerraMind is used frozen/zero-shot only.
- **Human review write-back loop** — nice-to-have, not demo-critical.
- **Multi-timestamp trend analysis** — T1/T2 pairwise only, no time series.
