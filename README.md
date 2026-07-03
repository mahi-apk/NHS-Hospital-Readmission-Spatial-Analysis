# NHS Hospital Readmission — Spatial Analysis

Analysing 30-day hospital readmission rates across England's nine regions and their relationship with deprivation, using interactive geographic mapping and correlation analysis.

## Problem

Patients readmitted to hospital within 30 days of discharge cost the NHS an estimated £2.4 billion per year. NHS trusts need to understand which regions have the highest readmission rates and what drives them, so that resources can be targeted where they will have the most impact.

This project investigates two questions:
1. Which regions of England have the highest readmission rates?
2. Is deprivation a genuine driver of readmission — or is another factor, such as patient age, responsible?

## Approach

1. **Data preparation** — assembled regional readmission, deprivation, and patient age data into a single dataset.
2. **Geographic merge** — joined the health data onto England's regional map boundaries (GeoJSON), resolving a region-name mismatch between the two sources and verifying that all nine regions matched successfully.
3. **Interactive mapping** — built a choropleth map (Folium) shading each region by readmission rate, with hover tooltips showing region-level detail.
4. **Correlation analysis** — measured the relationship between deprivation, patient age, and readmission to identify the true driver.
5. **Visualisation** — produced a scatter plot with a trend line to visually confirm the deprivation–readmission relationship.

## Key Findings

| Factor | Correlation with readmission |
|--------|------------------------------|
| Deprivation score | **0.98** (very strong positive) |
| Average patient age | -0.11 (negligible) |

- The **North East** has the highest readmission rate (14.8%) and the highest deprivation score (28.5).
- The **South East** has the lowest readmission rate (11.8%) and the lowest deprivation score (16.2).
- **Deprivation — not patient age — is the dominant driver.** Age was tested as an alternative explanation and showed almost no correlation, ruling it out.

**Implication:** targeting readmission-reduction efforts at more deprived regions is likely to be far more effective than targeting by patient age.

## Skills Demonstrated

- Merging tabular data with geographic boundaries (spatial join)
- Handling and cleaning mismatched categorical data between sources
- Building interactive choropleth maps with hover tooltips
- Correlation analysis and testing alternative explanations
- Communicating statistical findings as clear, actionable insight

## Tools

Python, pandas, GeoPandas, Folium, Matplotlib, NumPy

## Files

| File | Description |
|------|-------------|
| `nhs_readmission.py` | Full analysis pipeline |
| `england_choropleth.html` | Interactive readmission map (open in a browser) |
| `correlation_scatter.png` | Deprivation vs readmission scatter plot |

## How to Run

```bash
pip install pandas numpy geopandas folium matplotlib
python nhs_readmission.py
```

The script prints the key findings and generates the interactive map and scatter plot.

## Data Note

Regional figures are modelled on published NHS England and ONS regional patterns to demonstrate spatial analysis methodology. The techniques used — geographic merging, choropleth mapping, and correlation analysis — apply directly to raw NHS and ONS open data.
