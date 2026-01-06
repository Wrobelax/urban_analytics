# OpenAQ – Bronze Ingestion

## Purpose
This ingestion process retrieves raw air quality measurements
from the OpenAQ API and lands them into the Bronze layer.

The Bronze layer preserves raw API payloads for traceability.

## Data Source
- Provider: OpenAQ
- API version: v3
- Endpoint:
  /sensors/{sensor_id}/measurements
- Parameters:
  - PM2.5
  - PM10
  - NO2
  - SO2
  - O3
- Authentication:
  - API Key (header-based)

## Ingestion Tool
- Dataflow Gen2 (Microsoft Fabric)

## Ingestion Strategy
- Sensor-driven ingestion:
  - Sensor IDs sourced from a lookup table
- Pagination:
  - limit = 1000
  - multiple pages per sensor
- Time filtering:
  - datetime_from parameter (e.g. 2025-01-01)
- Data is ingested incrementally using datetime filters, enabling idempotent reprocessing

## Target Storage
- OneLake / Lakehouse
- Bronze tables:
  - Raw measurement-level records, one row per sensor, timestamp, and parameter.

## Transformations
- JSON expansion only
- Datetime fields preserved
- No aggregation
- No deduplication
- No filtering beyond API-level constraints

## Error Handling
- Sensors with no data return empty result sets
- Pagination stops when no results are returned
- Partial sensor coverage is expected and accepted

## Design Rationale
- Raw measurements are preserved to:
  - Allow future re-aggregation
  - Audit sensor-level gaps
  - Support alternative aggregation strategies