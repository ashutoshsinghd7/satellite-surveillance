# CHECKPOINTS.md

Live task tracker for the prototype. Doubles as the todo list.
Scope is fixed by `PROTOTYPE.md` — a checkpoint is never expanded beyond what it says there.

A checkpoint is "done" only when it has a linked commit/PR and a verifiable output — not by description.

Status values: `not started` / `in progress` / `blocked` / `done`

---

## CP0 — AOI & Event Definition

- **Status:** not started
- **Owner:** —
- **Maps to:** PROTOTYPE.md Step 1
- **Depends on:** nothing (blocking — everything else needs this)
- **Goal:** Lock a 10–15 km AOI anchored on one documented Himalayan landslide event.
- **What needs to be done:**
  - Find a specific event via NASA Global Landslide Catalog, a state disaster-management bulletin, or a news report
  - Confirm its approximate date and location
  - Define the AOI as `ee.Geometry.Rectangle` coordinates
- **Expected output:** `docs/aoi.md` written — bbox coordinates, event source, event date, one-paragraph justification for the extent chosen
- **Verification:** Coordinates load correctly in GEE; AOI visibly contains the cited event location on a basemap
- **What others need to know before starting dependent work:** Nothing downstream (CP1, CP2) can start until this file exists and is frozen.

---

## CP1 — GEE Imagery Acquisition

- **Status:** not started
- **Owner:** —
- **Maps to:** PROTOTYPE.md Step 2
- **Depends on:** CP0
- **Goal:** Pull cloud-masked Sentinel-2 T1/T2 composites and Copernicus DEM for the AOI.
- **What needs to be done:**
  - Sentinel-2 L2A from `COPERNICUS/S2_SR_HARMONIZED`, two median composites (T1 pre-monsoon, T2 post-monsoon, 4–6 week windows)
  - Cloud mask via SCL band
  - Copernicus DEM pull for the same AOI
  - **Publish the export contract early** (band names, resolution, file format) — CP2, CP3, CP4 all consume this
- **Expected output:** Saved T1/T2 composites + DEM raster for the AOI, viewable; `docs/datasources.md` written with exact collection IDs and date windows used
- **Verification:** Composites visually inspect as cloud-free (or near enough) over the AOI; DEM covers full AOI extent with no gaps
- **What others need to know:** The export format (resolution, projection, file type) must be agreed and shared before CP2/CP3 start, not discovered after CP1 finishes.

---

## CP2 — Terrain / Slope Layer

- **Status:** not started
- **Owner:** —
- **Maps to:** PROTOTYPE.md Step 3
- **Depends on:** CP0 + the DEM export contract from CP1 (not full CP1 completion — can start once the contract is agreed)
- **Goal:** Slope/aspect layer from the DEM, used as a soft plausibility filter.
- **What needs to be done:**
  - `ee.Terrain.slope()` on the DEM
  - 15°–45° threshold band used downstream as a soft mask (near-boundary cases pass through with reduced confidence, not dropped)
- **Expected output:** Slope raster for the AOI, queryable per-pixel or per-cell
- **Verification:** Spot-check known flat valley floor and known steep cliff in the AOI — both should fall outside the 15°–45° band
- **What others need to know:** CP5 (fusion) consumes this as one of the signals — output format (raster vs. per-cell value) should match what CP6's grid expects.

---

## CP3 — NDVI / NDSI Delta

- **Status:** not started
- **Owner:** —
- **Maps to:** PROTOTYPE.md Step 4
- **Depends on:** CP1's T1/T2 composites
- **Goal:** Compute NDVI and NDSI at T1/T2, difference them, flag AOI-local statistical outliers.
- **What needs to be done:**
  - NDVI and NDSI from T1/T2 bands
  - NDVI_delta flagged where it's an AOI-local outlier (mean − 2σ, not a hardcoded value)
  - NDSI delta checked to rule out snowmelt/snowfall mimicking the drop — **decide and document how** (hard gate vs. weighted input) before writing code, not while writing it
- **Expected output:** NDVI/NDSI delta raster + list of flagged candidate pixels/cells
- **Verification:** Flagged pixels visually overlap vegetation loss in true-color before/after imagery, not shadow or water
- **What others need to know:** The NDSI-gate decision affects CP5's fusion logic — resolve and note it in `DECISIONS.md` before CP5 starts.

---

## CP4 — TerraMind Zero-Shot Signal

- **Status:** not started
- **Owner:** —
- **Maps to:** PROTOTYPE.md Step 5
- **Depends on:** technically needs T1/T2 patches, but should start **in parallel with CP0/CP1 using a throwaway sample patch** — the real risk here is environment/integration, not AOI-specific, so don't wait on CP0 to find that out
- **Hard constraint:** 3–4 hour timebox (per `DECISIONS.md`). If no working embedding-distance raster by the cutoff, drop it, log it in `DECISIONS.md` as attempted-and-deferred, and proceed with 3 classical signals only.
- **What needs to be done:**
  - Install TerraTorch, download TerraMind 1.0 weights
  - Confirm input formatting (band order, patch size, normalization)
  - Pass T1/T2 patches through frozen backbone, compute per-patch embedding distance (cosine or L2)
