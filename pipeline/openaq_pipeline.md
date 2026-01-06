# OpenAQ Air Quality Pipeline

## Purpose
This pipeline ingests and transforms air quality measurements from OpenAQ exposed as FactAirQualityDaily for analytics
to enable daily environmental analytics and correlation with mobility data.

## Data Source
- OpenAQ REST API (v3)
- Parameters:
  - PM2.5
  - PM10
  - NO2
  - SO2
  - O3
- Sensor-based measurements limited to NYC:
  - 23068
  - 23069
  - 23103
  - 23104
  - 23105
  - 23106

## Pipeline Structure

### 1. Bronze Ingestion
- Tool: Dataflow Gen2
- Method: REST API calls with pagination
- Authentication: API Key
- Time filter: `datetime_from`
- Ingestion is idempotent per datetime window

**Key behavior**
- Dataflow pulls measurements incrementally
- Handles partial sensor coverage
- Stores raw API payloads

**Output**
- Bronze OpenAQ raw table

### 2. Silver Transformation
- Tool: PySpark Notebook
- Notebook: `silver_air_quality_measurements.py`

**Responsibilities**
- JSON normalization
- Datetime normalization to UTC
- Validation:
  - Non-null measurements
  - Valid timestamps
- Separation into:
  - `silver_air_quality_measurements` (raw granularity)
  - `silver_air_quality_daily` (daily aggregates)

**Rationale**
Raw measurements are retained to:
- Support auditability
- Allow future re-aggregation strategies

### 3. Gold Transformation
- Tool: PySpark Notebook
- Notebook: `gold_fact_air_quality_daily.py`

**Responsibilities**
- Daily aggregation by:
  - Date
  - Parameter (PM2.5 / NO2)
- Sensor-agnostic averaging
- Alignment with `DimDate`

**Output**
- `gold_fact_air_quality_daily_staging`

## Scheduling
- Dataflow Gen2: Daily
- Silver pipeline: Daily
- Gold pipeline: Daily

## Design Rationale
- Sensor continuity is uneven — daily aggregation reduces noise
- City-level averages provide stable signals for cross-domain analysis
- Individual sensors are averaged to reduce bias from uneven spatial coverage
