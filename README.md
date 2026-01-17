# Urban Mobility, Air Quality & Economy Analytics (Microsoft Fabric)

___

## Overview
This project builds a unified analytics platform on Microsoft Fabric that integrates:
- NYC Taxi mobility data
- OpenAQ air quality data
- World Bank GDP & ECB FX data
- OpenAPI weather data

The solution uses a Medallion Architecture (Bronze → Silver → Gold)
and a Star Schema for analytics.

___

## Live Environment
The solution is implemented in Microsoft Fabric. Access to the workspace can be provided upon request.
___

## Project Scope
This project focuses on batch analytics and daily-grain insights.
Real-time streaming, Power BI dashboards, and advanced governance features
(RLS, Purview) are considered out of scope.

___

## Repository Structure

```
urban_analytics/
│
├── README.md
│
├── documentation/
│   ├── documentation_architecture_and_lineage.md
│   ├── documentation_data_dictionary.md
│   ├── documentation_governance_policies.md
│   └── diagrams/
│        ├── medallion_architecture.png
│        └── star_schema.png
│   
├── ingestion/
│      ├── bronze_nyc_taxi_ingestion.md
│      ├── bronze_openaq_ingestion.md
│      ├── bronze_fx_ingestion.md
│      ├── bronze_weather_openapi_ingestion.md
│      └── bronze_gdp_ingestion.md
│
├── notebooks/
│   ├── silver/
│   │   ├── silver_nyc_taxi_transformation.py
│   │   ├── silver_air_quality_measurements_transformation.py
│   │   ├── silver_air_quality_daily_transformation.py
│   │   ├── silver_fx_daily.py
│   │   ├── silver_gdp_transformation.py
│   │   ├── silver_weather.py
│   │   └── silver_taxi_zones_lookup.py
│   │
│   ├── gold/
│   │   ├── gold_fact_taxi_daily.py
│   │   ├── gold_fact_air_quality_daily.py
│   │   ├── gold_dimdate.py
│   │   ├── gold_dimzone.py
│   │   ├── gold_weather.py
│   │   ├── gold_dimfx.py
│   │   └── gold_dimgdp.py
│   │
│   ├── implementations/
│   │   ├── grafana/
│   │   │     └── influx_integration.py
│   │   ├── great_expectations/
│   │   │     ├── great_expectations_conf.py
│   │   │     └── great_expectations_run.py
│   │   └──  power_automate/
│   │         └── generate_json.py
│   │ 
│   └── visualization/
│       └── data_visualization.ipynb
│
└── sql/
    └── warehouse/
        ├── create_dimdate.sql
        ├── create_dimzone.sql
        ├── create_dimfx.sql
        ├── create_dimgdp.sql
        ├── create_fact_taxi_daily.sql
        └── create_air_quality.sql
```
___

## Architecture

Dataflows and Pipelines ingest data into OneLake, PySpark Notebooks perform transformations across medallion layers, and Gold tables are exposed through the Fabric Warehouse for analytics.

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
- OpenAPI Weather

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
- Revenue USD vs EUR with FX conversion and GDP as macroeconomic context

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
Microsoft Fabric (Lakehouse, Dataflows Gen2, Pipelines, Warehouse), PySpark, Delta Lake, SQL, Matplotlib
