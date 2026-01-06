# GDP Pipeline

## Purpose
This pipeline ingests macroeconomic GDP data to provide long-term economic
context for mobility and revenue analysis.

## Data Source
- World Bank API
- Indicator: GDP (current USD)
- Frequency: Yearly
- Records are overwritten by year to ensure idempotent ingestion

## Pipeline Structure

### 1. Bronze Ingestion
- Tool: Dataflow Gen2
- Method: REST API pull
- Target: Bronze GDP table

### 2. Silver Transformation
- Tool: PySpark Notebook
- Notebook: `silver_gdp_transformation.py`

**Responsibilities**
- JSON normalization
- Numeric casting
- Country filtering (USA)
- Validation of yearly values

**Output**
- `silver_gdp`

### 3. Gold Transformation
- Tool: PySpark Notebook
- Notebook: `gold_dimgdp.py`

**Responsibilities**
- Exposure as `DimGDP`
- Time-based economic context

**Output**
- `gold_dim_gdp_staging`

## Scheduling
- Monthly (low volatility) sufficient due to the annual publication frequency of GDP data.

## Design Rationale
GDP is used strictly as contextual data:
- No joins at transaction level
- Visualization-only enrichment
- DimGDP can be related to DimDate via the calendar year for contextual analysis
