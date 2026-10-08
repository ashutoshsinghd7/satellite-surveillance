# Prototype — Himalayan Landslide Detection Web App

**Status:** not yet built. 3–4 day build target.

**Relationship to CONTEXT.md:** this is one narrow instantiation of "Change Intelligence" (plus partial Terrain Intelligence and Confidence) from the macro pipeline — scoped to a single AOI, optical-only sensing, heuristic (not learned) scoring, served as a real web app rather than a notebook. Nothing here is the project's final architecture; it's the first demoable slice.

**Form factor:** a running web app — FastAPI backend serving alert data, a Leaflet/folium map frontend a person can actually open and click around in. Not a notebook. This matters for tech choices below: every component needs to be servable, not just runnable once interactively.

---

## Scope

**In scope:** optical-only (Sentinel-2) pipeline via GEE on one 10–15 km AOI with a documented landslide event. NDVI/NDSI delta + slope filter + TerraMind (frozen, zero-shot) → heuristic score → grid alerts → API → map.

**Explicitly out of scope:**
- **SAR** — adds a whole separate preprocessing chain (speckle filtering, different calibration). Validate the optical baseline works at all before adding a second sensor's complexity.
- **Fine-tuning TerraMind's U-Net decoder** — requires labeled data you don't have. TerraMind is used frozen/zero-shot only (see Step 5).
- **Human review write-back loop** — nice-to-have, not demo-critical.
- **Multi-timestamp trend analysis** — T1/T2 pairwise only, no time series.

---

## Pipeline

### Step 1 — AOI Definition

**What:** A 10–15 km bounding box anchored on a documented Himalayan landslide event (not an arbitrary coordinate).

**Why:** Small enough to visually and programmatically validate against something real; without a known event to check against, there's no way to tell a real detection from noise.

**Technical choice:** define via `ee.Geometry.Rectangle`, coordinates hardcoded in `DATA_SOURCES.md` once finalized — not re-derived per run.

**Questions to resolve before building:** which specific documented event (source: news report, state disaster-management bulletin, or NASA Global Landslide Catalog), and its approximate date/location?

---

### Step 2 — Imagery Acquisition (GEE)

**What:** Sentinel-2 L2A from `COPERNICUS/S2_SR_HARMONIZED`, two cloud-masked median composites (T1 pre-monsoon, T2 post-monsoon, 4–6 week windows), plus Copernicus DEM for the same AOI.

**Why L2A:** already atmospherically corrected — no need to build correction yourself.

**Why composites, not single dates:** a single Himalayan pass has a real chance of total cloud cover; a multi-week median gives a usable image even when no single date is clean.

**Why pre/post-monsoon:** most Himalayan landslides are monsoon-triggered — this window maximizes the odds the event actually falls between your two snapshots.

**Why GEE as the access layer (reconfirmed here):** free compute at prototype scale, server-side processing so you're not downloading raw tiles, Python API keeps it scriptable and portable into the backend (not a one-off notebook operation).

**Cloud masking:** SCL band (ships with S2_SR_HARMONIZED, zero extra cost) — good enough for prototype; upgrade to `s2cloudless` only if SCL visibly under-masks.

---

### Step 3 — Terrain Context (DEM / Slope)

**What:** Slope (and aspect) computed from Copernicus DEM (30m) over the same AOI.

**Why:** Landslides occur within a plausible slope-angle range (not flat valley floors or vertical cliffs). This is a cheap, deterministic filter that rules out geomorphologically implausible detections before they ever reach scoring — no model needed for this signal.

**Technical choice:** `ee.Terrain.slope()` on the DEM, threshold band 15°–45° used downstream as a mask, not a hard cutoff (near-boundary cases still pass through with reduced confidence rather than being silently dropped).

---

### Step 4 — Classical Change Signals (NDVI / NDSI Delta)

**What:** NDVI and NDSI computed on T1 and T2, differenced. Candidate pixels flagged where NDVI_delta is a statistical outlier (AOI-local mean − 2σ, not a hardcoded value) — a landslide strips vegetation, producing a sharp, localized NDVI drop. NDSI delta checked to rule out snowmelt/snowfall mimicking the same drop.

**Why these specific indices:** decades-old, trivial to compute, fully interpretable — if this signal and others disagree, that disagreement is itself useful information, not noise to average away.

**Why AOI-local threshold, not fixed:** a fixed NDVI-drop value won't generalize across AOIs with different baseline vegetation density; calibrating from the AOI's own distribution is cheap and self-adjusting.

**Why slope-mask here (Step 3) rather than fold into one combined score immediately:** keeping terrain plausibility as a separate gate — not blended into one number — means a human (or you, debugging) can later see exactly which check a false positive failed, not just that "the score was low."

---

### Step 5 — TerraMind (Frozen, Zero-Shot Fourth Signal)

**What:** TerraMind 1.0 used as a frozen feature extractor, not fine-tuned. T1 and T2 image patches passed through the pretrained backbone; per-patch embedding distance (cosine or L2) between T1 and T2 embeddings computed. A large distance = the model perceives structural change, independent of whether it's labeled.

**Why frozen instead of fine-tuning the U-Net decoder:** fine-tuning needs labeled Himalayan landslide data, which doesn't exist yet — that's a multi-week effort once a labeling pipeline exists, not a prototype-week task. Zero-shot embedding distance needs no labels at all and still lets TerraMind's pretraining (general EO structure: terrain, vegetation, land cover) contribute something.

