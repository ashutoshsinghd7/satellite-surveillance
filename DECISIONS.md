# Decisions Log

### GEE over Microsoft Planetary Computer / STAC
**Date:** 2026-10-08
**Decision:** I use Google Earth Engine as the access layer for this prototype.
**Why:** GEE provides free compute at prototype scale, server-side processing so raw tiles do not need to be downloaded, and a scriptable Python API that can be carried into the larger pipeline.
**Alternatives I considered and rejected:** I rejected Microsoft Planetary Computer/STAC and other data APIs because this prototype is explicitly built around GEE.

### Optical-first (Sentinel-2); SAR deferred
**Date:** 2026-10-08
**Decision:** I use Sentinel-2 optical imagery first and explicitly defer SAR.
**Why:** SAR adds a separate preprocessing chain, including speckle filtering and different calibration. I need to validate the optical baseline before adding a second sensor's complexity.
**Alternatives I considered and rejected:** I rejected adding optical and SAR together in the prototype because SAR adds a separate preprocessing chain and optical-only validation is the prerequisite.

### Heuristic priority scoring over a learned ranker
**Date:** 2026-10-08
**Decision:** I use a hand-specified heuristic to produce a priority score per grid cell rather than training a learned ranker.
**Why:** No validated ground-truth outcomes exist yet to train a ranker on. A heuristic is fully auditable, and late fusion keeps each signal individually inspectable.
**Alternatives I considered and rejected:** I rejected a learned ranker at this stage because there are no validated ground-truth outcomes for training.

### TerraMind frozen/zero-shot as a fourth evidence signal
**Date:** 2026-10-08
**Decision:** I use TerraMind 1.0 as a frozen feature extractor and zero-shot fourth evidence signal, not as a fine-tuned model. I timebox the Day-2 integration to 3–4 hours; if it does not produce a working embedding-distance raster by the cutoff, I fall back to classical signals only.
**Why:** Fine-tuning requires labeled Himalayan landslide data, which does not exist yet. TerraMind can provide an independent signal while preserving the late-fusion design, but the integration risk must remain bounded.
**Alternatives I considered and rejected:** I rejected fine-tuning because labeled data does not exist. I rejected embedding clustering/anomaly scoring because it adds complexity for a first pass. I retain classical-signals-only as the fallback if the timebox is missed.

### SQLite over PostgreSQL/PostGIS at prototype stage
**Date:** 2026-10-08
**Decision:** I use SQLite for prototype storage.
**Why:** SQLite is file-based, requires zero setup, and is appropriate for one AOI with no concurrent writers.
**Alternatives I considered and rejected:** I rejected PostgreSQL/PostGIS at this stage because the prototype is limited to one AOI and has no concurrent writers; migration can happen if the project moves past a single AOI.

### Web app over notebook deliverable
**Date:** 2026-10-08
**Decision:** I build a running web app with a FastAPI backend and Leaflet/folium frontend rather than a notebook deliverable.
**Why:** The prototype must be something a person can open and click around in. A notebook-rendered map only lives inside a running notebook kernel and is not shareable in the same way as a served web page.
**Alternatives I considered and rejected:** I rejected a notebook/geemap deliverable because its interactive layers live inside the running notebook kernel and are not a shareable web app.

### NDVI/NDSI delta and slope filter with AOI-local thresholding
**Date:** 2026-10-08
**Decision:** I use NDVI/NDSI deltas and a slope filter as classical signals, with AOI-local statistical thresholding rather than a fixed threshold.
**Why:** NDVI and NDSI are trivial to compute and fully interpretable. An AOI-local threshold accounts for different baseline vegetation density, and keeping slope plausibility as a separate gate preserves inspectability.
**Alternatives I considered and rejected:** I rejected a fixed NDVI-drop threshold because it will not generalize across AOIs with different baseline vegetation density. I rejected immediately blending terrain plausibility into one opaque score because the separate gate is easier to inspect and debug.
