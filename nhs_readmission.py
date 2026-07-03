# ============================================
# NHS HOSPITAL READMISSION — SPATIAL ANALYSIS
# Sector: Healthcare / NHS
# Tools: pandas, geopandas, folium, matplotlib
# ============================================

import pandas as pd
import numpy as np
import geopandas as gpd
import folium
import matplotlib.pyplot as plt

# ============================================
# STEP 1: LOAD DATA
# ============================================

health_data = {
    "region": [
        "North East", "North West", "Yorkshire and The Humber",
        "East Midlands", "West Midlands", "East of England",
        "London", "South East", "South West"
    ],
    "readmission_rate": [14.8, 14.2, 13.9, 13.1, 13.5, 12.4, 12.9, 11.8, 12.1],
    "deprivation_score": [28.5, 27.1, 25.8, 22.3, 24.6, 18.9, 23.4, 16.2, 17.8],
    "avg_patient_age": [71, 70, 69, 68, 69, 70, 64, 71, 73]
}
health_df = pd.DataFrame(health_data)

url = "https://raw.githubusercontent.com/martinjc/UK-GeoJSON/master/json/electoral/eng/eer.json"
map_df = gpd.read_file(url)

# ============================================
# STEP 2: MERGE HEALTH DATA ONTO MAP
# ============================================

# Fix region name mismatch between datasets
map_df["EER13NM"] = map_df["EER13NM"].replace({"Eastern": "East of England"})

merged = map_df.merge(health_df, left_on="EER13NM", right_on="region", how="left")

# Verify the merge — no region should be left without data
missing = merged[merged["readmission_rate"].isnull()]
if len(missing) == 0:
    print("SUCCESS - all regions matched and have data")
else:
    print(f"WARNING - {len(missing)} regions did not match:")
    print(missing["EER13NM"].tolist())

# ============================================
# STEP 3: INTERACTIVE CHOROPLETH MAP
# ============================================

england_map = folium.Map(location=[53.0, -1.5], zoom_start=6, tiles="cartodbpositron")

folium.Choropleth(
    geo_data=merged,
    data=merged,
    columns=["EER13NM", "readmission_rate"],
    key_on="feature.properties.EER13NM",
    fill_color="YlOrRd",
    fill_opacity=0.7,
    line_opacity=0.3,
    legend_name="30-Day Readmission Rate (%)"
).add_to(england_map)

folium.GeoJson(
    merged,
    name="Region Details",
    style_function=lambda x: {"fillColor": "transparent", "color": "transparent", "weight": 0},
    tooltip=folium.GeoJsonTooltip(
        fields=["EER13NM", "readmission_rate", "deprivation_score"],
        aliases=["Region:", "Readmission %:", "Deprivation Score:"],
        localize=True
    )
).add_to(england_map)

england_map.save("england_choropleth.html")
print("Interactive choropleth map saved as england_choropleth.html")

# ============================================
# STEP 4: CORRELATION ANALYSIS
# ============================================

deprivation_corr = health_df["deprivation_score"].corr(health_df["readmission_rate"])
age_corr = health_df["avg_patient_age"].corr(health_df["readmission_rate"])

if abs(deprivation_corr) > abs(age_corr):
    more_influential = "deprivation"
else:
    more_influential = "age"

average_readmission = health_df["readmission_rate"].mean()
health_df["high_risk"] = health_df["readmission_rate"].apply(
    lambda x: 1 if x > average_readmission else 0
)

highest = health_df.sort_values(by="readmission_rate", ascending=False).iloc[0]
lowest = health_df.sort_values(by="readmission_rate", ascending=True).iloc[0]

def describe_strength(correlation):
    correlation = abs(correlation)
    if correlation > 0.7:
        return "strong"
    elif correlation > 0.4:
        return "moderate"
    else:
        return "weak"

deprivation_strength = describe_strength(deprivation_corr)

print("\n=== KEY FINDINGS ===")
print(f"Deprivation vs readmission correlation: {deprivation_corr:.2f} ({deprivation_strength})")
print(f"Age vs readmission correlation: {age_corr:.2f}")
print(f"More influential factor: {more_influential}")
print(f"Highest readmission: {highest['region']} "
      f"({highest['readmission_rate']}%, deprivation {highest['deprivation_score']})")
print(f"Lowest readmission: {lowest['region']} "
      f"({lowest['readmission_rate']}%, deprivation {lowest['deprivation_score']})")
print(f"Regions flagged high-risk: {health_df['high_risk'].sum()} out of {len(health_df)}")
print(f"Conclusion: deprivation is {deprivation_strength}ly associated with hospital readmission")

# ============================================
# STEP 5: CORRELATION SCATTER PLOT
# ============================================

plt.figure(figsize=(9, 6))
plt.scatter(health_df["deprivation_score"], health_df["readmission_rate"],
            s=120, color="#8856a7", edgecolor="black", zorder=3)

for _, row in health_df.iterrows():
    plt.annotate(row["region"],
                 (row["deprivation_score"], row["readmission_rate"]),
                 fontsize=8, xytext=(5, 5), textcoords="offset points")

z = np.polyfit(health_df["deprivation_score"], health_df["readmission_rate"], 1)
p = np.poly1d(z)
plt.plot(health_df["deprivation_score"], p(health_df["deprivation_score"]),
         "--", color="red", label="Trend line")

plt.xlabel("Deprivation Score (higher = more deprived)")
plt.ylabel("30-Day Readmission Rate (%)")
plt.title(f"Deprivation vs Readmission (correlation = {deprivation_corr:.2f})")
plt.legend()
plt.grid(alpha=0.3)
plt.savefig("correlation_scatter.png", dpi=150, bbox_inches="tight")
plt.close()
print("Scatter plot saved as correlation_scatter.png")
