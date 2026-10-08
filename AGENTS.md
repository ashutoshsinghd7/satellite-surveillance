# Instructions for AI Coding Agents

I'm building **GeoAgis**, an AI system that fuses optical and SAR satellite imagery over difficult, remote terrain to detect change and assess environmental and terrain hazards. This prototype focuses on optical-only Sentinel-2 change detection through Google Earth Engine, with terrain and hazard signals, scoped to one area of interest.

`CONTEXT.md` and `PROTOTYPE.MD` are the full source of truth for scope, reasoning, constraints, and the prototype plan. Read both files in full before proposing any architectural change. Do not invent requirements or reasoning that are not in those files.

## Closed decisions

Check `DECISIONS.md` before proposing an alternative to an existing architectural decision. These decisions are closed for the prototype phase:

- Do not suggest STAC, Microsoft Planetary Computer, or another data API; this prototype uses Google Earth Engine.
- Do not suggest fine-tuning TerraMind or training a custom model; TerraMind is frozen and zero-shot only. If its integration fails within the 3–4 hour timebox, fall back to classical signals only.
- Do not add SAR integration; optical-only validation is a prerequisite and SAR is explicitly deferred.
- Do not build multi-timestamp trend analysis or time-series modeling; use T1/T2 pairwise comparisons only.
- Do not build a human-review write-back loop; feedback collection is nice-to-have and not demo-critical.

## Off-limits for this prototype

- SAR integration.
- TerraMind fine-tuning or custom model training.
- Multi-timestamp trend analysis or time-series modeling.
- Human-review write-back or feedback loops.

## Repository structure convention

Place new code in the existing layout below. Do not create additional top-level directories or deviate from this structure without explicit approval.

```text
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
├── data/                  # Gitignored local data cache
├── tests/                 # Test suite
├── .env.example           # Environment variable template
└── requirements.txt       # Python dependencies
```

## Testing

The `tests/` directory exists but is currently empty. The instructions for running tests will be documented as the test suite grows.

## No implementation stubs

When creating placeholder files, add exactly one comment line using the correct syntax for the file type. Describe what will go there based on `CONTEXT.md` and `PROTOTYPE.MD`. Do not write function bodies, example code, or `pass` stubs.