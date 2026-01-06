# FX (USD/EUR) – Bronze Ingestion

## Purpose
This ingestion process retrieves raw foreign exchange rates
from the European Central Bank for economic normalization.

## Data Source
- Provider: European Central Bank (ECB)
- Dataset: USD/EUR spot exchange rate
- Format: CSV
- Frequency: Daily

## Ingestion Tool
- Dataflow Gen2 (Microsoft Fabric)

## Ingestion Strategy
- Full dataset pull on each execution
- Stateless ingestion
- Historical values are overwritten safely
- Idempotent full refresh on each run

## Target Storage
- OneLake / Lakehouse
- Bronze FX table (daily USD/EUR rates)

## Transformations
- NONE
- Raw CSV fields only
- No filtering
- No deduplication

## Error Handling
- API availability failures fail the Dataflow
- Retry handled by Fabric scheduling
- Short-term API outages do not impact downstream analytics due to historical stability of FX rates

## Design Rationale
- FX data is small and stable
- Full refresh is simpler and safer than incremental logic