# FX (USD/EUR) Pipeline

## Purpose
This pipeline ingests daily foreign exchange rates to convert taxi revenue
from USD to EUR for economic context analysis.

## Data Source
- European Central Bank (ECB)
- Format: CSV via REST API
- Frequency: Daily

## Pipeline Structure

### 1. Bronze Ingestion
- Tool: Dataflow Gen2
- Method: CSV API pull
- Target: Bronze FX table
- Daily rates are overwritten by date to ensure idempotent ingestion.

### 2. Silver Transformation
- Tool: PySpark Notebook
- Notebook: `silver_fx_daily.py`

**Responsibilities**
- Date normalization
- Numeric type casting
- Deduplication
- Validation of exchange rates

**Output**
- `silver_fx_daily`

### 3. Gold Transformation
- Tool: PySpark Notebook
- Notebook: `gold_dimfx.py`

**Responsibilities**
- Exposure as `DimFX`
- Join-ready daily FX rates

**Output**
- `gold_dim_fx_staging`

**Usage**
- Applied during visualization stage
- Converts daily taxi revenue:
  - USD → EUR

## Scheduling
- Daily scheduling aligns FX rates with daily taxi and air quality aggregates.

## Design Rationale
FX is treated as a dimension:
- Small, stable dataset
- Frequently joined
- Time-dependent lookup behavior
- DimFX is joined to facts using the calendar date shared with DimDate
