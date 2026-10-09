# Methodology and Evaluation

## 1. Overview

The Himalayan Landslide Detection Pipeline is designed to investigate potential landslide-related surface changes using optical satellite imagery, terrain information and complementary image-derived features.

The proposed methodology follows a reproducible workflow: data selection, preprocessing, change analysis, terrain assessment, evidence fusion, geospatial output generation and validation.

The system is a research prototype under development. The methodology described below defines the intended approach; individual processing stages and their performance must be verified through implementation and testing.

## 2. Data Sources

### 2.1 Sentinel-2 Optical Imagery

Sentinel-2 provides multispectral observations suitable for analysing vegetation, snow and other surface characteristics.

The proposed workflow uses two observation periods:

- **T1:** Earlier observation.
- **T2:** Later observation.

The selected images should cover the same Area of Interest (AOI) and have sufficiently comparable acquisition conditions.

Before interpreting T1 and T2 as pre-event and post-event imagery, their acquisition dates must be checked against a documented landslide event.

### 2.2 Digital Elevation Model

A Digital Elevation Model (DEM) represents ground elevation and provides terrain context.

The proposed workflow uses elevation data to derive slope and assess whether candidate changes occur in terrain that may be relevant to landslide investigation.

The DEM source, spatial resolution, coordinate reference system and processing parameters must be recorded.

### 2.3 Semantic Image Features

TerraMind is proposed as an additional source of semantic image features.

Its suitability for the selected imagery, the precise feature-extraction procedure and its contribution to landslide-related change detection must be established experimentally.

### 2.4 Data Provenance

For reproducibility, record the following wherever applicable:

- Data provider and dataset identifier.
- Study-area boundary and coordinate reference system.
- Acquisition dates and observation windows.
- Image identifiers and selected spectral bands.
- Cloud and data-quality information.
- DEM source and resolution.
- Processing parameters and software versions.

## 3. Study Area and Observation Selection

The analysis begins by defining an Area of Interest around a documented landslide event in the Himalayan region.

The AOI should be large enough to include the event and surrounding terrain while remaining manageable for the initial prototype.

The observation-selection process should:

1. Define the study-area boundary.
2. Identify the reference event and date, where available.
3. Search for suitable earlier and later satellite observations.
4. Check image coverage, cloud conditions and acquisition dates.
5. Record the selected observations and the reasons for their selection.

A valid comparison requires suitable imagery from both periods. If the available observations are unsuitable, the analysis should report the limitation rather than silently use poor-quality data.

## 4. Image Preprocessing

Preprocessing is intended to reduce differences caused by data quality and acquisition conditions rather than genuine surface change.

### 4.1 Cloud and Shadow Masking

Clouds and shadows can produce misleading changes between observations.

Where suitable Sentinel-2 quality information is available, cloud and shadow masks should be applied before calculating change indicators. The Scene Classification Layer (SCL) may be used where appropriate.

The masking procedure and excluded pixels should be documented.

### 4.2 Spatial Alignment

The T1 and T2 observations and the DEM must use compatible spatial references and be aligned appropriately before pixel-level comparison.

Differences in projection, resolution, extent or pixel alignment can create artificial changes.

### 4.3 Temporal Comparability

Observation periods should be selected carefully to reduce misleading differences caused by seasonal vegetation, snow cover and other environmental variation.

Median composites may be considered when multiple suitable observations are available within a defined period. Their use should be justified and documented.

## 5. Spectral Change Analysis

The baseline approach compares selected spectral indicators between T1 and T2.

### 5.1 Normalized Difference Vegetation Index

NDVI is used to investigate vegetation-related surface changes.

For Sentinel-2, NDVI is commonly calculated using the near-infrared and red bands:

\[
NDVI = \frac{B8-B4}{B8+B4}
\]

where \(B8\) is the near-infrared band and \(B4\) is the red band.

The change in NDVI is calculated as:

\[
\Delta NDVI = NDVI_{T2}-NDVI_{T1}
\]

A negative change may indicate reduced vegetation response, but it does not independently establish a landslide.

### 5.2 Normalized Difference Snow Index

NDSI is used to investigate snow-related conditions.

For Sentinel-2, a common formulation is:

\[
NDSI = \frac{B3-B11}{B3+B11}
\]

where \(B3\) is the green band and \(B11\) is the short-wave infrared band.

The change is calculated as:

\[
\Delta NDSI = NDSI_{T2}-NDSI_{T1}
\]

NDSI changes can help identify snow-related differences that might otherwise complicate interpretation of the vegetation signal.

### 5.3 Candidate Change Indicators

The spectral indicators can be combined with data-quality checks to identify locations requiring further investigation.

Thresholds should be treated as parameters to evaluate rather than universal rules. Their selection must consider the study area, image quality, seasonal variation and reference data.

## 6. Terrain Analysis

Terrain information provides context for interpreting candidate changes.

### 6.1 Slope Derivation

Slope can be derived from the DEM using an appropriate terrain-processing method.

The resulting slope layer should be aligned with the imagery before it is incorporated into the assessment.

### 6.2 Terrain-Aware Assessment

Slope may be used to prioritise or contextualise candidate regions. However, a steep slope is not sufficient evidence of a landslide, and landslides can occur outside any single predefined slope range.

Any slope thresholds or weighting rules must be documented and evaluated against reference examples.

## 7. Semantic Feature Analysis

The proposed TerraMind stage investigates whether semantic image features can provide additional evidence beyond conventional spectral indicators.

