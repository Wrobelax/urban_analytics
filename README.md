# Urban Mobility, Air Quality & Economy Analytics (Microsoft Fabric)

___

## Overview
This project builds a unified analytics platform on Microsoft Fabric that integrates:
- NYC Taxi mobility data
- OpenAQ air quality data
- World Bank GDP & ECB FX data

The solution uses a Medallion Architecture (Bronze → Silver → Gold)
and a Star Schema for analytics.

___

## Architecture
- OneLake + Lakehouse
- Dataflows Gen2 for APIs
- Fabric Pipelines for orchestration
- PySpark Notebooks for transformations
- Fabric Warehouse for Gold layer

___

## Data Sources
- NYC TLC Taxi Trips (Parquet)
- OpenAQ API
- World Bank API
- ECB FX API

___

## Medallion Layers
### Bronze
Raw ingested data, no transformations.

### Silver
Cleaned, validated, standardized datasets.

### Gold
Star schema with Fact and Dimension tables.

___

## Analytics
- Daily taxi trips & revenue
- Average fare trends
- Top pickup zones
- PM2.5 / NO2 daily trends
- Mobility vs Air Quality correlation
- Revenue USD vs EUR with GDP context

___

## Automation
- Scheduled Dataflows
- Orchestrated pipelines (Bronze → Silver → Gold)

___

## Key Insights
- **Strong daily mobility patterns are visible in NYC taxi data**: Daily taxi trips show clear temporal patterns with consistent weekday activity and visible drops during public holidays. This confirms that taxi demand is strongly driven by urban routines rather than random behavior.

- **Average fare spikes align with reduced trip volume, not data errors**: Significant increases in average fare per trip (e.g. around public holidays such as Martin Luther King Jr. Day) occur simultaneously with lower trip counts.
This suggests:
  - longer trips,
  - higher congestion surcharges,
  - or higher proportion of premium rides, rather than data quality issues.

- **Pickup demand is highly concentrated in a small number of zones**: A small subset of pickup zones accounts for a disproportionately large share of all taxi trips.
  This highlights:
  - spatial inequality in mobility demand,
  - the importance of central business and transport hubs, which is highly relevant for urban planning and congestion management.

- **Air quality data shows sensor-level variability but consistent city-wide trends**: Individual OpenAQ sensors exhibit partial coverage and varying continuity, but when aggregated:
  - PM2.5 and NO₂ daily trends show coherent city-level patterns,
  - enabling meaningful temporal analysis despite sensor sparsity.
  - This validates the decision to aggregate air quality data at the daily level in the Gold layer.

- **Mobility and air quality show temporal co-movement, not direct causality**: Overlaying daily taxi trips with PM2.5 concentrations reveals periods where increased mobility coincides with pollution spikes.
  While this does not prove causation, it demonstrates:
  - temporal alignment between mobility intensity and environmental pressure,
  - the analytical value of integrating mobility and environmental datasets.

- **Medallion architecture enables scalability and auditability**: 
  Separating raw (Bronze), cleaned (Silver), and analytical (Gold) layers allowed:
  - safe reprocessing of historical data,
  - transparent handling of outliers and partial sensor coverage,
  - flexible future extensions (e.g. adding weather or traffic sensor data).
  - This architecture proved essential for managing heterogeneous, multi-domain datasets.

- **Daily aggregation is the optimal granularity for cross-domain analytics**:
  Aligning all datasets (mobility, air quality, FX) at a daily grain enabled:
  - reliable joins across domains,
  - stable visualizations,
  - avoidance of false precision that would arise from mixing hourly and daily data.

___

## Tech Stack
Microsoft Fabric, PySpark, Delta Lake, SQL, Matplotlib
