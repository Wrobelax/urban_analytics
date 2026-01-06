# NYC Taxi – Bronze Ingestion

## Purpose
This ingestion process lands raw NYC Taxi Trip data into the Bronze layer
of the Fabric Lakehouse without enforcing schema or business rules.

The Bronze layer acts as a durable, auditable raw data store.

## Data Source
- Provider: NYC Taxi & Limousine Commission (TLC)
- Format: Parquet
- Taxi types:
  - Yellow Taxi
  - Green Taxi
- Source URLs:
  - CloudFront-hosted monthly Parquet files
  - Example:
    https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2025-01.parquet

## Ingestion Tool
- Microsoft Fabric Data Pipeline
- Control flow: ForEach
- Activities: Copy Data (Yellow, Green)

## Ingestion Strategy
- Monthly files are ingested independently
- A predefined list of expected months (2025-01 to 2025-11) is iterated
- Pipeline is idempotent and can be re-run

## Target Storage
- OneLake / Lakehouse
- Bronze layer
- Folder structure: bronze/nyc_taxi/{taxi_type}/trip-data/

## Transformations
- NONE
- Files are copied as-is
- No filtering
- No deduplication
- No schema enforcement

## Error Handling
- Missing monthly files are skipped
- Failed copy operations do not block the pipeline
- Partial availability is expected due to TLC publication lag

## Design Rationale
- Raw data preservation enables:
- Reprocessing
- Auditing
- Schema evolution
- Business logic is intentionally deferred to Silver
