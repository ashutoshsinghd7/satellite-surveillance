# Decisions Log

### GEE over Microsoft Planetary Computer / STAC
**Date:** 2026-10-08
**Decision:** Use Google Earth Engine (GEE) as the primary data access and processing layer for this prototype.
**Why:** Free compute at prototype scale, server-side processing so raw tiles aren't downloaded locally, Python API keeps it scriptable and portable into the larger pipeline, and established precedent in geospatial research.
**Alternatives I considered and rejected:** 
- Microsoft Planetary Computer with STAC — adds cloud storage API complexity and doesn't offer free compute; defer to a later scaling phase if moving beyond GEE's quotas.
- Direct tile download from AWS/USGS — manual preprocessing burden; GEE handles it server-side.

---

### Optical-First (Sentinel-2), SAR Explicitly Deferred
**Date:** 2026-10-08
**Decision:** Build the entire first prototype using optical imagery only (Sentinel-2); do not integrate SAR until the optical baseline is validated.
**Why:** SAR adds a separate preprocessing chain (speckle filtering, different calibration, different interpretation semantics). Without validating the optical pipeline works at all, adding SAR complexity is premature; the optical-only validation is the prerequisite for SAR integration.
**Alternatives I considered and rejected:**
- Optical + SAR from day one — too much surface area before proving the baseline works.
- SAR-only — optical is simpler, more directly interpretable, and the default starting point in the literature.

---

### Heuristic Priority Scoring, Not Learned Ranker at This Stage
**Date:** 2026-10-08
**Decision:** Use hand-specified heuristic rules (weighted combination of NDVI/NDSI delta, slope plausibility, TerraMind distance) to score grid cells; do not train a learned ranker.
**Why:** No validated ground-truth outcomes exist yet to train a ranker on. A heuristic is fully auditable — you can state exactly why a cell ranked high ("NDVI drop + plausible slope + TerraMind agreement") and debug disagreements between signals. Late fusion (combine scores, not raw signals into one model) keeps each signal inspectable—a necessity at this stage.
**Alternatives I considered and rejected:**
- Train a ranker immediately — no labeled outcomes to learn from; early overfit would waste time.
- Single monolithic model (e.g., CNN end-to-end) — loses interpretability; can't debug which signal is firing.

---

### TerraMind Frozen/Zero-Shot, Not Fine-Tuned
**Date:** 2026-10-08
**Decision:** Use TerraMind 1.0 as a frozen feature extractor (pretrained backbone only); do not fine-tune the U-Net decoder. If the integration doesn't work within a 3–4 hour timebox, drop TerraMind entirely and fall back to classical signals only.
**Why:** Fine-tuning requires labeled Himalayan landslide data, which doesn't exist yet—that's a multi-week labeling effort once a labeling pipeline exists and a Day-2 priority. Zero-shot embeddings can still act as a fourth independent evidence signal (consistent with late-fusion philosophy), and the timebox/fallback keeps scope bounded. If TerraMind install, weight download, and input normalization (band order, patch size) prove too complex, a validated classical-signals-only baseline is better than a failed attempt.
**Alternatives I considered and rejected:**
- Fine-tune TerraMind now — no labels; premature and out of scope.
- Embedding clustering/anomaly scoring — more sophisticated, not worth added complexity for a first pass.
- Skip TerraMind entirely — valid safety fallback; classical signals alone are sufficient and already proven elsewhere.

---

### SQLite Over PostgreSQL/PostGIS at Prototype Stage
**Date:** 2026-10-08
**Decision:** Use SQLite for prototype storage; migrate to PostgreSQL/PostGIS only if the project grows past a single AOI with concurrent write access needs.
**Why:** File-based, zero setup, appropriate at prototype scale with one AOI and asynchronous (single-writer) updates. PostgreSQL/PostGIS add operational overhead (process management, schema migrations, connection pooling) not justified yet.
**Alternatives I considered and rejected:**
- PostgreSQL from day one — overkill complexity; adds deployment/DevOps burden at a stage when the data model itself is still being validated.
- Cloud data warehouse (BigQuery, Snowflake) — not necessary for a 10–15 km AOI; premature scaling.

---

### Web App (FastAPI + Leaflet/Folium), Not Notebook Deliverable
**Date:** 2026-10-08
**Decision:** Build the prototype as a running web app (FastAPI backend serving GeoJSON, Leaflet/folium HTML frontend), not as a Jupyter notebook.
**Why:** A notebook-rendered map only lives inside a running kernel and isn't shareable; a served HTML page is actually openable by someone else, clickable, and demonstrates the real form factor expected for the full system. FastAPI matches existing backend stack (continuity), is async-capable if scaling is needed later, and auto-generates interactive API docs.
**Alternatives I considered and rejected:**
- geemap in Jupyter — maps only live in the notebook; not shareable without the kernel running.
- Static GeoJSON dump + manual map rendering — loses interactivity and the real-time query capability.

---

### NDVI/NDSI Delta + Slope Filter + AOI-Local Statistical Thresholding
**Date:** 2026-10-08
**Decision:** Use decades-old, fully interpretable signals (NDVI and NDSI deltas) with an AOI-local statistical threshold (mean − 2σ, not a fixed hardcoded value) and slope plausibility as a separate gate (not blended into one score).
**Why:** NDVI/NDSI are trivial to compute and fully interpretable—if this signal and others disagree, that disagreement is itself useful debugging information, not noise to average away. AOI-local thresholds generalize better than fixed values (vegetation density varies by AOI). Slope as a separate gate (15°–45° plausibility mask, not hard cutoff) means terrain filtering is transparent and debuggable; near-boundary cases still pass through with reduced confidence.
**Alternatives I considered and rejected:**
- Hardcoded NDVI thresholds — won't generalize across AOIs with different baseline vegetation.
- Fold all signals into one composite score immediately — loses interpretability; can't audit why a cell ranked high or debug disagreements.
- Skip slope entirely — increases false positives in implausible terrain (flat valleys, vertical cliffs).
