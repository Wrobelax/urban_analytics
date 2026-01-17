# Open-Meteo – Bronze Ingestion

## Purpose
This ingestion process retrieves raw historical weather data
from the Open-Meteo Archive API and lands them into the Bronze layer.

The Bronze layer preserves unmodified API responses for traceability and reprocessing.

## Data Source
- Provider: Open-Meteo
- API version: Archive v1
- Endpoint:
  `/v1/archive`
- Parameters:
  - `temp__max`
  - `temp__min`
  - `precip_sum`
  - `wind_max`
- Timezone: America/New_York (passed explicitly to API)
- Authentication: None (public API)

## Ingestion Tool
- Dataflow Gen2 (Microsoft Fabric)

## Ingestion Strategy
- Location-driven ingestion:
  - Static coordinates: New York City (`lat=40.7128`, `lon=-74.0060`)
- Date range:
  - start_date=2025-01-01
  - end_date=today
- Data is retrieved as daily summaries
- API returns all requested variables in a single payload

## Target Storage
- OneLake / Lakehouse
- Bronze table:
  - One row per date, per location, with all selected variables

## Transformations
- Flattening of nested JSON structure
- Mapping to columns:
  - `date`, `temp_max`, `temp_min`, `precip_sum`, `wind_max`
- No deduplication
- No null filtering
- No unit conversion (values are preserved as-is from API: **°C** for temperature, **mm** for precipitation, **km/h** for wind speed)

## Error Handling
- API call failures are surfaced in Power Query logs
- Empty results are handled gracefully
- Retry is possible by re-triggering Dataflow refresh

## Design Rationale
- Raw weather metrics are preserved to:
  - Enable consistent enrichment of air quality metrics
  - Support temporal joins in Gold layer
  - Allow aggregation flexibility downstream