The intended procedure is to:

1. Prepare compatible imagery according to the model's requirements.
2. Apply the selected model configuration.
3. Extract the appropriate representations or predictions.
4. Compare the resulting signals across observation periods where appropriate.
5. Evaluate whether the features improve candidate detection.

The exact model interface, input requirements, feature-comparison method and computational cost must be confirmed before implementation.

Semantic feature differences should not automatically be interpreted as landslide evidence.

## 8. Evidence Fusion and Candidate Scoring

The proposed evidence-fusion stage combines selected signals into an interpretable candidate assessment.

Potential inputs include:

- NDVI change.
- NDSI change and snow-related checks.
- Terrain characteristics.
- Semantic image features, if validated.

A scoring method may combine these signals using documented rules or a suitable model. Its inputs, transformations, weights and thresholds must be specified explicitly.

The initial scoring approach should be treated as a heuristic unless it is calibrated and validated against appropriate reference data.

**Important:** A candidate score is not a probability of landslide occurrence unless probabilistic calibration and validation support that interpretation.

## 9. Geospatial Output Generation

Candidate results should retain their geographical location and supporting evidence.

The proposed output process includes:

1. Associating candidate scores with the relevant pixels or spatial units.
2. Aggregating results into defined grid cells or regions, if appropriate.
3. Recording the evidence contributing to each candidate.
4. Preserving source dates and processing metadata.
5. Exporting suitable georeferenced outputs for inspection and visualisation.

Grid dimensions, aggregation rules and alert thresholds must be selected and documented during implementation.

An alert represents a location requiring further investigation, not a confirmed landslide.

## 10. Evaluation Strategy

Evaluation must compare system outputs with suitable reference data, such as documented landslide boundaries or independently verified event locations.

The reference data, spatial evaluation unit and matching criteria should be defined before calculating performance metrics.

### 10.1 Precision

Precision measures the proportion of predicted positive cases that match the reference labels.

\[
Precision = \frac{TP}{TP+FP}
\]

Here, \(TP\) represents true positives and \(FP\) represents false positives.

Higher precision generally indicates fewer incorrect candidate detections.

### 10.2 Recall

Recall measures the proportion of reference positive cases identified by the system.

\[
Recall = \frac{TP}{TP+FN}
\]

Here, \(FN\) represents false negatives.

Higher recall generally indicates that fewer reference cases were missed.

### 10.3 F1-Score

The F1-score is the harmonic mean of precision and recall.

\[
F1 = 2 \times \frac{Precision \times Recall}{Precision+Recall}
\]

It provides a combined measure when both false alarms and missed detections matter.

### 10.4 Spatial Overlap

Where reference landslide boundaries are available, spatial overlap can be evaluated using Intersection over Union (IoU):

\[
IoU = \frac{|P \cap G|}{|P \cup G|}
\]

where \(P\) represents the predicted region and \(G\) represents the reference region.

The overlap metric and matching procedure should be appropriate to the scale and geometry of the reference data.

### 10.5 False-Positive Analysis

False positives should be investigated to understand whether candidate detections are caused by:

- Seasonal vegetation changes.
- Snow accumulation or snowmelt.
- Cloud or cloud-shadow contamination.
- Changes in illumination or acquisition conditions.
- Water, exposed ground or other unrelated surface changes.
- Terrain or image-alignment errors.

The results of this analysis can guide improvements to preprocessing and evidence fusion.

## 11. Validation Protocol

A proposed validation procedure is:

1. Select documented landslide events with suitable satellite observations.
2. Establish reference labels from reliable independent sources.
3. Process the imagery using recorded parameters.
4. Generate candidate regions without using the evaluation labels to tune the results on the same test cases.
5. Calculate the selected metrics.
6. Examine false positives and missed events.
7. Compare against a simple baseline, such as spectral change detection without semantic features.
8. Record the results, limitations and any changes to the method.

Where sufficient data is available, separate development and evaluation events to reduce the risk of overestimating performance.

Results should include the test cases, data sources, thresholds and evaluation procedure so that another reviewer can reproduce the analysis.

## 12. Limitations and Sources of Uncertainty

The methodology has several important limitations:

- Optical imagery can be affected by clouds and shadows.
- Seasonal and environmental changes can resemble landslide-related changes.
- Spatial resolution may limit the identification of small events.
- Differences between observation dates can introduce misleading signals.
- DEM quality and resolution affect derived terrain features.
- Semantic features may not generalise to the study environment.
- Incomplete or inaccurate reference labels can distort evaluation.
- Heuristic scores may not be comparable across regions without calibration.

These limitations must be considered when interpreting candidate detections.

## 13. Current Status and Reporting

The methodology described in this document is the proposed approach for the research prototype.

A component should be labelled **implemented** only when its code and outputs have been verified. A method should be labelled **evaluated** only after testing against appropriate reference data.

No detection-accuracy, reliability or generalisation claim should be reported without measured results and a documented evaluation procedure.

## 14. References and Technical Resources

- [Copernicus Sentinel-2](https://dataspace.copernicus.eu/explore-data/data-collections/sentinel-data/sentinel-2)
- [Copernicus Data Space Ecosystem](https://dataspace.copernicus.eu/)
- [Google Earth Engine Documentation](https://developers.google.com/earth-engine)
- [TerraMind — Official GitHub Repository](https://github.com/IBM/terramind)
- [Rasterio Documentation](https://rasterio.readthedocs.io/)
- [GeoPandas Documentation](https://geopandas.org/)
