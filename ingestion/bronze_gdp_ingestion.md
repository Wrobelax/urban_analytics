# GDP – Bronze Ingestion

## Purpose
This ingestion process retrieves raw GDP data
to provide macroeconomic context.

## Data Source
- Provider: World Bank
- Indicator: NY.GDP.MKTP.CD
- Format: JSON
- Frequency: Yearly

## Ingestion Tool
- Dataflow Gen2 (Microsoft Fabric)

## Ingestion Strategy
- Country-specific pull (USA)
- Full historical dataset ingestion
- Stateless refresh

## Target Storage
- OneLake / Lakehouse
- Bronze GDP table

## Transformations
- NONE
- JSON normalization only
- No filtering
- No aggregation

## Error Handling
- API failures stop the Dataflow
- Low update frequency minimizes operational risk

## Design Rationale
- GDP data is contextual, not transactional
- Retained fully for long-term trend analysis