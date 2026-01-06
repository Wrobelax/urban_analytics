# Solution Architecture

This project implements a unified analytics platform on Microsoft Fabric
using a medallion architecture (Bronze → Silver → Gold).

The solution integrates:
- Mobility data (NYC Taxi Trips)
- Environmental data (OpenAQ Air Quality)
- Macroeconomic data (World Bank GDP, ECB FX)

All components are orchestrated inside a single Fabric workspace.


## High-Level Data Flow

1. External data sources provide raw data:
   - NYC Green and Yellow Taxi Parquet files
   - OpenAQ REST API
   - World Bank REST API
   - ECB FX CSV API

2. Data is ingested into OneLake using:
   - Fabric Data Pipelines (file copy, orchestration)
   - Dataflows Gen2 (API ingestion)
   - Fabric pipelines are used for orchestration only and rely on Dataflows and Notebooks to handle data persistence in the Lakehouse.

3. Raw data is stored in the Bronze layer.

4. PySpark notebooks transform data into standardized Silver tables.

5. Gold layer applies dimensional modeling (star schema).

6. Analytics and visualizations are built using Fabric Notebooks (Matplotlib).

## Medallion Architecture

The medallion architecture was used to separate concerns between raw ingestion, data cleansing, and analytical modeling. This design improves data quality, reproducibility, and scalability.

![image-alt-text](https://i.postimg.cc/y8yxN8Sx/medalion.png)
### Bronze Layer
- Stores raw ingested data
- No schema enforcement
- Minimal transformations (JSON flattening)
- Sources:
  - NYC Taxi Parquet files
  - OpenAQ API JSON
  - World Bank GDP JSON
  - ECB FX CSV
- Supportive data:
  - Taxi zones lookup CSV

### Silver Layer
- Cleaned and standardized datasets
- Schema normalization
- Deduplication and validation
- Enriched with date columns

### Gold Layer
- Analytics-ready star schema
- Fact and Dimension tables
- Aggregated daily metrics
- Optimized for reporting


## Design Decisions and Trade-offs

Several architectural decisions were made to balance scalability, data quality, and operational simplicity.

### Use of Medallion Architecture
The medallion architecture was selected to clearly separate raw ingestion, data cleansing, and analytical modeling.
This enables:
- easier debugging and reprocessing
- reproducibility of transformations
- safe extension of historical data without re-ingestion

### Retaining Raw Data in Bronze
Raw data is preserved without filtering to ensure:
- full auditability
- ability to reprocess data with new business rules
- protection against incorrect early assumptions

### Partial Data Cleansing in Silver
Silver layer applies validation and normalization but avoids aggressive filtering.
This prevents accidental loss of valid but rare events (e.g. long taxi trips, sensor gaps).

### Aggregation Strategy
Aggregations are applied selectively in the Silver layer when they represent stable, reusable business grains (e.g. daily metrics).
The Gold layer focuses on dimensional modeling, surrogate key mapping, and exposing analytics-ready fact tables.


## Data Quality and Validation Strategy

Data quality checks are applied progressively across layers.

### Bronze
- No filtering or validation
- Raw ingestion guarantees data completeness

### Silver
- Validation of timestamps (pickup <= dropoff)
- Removal of clearly invalid records (null critical fields)
- Normalization of date and time formats
- Handling of partial sensor coverage without forcing continuity

### Gold
- Aggregation-level validation
- Referential integrity between fact and dimension tables
- Detection of unexpected nulls in aggregated metrics

## Bronze Layer Components

### Ingestion Methods
- Data Pipelines:
  - Monthly NYC Taxi Parquet ingestion
- Dataflows Gen2:
  - OpenAQ air quality API
  - World Bank GDP API
  - ECB FX API

### Storage
- OneLake / Lakehouse
- Raw files and raw tables

## Silver Layer Components

### Key Silver Tables
- silver_taxi_trips
- silver_air_quality_measurements
- silver_air_quality_daily
- silver_fx
- silver_gdp
- silver_zone_lookup

### Responsibilities
- Schema standardization
- Data cleansing
- Date normalization
- Validation rules


## Gold Layer and Star Schema

In the Gold layer, a star schema was applied to optimize analytical queries and enable efficient slicing by time, location, and economic context.

![Star schema](https://i.postimg.cc/2SGjD9Ph/star.png)

### Fact Tables
- FactTaxiDaily
- FactAirQualityDaily

### Dimension Tables
- DimDate
- DimZone
- DimFX
- DimGDP


## Warehouse Integration

Gold tables are exposed through the Fabric Warehouse using:
- Shortcuts to Lakehouse Gold tables
- SQL-based querying and reporting

The Warehouse serves as the semantic layer for analytics and BI tools, and acts as the consumer-facing analytical layer, while the Lakehouse remains the system of record for transformations.

## Lineage and Governance

- Data lineage is tracked automatically by Microsoft Fabric.
- End-to-end lineage covers:
  - Source systems
  - Dataflows and Pipelines
  - Lakehouse tables
  - Notebooks
  - Warehouse tables

Each Gold table can be traced back to its originating Bronze source through a deterministic chain of Dataflows and Notebooks.

## Automation and Refresh


- NYC Taxi ingestion and transformation are separated into two pipelines: one responsible for Bronze ingestion and another for Silver and Gold transformations, ensuring modularity and easier maintenance.
- Static reference data such as taxi zone lookup tables are loaded once and are not part of scheduled pipelines due to their infrequent changes.

## Scalability and Extensibility

The solution was designed to support future growth with minimal refactoring.

### Temporal Scalability
- Historical taxi and air quality data can be added without schema changes
- Date-driven transformations allow seamless backfilling

### Domain Scalability
- New mobility datasets (e.g. bike sharing, traffic sensors) can reuse DimDate and DimZone
- Additional environmental indicators can be added to FactAirQualityDaily

### Tooling Scalability
- Pipelines orchestrate components without embedding business logic
- Notebooks remain isolated per transformation stage


## Limitations and Known Constraints

This project acknowledges several real-world data constraints.

### Sensor Coverage Gaps
Air quality sensors do not provide continuous measurements.
Daily aggregation was chosen to mitigate irregular sampling.

### API Availability
OpenAQ and World Bank APIs impose rate limits and historical availability constraints.
The pipeline design allows re-execution when new data becomes available.

### Correlation vs Causation
Observed correlations between mobility and air quality do not imply direct causation.