- **Expected output:** Either a working embedding-distance raster, or a logged deferral in `DECISIONS.md`
- **Verification:** If successful — spot-check that high-distance patches correspond to visibly different T1/T2 imagery, not noise
- **What others need to know:** CP5 must work with 3 OR 4 signals — do not build CP5 assuming CP4 succeeds.

---

## CP5 — Evidence Fusion + Heuristic Scoring

- **Status:** not started
- **Owner:** —
- **Maps to:** PROTOTYPE.md Step 6
- **Depends on:** CP2, CP3, CP4-or-its-deferral
- **Goal:** Combine the available signals into one priority score per grid cell via a hand-specified heuristic.
- **What needs to be done:**
  - Define the heuristic (start equal-weighted across available signals; document the exact formula in `docs/research.md` or inline comments)
  - Must gracefully accept 3 or 4 signals depending on CP4's outcome
  - Confidence should fold in data quality (cloud %, T1/T2 time gap)
- **Expected output:** Per-cell priority score + confidence value
- **Verification:** Cells overlapping the known event (from CP0) rank among the highest-scored
- **What others need to know:** CP6 needs the exact output schema (fields, types) before it can be scaffolded — publish this early, ideally before CP5 is fully done, so CP6 can build against mock data.

---

## CP6 — Gridding + SQLite Storage

- **Status:** not started
- **Owner:** —
- **Maps to:** PROTOTYPE.md Step 7
- **Depends on:** CP5's output schema (can scaffold against a mocked schema before CP5 finishes)
- **Goal:** Divide the AOI into a grid, store each cell's fused score and metadata.
- **What needs to be done:**
  - Define grid resolution over the AOI
  - SQLite schema: location, score, component signals, confidence, status
  - Write the schema to `docs/datasources.md` or a dedicated schema note before building against it
- **Expected output:** Populated SQLite DB with one row per grid cell
- **Verification:** Query returns the expected number of cells; a cell near the known event has a high score and all three/four component signals populated
- **What others need to know:** CP7 reads this schema directly — don't change field names without telling whoever owns CP7.

---

## CP7 — FastAPI Layer

- **Status:** not started
- **Owner:** —
- **Maps to:** PROTOTYPE.md Step 8
- **Depends on:** CP6's schema (can scaffold against a mock DB before CP6 is live)
- **Goal:** Serve grid cells as GeoJSON from SQLite.
- **What needs to be done:**
  - Endpoint(s) returning cell location, score, confidence, contributing signals as GeoJSON
  - Confirm auto-generated docs (`/docs`) work as a manual test surface
- **Expected output:** Running FastAPI app, GeoJSON response verified via `/docs` or curl
- **Verification:** Response validates as GeoJSON; cell count matches CP6's DB
- **What others need to know:** CP8 needs the exact response shape (field names, geometry format) — freeze this before CP8 starts building against it.

---

## CP8 — Frontend (Leaflet / folium)

- **Status:** not started
- **Owner:** —
- **Maps to:** PROTOTYPE.md Step 9
- **Depends on:** CP7's API contract (can scaffold against mocked GeoJSON before CP7 is live)
- **Goal:** Map showing AOI boundary, alert-cell overlay (colored/sized by score), before/after imagery toggle.
- **What needs to be done:**
  - Render AOI boundary
  - Render alert cells from the API, styled by score
  - Before/after true-color toggle using CP1's composites
- **Expected output:** A page that opens in a browser and shows the AOI with alert cells
- **Verification:** Highest-scored cells visually cluster near the known event location

---

## Known Overflow Risks (not separate checkpoints, but expect spillover)

- **Threshold tuning** (NDVI σ-multiplier, slope bounds, fusion weights) is explicitly unvalidated per `PROTOTYPE.md` and will likely need a second pass after CP0's real event data is available. Don't treat CP3/CP5 as closed after one pass.
- **Scope check:** before CP0 starts, confirm `PROTOTYPE.md`'s optical-only, single-AOI, single-pair scope still holds — there's a noted tension with later SAR/constellation plans. If scope has changed, update `PROTOTYPE.md` first; don't let checkpoints drift from a stale spec.

---

## Dependency Graph

```
CP0 ─┬─→ CP1 ─┬─→ CP3 ─┐
     │        │        ├─→ CP5 → CP6 → CP7 → CP8
     └─→ CP2 ─┘   CP4* ┘

* CP4 started early/in parallel with CP0, decoupled via a throwaway sample patch.
```
