# Project Context : Multi-Sensor Satellite Surveillance & Hazard Intelligence

Name: GeoAgis

**Status:** in Development.

## One Sentence Definition:

An AI system that fuses optical + SAR satellite imagery over difficult, remote terrain (starting with the Himalayas) to continuously detect change, assess terrain/environmental hazards, and deliver confidence rated, evidence backed alerts to human decision makers  for both defense situational awareness and civilian mountain safety.

## Problem

- Physical/drone surveillance in high-altitude terrain is unreliable: cold, snowfall, cloud cover, rugged terrain, battery limits, restricted access create observation gaps.
- Satellites can cover the gap, but imagery volume is too large to review manually.
- Optical fails under cloud/darkness. SAR works day/night through cloud but is harder to interpret alone.
- Goal: **raw imagery → detected change → interpreted, confidence rated intelligence**, not stopping at image classification.

## Design Philosophy

- Decision support, not autonomy — the system flags, humans decide.
- Every output is explainable: what was detected, why, what evidence supports it, how confident the system is.
- No single opaque score — independent evidence stays inspectable; fusion happens at decision level.
- Confidence is mandatory — satellite data is incomplete, noisy, outdated, or weather-limited.
- "Continuous" ≠ real-time — bounded by revisit frequency and coverage.

---

## Macro Pipeline

1. **Multi-sensor acquisition** — optical + SAR imagery over a defined area of interest, multiple timestamps, ideally from a satellite constellation (not single-pass) to shrink revisit time gaps.
2. **Preprocessing & co-registration** — align all timestamps/sensors to the same pixel grid; mask unusable data (cloud, noise) so downstream layers aren't fed garbage.
3. **Intelligence layers (parallel evidence generation layers, with dependencies where required):**
   - **Change Intelligence** — what changed since the last observation, and where.
   - **Terrain Intelligence** — elevation, slope, aspect, terrain structure.
   - **Environmental Intelligence** — snow, weather, surface conditions.
   - **Hazard Intelligence** — avalanche, landslide, and other instability risk.
   - **Human-Activity Change Intelligence** — whether a detected change is plausibly human-induced vs. natural.
4. **Evidence fusion** — combine the independent layers' outputs per location at decision level, not as one opaque score.
5. **Confidence / uncertainty estimation** — attach a reliability estimate to every fused assessment.
6. **Alerting** — convert the fused, confidence-rated output into discrete, reviewable units for a human (not a raw probability map).
7. **Human review & feedback** — a person confirms or rejects each alert; outcomes feed back into the system to improve future detection and scoring.

## Use Cases (dual use, same infrastructure)

- **Defense / border region monitoring:** detected changes, areas requiring attention, environmental conditions, terrain characteristics, historical changes, confidence estimates — decision support only, no autonomous action.
- **Civilian mountain safety:** avalanche monitoring, snow-condition assessment, landslide monitoring, infrastructure monitoring, trekker/hiker safety, search-and-rescue support, disaster monitoring.

## Honest Differentiation

- SAR-optical fusion for change detection is **not novel** — it's an active published research area, and commercial systems already sell it.
- What's actually distinct: scoping to Himalayan terrain specifically, an auditable late-fusion design where every alert traces to named evidence rather than one opaque score, and a human feedback loop wired in from the start.

## Known Constraints (apply across the whole pipeline)

- Satellite resolution may not resolve every object/event of interest.
- Revisit frequency gaps are structural; a constellation reduces but doesn't eliminate them.
- Optical is blind under cloud/darkness; SAR is harder to interpret and needs its own handling, not shared tooling with optical.
- Himalayan terrain complexity (shadows, slopes, snow, rock, vegetation) makes automated interpretation harder than flatter terrain most published work targets.
- False positives/negatives run both directions — natural change can resemble human activity and vice versa.
- Hazard prediction (avalanche/landslide) from imagery alone is likely insufficient; probably needs added environmental/historical data.
- Data availability, licensing, and compute quotas constrain what's actually buildable at any given time.
- Model outputs can be wrong — the confidence layer exists specifically so the system doesn't overclaim certainty.

## Explicitly Undecided

Exact datasets per layer · sensor-fusion methodology · change-detection algorithms · hazard-prediction methodology · terrain-modelling approach · confidence-score methodology · revisit-frequency strategy at constellation scale · false-positive/negative handling policy · real-time vs. near-real-time processing · cloud vs. edge infrastructure · visualization approach · alert-generation policy · evaluation metrics · ground-truth/dataset creation strategy · defense integration path · civilian deployment path · cost and scalability.