**Why include it at all, given the cost:** it's framed as a fourth *independent* evidence signal alongside NDVI/NDSI delta and slope — consistent with the project's late-fusion philosophy (every signal stays inspectable, nothing is blended into one opaque score). If it adds nothing beyond the classical signals, that's a legitimate, loggable finding, not a wasted effort.

**Real risk, stated plainly:** TerraTorch install, weight download, and correct input formatting (band order, patch size, normalization) are new integration surface with no prior experience to draw on — this is the single most likely thing to blow the build timebox.

**Technical choice — hard mitigation, not a hope:** this step is timeboxed (3–4 hrs). If a working embedding-distance raster isn't produced by the cutoff, **drop TerraMind for this prototype**, log it in `DECISIONS.md` as attempted-and-deferred, and proceed with the three classical signals only. The fusion step (Step 6) is built to accept 3 or 4 signals without a redesign, specifically so this fallback costs nothing structurally.

**Alternatives considered:**
- *Fine-tune now* — rejected, no labels.
- *Skip TerraMind entirely* — the safe fallback, already a validated-enough baseline on its own.
- *Embedding clustering/anomaly scoring instead of raw distance* — more sophisticated, not worth the added complexity for a first pass.

---

### Step 6 — Evidence Fusion + Heuristic Scoring

**What:** Combine NDVI/NDSI delta, slope plausibility, and (if it survived Step 5) TerraMind embedding distance into a single priority score per grid cell, via a hand-specified heuristic — not a trained model.

**Why heuristic, not learned:** no validated ground-truth outcomes exist yet to train a ranker on. A heuristic is fully auditable — you can state exactly why a cell ranked high ("NDVI drop + plausible slope + TerraMind agrees" vs. "NDVI drop only, slope implausible, TerraMind silent"). Swap for a learned ranker later once real review data accumulates.

**Why late fusion (combine scores, not combine raw signals into one model):** each signal stays individually inspectable — a debugging necessity at this stage, not a nicety.

---

### Step 7 — Gridding + Alert Storage

**What:** AOI divided into a grid; each cell's fused score written to SQLite (location, score, component signals, confidence, status).

**Why gridding:** converts a continuous raster into discrete, reviewable units — "check cell (3,7)" is a concrete task, a probability heatmap is not.

**Why SQLite, not Postgres/PostGIS:** file-based, zero setup, appropriate at prototype scale with one AOI and no concurrent writers. Swap to PostgreSQL/PostGIS only if the project moves past single-user prototype into something with concurrent access or heavier geospatial queries — premature now.

---

### Step 8 — API Layer (FastAPI)

**What:** FastAPI endpoint(s) serving grid cells as GeoJSON (location, score, confidence, contributing signals) from SQLite.

**Why FastAPI:** matches your existing backend stack (continuity with your broader FastAPI learning direction), async-capable if this ever needs to scale, auto-generates interactive API docs which doubles as a quick manual test surface.

**Why a real API instead of a notebook dumping static files:** this is the actual requirement driving the "web app not notebook" shift — a notebook can't be opened and clicked through by someone else, an API + frontend can.

---

### Step 9 — Frontend (Leaflet / folium map)

**What:** A map showing the AOI boundary, alert-cell overlay (colored/sized by score), and a before/after true-color imagery toggle.

**Why Leaflet:** open-source, lightweight, the standard choice for a web GIS frontend without needing a commercial mapping platform — directly consistent with your macro pipeline's existing choice.

**Why this over a notebook-rendered `geemap` map:** `geemap`'s interactive layers only live inside a running notebook kernel — not shareable, not a thing someone else can open. A served HTML page backed by the FastAPI endpoint is an actual deliverable.

---

## Known Limitations (by design, not oversights)

- **No SAR** — any sub-region cloud-covered across the entire T1/T2 window has no usable data and will silently read as "no change," not "no data." This is the project's core cloud-cover problem, reproduced in miniature.
- **TerraMind, if it survives the timebox, is zero-shot** — not fine-tuned, not validated against labels, treated as one weak corroborating signal, not a ground-truth source.
- **Heuristic scoring is unvalidated** — thresholds (NDVI σ-multiplier, slope range, fusion weights) are hand-picked, not calibrated against confirmed outcomes, because no labeled outcomes exist yet.
- **Single AOI, single event** — no claim of generalization to other regions or event types from this prototype.

## Validation Approach

No labeled dataset exists, so validation is case-based, not metric-based:
- Do the highest-scored grid cells spatially overlap the documented event?
- For 2–3 flagged cells that look like likely false positives (steep shadowed terrain, non-landslide vegetation loss), do they fail the slope filter or lack TerraMind agreement — confirming *why* they're false positives, not just that they are?
- If TerraMind was included: does it change which cells rank highest versus classical-signals-only? Log the answer either way — a "no difference" result is useful evidence for scoping it out of the next iteration.

## Explicitly Undecided / To Confirm Before Building

- Final AOI coordinates and anchoring event (Step 1 — nothing downstream can start without this).
- Exact T1/T2 date windows, pending how cloudy this specific AOI/season actually is.
- NDVI σ-multiplier and slope-range bounds — expected to need 1–2 rounds of empirical tuning, not fixed in advance.
- Fusion weighting between the (up to) four signals — start equal-weighted, adjust only if Step 6 output looks obviously wrong.
