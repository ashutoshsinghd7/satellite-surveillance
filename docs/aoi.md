# AOI — Kali Dhank (Barwas) landslide, Sirmaur, Himachal Pradesh

Single source of truth for the AOI (see AGENTS.md no-duplication rule). Code reads the JSON block below.

```json
{
  "name": "kali_dhank_barwas",
  "bbox_wgs84": [77.5924, 30.5331, 77.7176, 30.6409],
  "bbox_order": "[west, south, east, north] (lon/lat, EPSG:4326)",
  "event_point_wgs84": [77.65056, 30.59722],
  "event_date": "2021-07-30",
  "box_size_km": 12
}
```

## Event
- Debris slide at Kali Dhank near Barwas village on NH-707 (Paonta Sahib–Hatkoti road), Shillai subdivision, Sirmaur district, Himachal Pradesh, morning of 30 July 2021.
- Sources: HPSDMA-hosted geological note on the Kali Dhank landslide (dated field study 3–4 Aug 2021); news coverage dated 30 July 2021 (DNA India / CNN News18 video report of NH-707 blocked near Barwas; fact-check articles citing a ~100 m road stretch collapse, no casualties).

## Extent justification
12 km x 12 km (inside the 10–15 km spec), centred about 1 km south of the event point so the scar sits well inside the box with ~5 km of surrounding terrain. That gives enough undisturbed hillside for AOI-local NDVI statistics (mean − 2σ) while staying small enough to inspect visually. At 20 m this is ~600 x 600 px.

## Verification
Event point and box checked on a basemap by the CP0 owner: the scar lies inside the box (point is ~1.1 km north of the box centre, ~5 km from the nearest edge).

Status: FROZEN (CP0).
