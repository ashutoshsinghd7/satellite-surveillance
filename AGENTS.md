# Instructions for AI Coding Agents

I'm building **GeoAgis**, an AI system that fuses optical and SAR satellite imagery over difficult, remote terrain to detect change and assess environmental/terrain hazards. This prototype focuses on optical-only (Sentinel-2) change detection via Google Earth Engine, with terrain and hazard signals, scoped to a single area of interest.

**Before proposing any architectural change, read CONTEXT.md and PROTOTYPE.md in full.** They are the source of truth for scope, reasoning, and constraints. Do not invent reasoning or requirements that aren't in those files.

## Hard Rules (Closed Decisions)

Check DECISIONS.md before proposing an alternative to any architectural choice below—these are closed for the prototype phase:

- **Do not suggest STAC, Planetary Computer, or other data APIs** — we use Google Earth Engine.
- **Do not suggest fine-tuning TerraMind or training a custom model** — TerraMind is frozen/zero-shot only; fine-tuning is deferred post-prototype due to lack of labeled data. If TerraMind integration fails within the 3–4 hour timebox, drop it and fall back to classical signals only.
- **Do not add SAR integration** — optical-only validation is a prerequisite. SAR is explicitly deferred.
- **Do not build multi-timestamp trend analysis or time-series modeling** — T1/T2 pairwise comparisons only.
- **Do not build a human-review write-back loop** — feedback collection is nice-to-have, not demo-critical.

## Repository Structure (Convention)

Place all new code according to this layout (already created as placeholders):

```
├── gee/                    # Google Earth Engine pipelines
│   ├── aoi.py             # AOI definition and retrieval
│   ├── fetch_optical.py   # Sentinel-2 acquisition and compositing
│   ├── indices.py         # NDVI, NDSI, and custom index computation
│   ├── slope.py           # DEM-derived terrain signals
│   └── terramind.py       # TerraMind zero-shot embeddings (frozen)
├── pipeline/              # Fusion and scoring logic
│   ├── fusion.py          # Heuristic evidence fusion (late fusion)
│   ├── scoring.py         # Heuristic score computation per grid cell
│   └── grid.py            # AOI gridding and cell management
├── api/                   # FastAPI backend
│   ├── main.py            # FastAPI app and route handlers
│   └── models.py          # Pydantic models for API responses
├── db/                    # Database schema
│   └── schema.sql         # SQLite schema definition
├── webapp/                # Frontend
│   └── map.html           # Leaflet/folium map interface
├── data/                  # (gitignored) Local data cache
├── tests/                 # Test suite (currently empty)
├── .env.example           # Environment variable template
└── requirements.txt       # Python dependencies
```

Do not create additional top-level directories or deviate from this structure without explicit approval.

## Testing

Tests should go in `tests/`. The directory exists but is empty. How to run tests will be documented as the test suite grows.

## No Implementation Stubs

When creating placeholder files, add exactly one comment line (correct syntax for the file type) describing what will go there, based on CONTEXT.md and PROTOTYPE.md. Do not write function bodies, example code, or "pass" stubs.
