# NYC Taxi Data Pipeline

## Purpose
This pipeline orchestrates the ingestion and transformation of NYC Taxi Trip data
into an analytics-ready star schema.

The pipeline is designed to handle:
- Monthly file availability delays
- Partial historical ingestion
- Idempotent re-processing

## Data Source
- NYC Taxi (TLC)
- Format: Parquet
- Taxi types: Yellow, Green
- Publication frequency: Monthly (with ~2-month lag)

## Pipeline Structure

### 1. Bronze Ingestion
- Tool: Fabric Pipeline (Copy Data)
- Source: TLC CloudFront Parquet URLs
- Target: OneLake / Lakehouse (Bronze)

**Key behavior**
- Monthly files are processed independently
- Months and year are hardcoded and iterated through ForEach statement
- Pipeline is safe to rerun without duplication
- Files are overwritten by month to ensure idempotent ingestion

### 2. Silver Transformation
- Tool: PySpark Notebook
- Notebook: `silver_nyc_taxi_transformation.py`

**Responsibilities**
- Schema unification (Yellow + Green)
- Datetime normalization
- Validation:
  - Non-null pickup/dropoff timestamps
  - pickup_datetime ≤ dropoff_datetime
- Preservation of trip-level granularity

**Output**
- `silver_taxi_trips`

### 3. Gold Transformation
- Tool: PySpark Notebook
- Notebook: `gold_fact_taxi_daily.py`

**Responsibilities**
- Daily aggregation by:
  - Date
  - Pickup zone
- Metric calculation:
  - Trips count
  - Total & average fare
  - Total & average trip distance
- Join with `DimDate`

**Output**
- `gold_fact_taxi_daily_staging`

## Scheduling
- Bronze ingestion: Monthly / manual backfill
- Silver + Gold: Daily (safe to re-run)
- Silver and Gold transformations can be safely re-executed due to deterministic logic and overwrite semantics

## Design Rationale
- Orchestration logic is isolated in pipelines
- Business logic is fully contained in versioned notebooks
- Daily grain aligns mobility data with air quality and FX datasets