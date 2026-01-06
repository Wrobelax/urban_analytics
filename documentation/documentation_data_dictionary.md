# Urban Analytics – Data Dictionary

This data dictionary documents the Gold-layer tables used for analytics and reporting
in the project.

The project integrates:
- NYC Taxi mobility data
- OpenAQ air quality data
- World Bank GDP and ECB FX macroeconomic data


## FactTaxiDaily

FactTaxiDaily is the primary fact table for mobility analysis and revenue reporting.

Daily aggregated taxi metrics by pickup zone.

**Grain:** One row per `service date` and `pickup zone`.

**Foreign keys:** 
date_key → DimDate.date_key, pickup_zone_id → DimZone.zone_id

### Columns

| Column | Type | Description |
|------|-----|------------|
| date_key | int | Surrogate key referencing DimDate |
| date | date | Taxi service date |
| pickup_zone_id | int | NYC Taxi pickup zone identifier |
| trips_count | bigint | Number of taxi trips |
| total_revenue_usd | double | Total taxi revenue in USD |
| avg_fare_usd | double | Average fare per trip in USD |
| taxi_type | string | Taxi service type (yellow / green) |
| total_distance | double | Total trip distance |
| avg_trip_distance | double | Average trip distance |


## DimDate

Calendar date dimension used for time-based analysis.

### Columns

| Column | Type | Description |
|------|-----|------------|
| date_key | int | Surrogate key in YYYYMMDD format |
| date | date | Calendar date |
| year | int | Year number |
| quarter | int | Quarter number (1–4) |
| month | int | Month number (1–12) |
| month_name | string | Month name |
| day | int | Day of month |
| day_of_week | int | Day of week number |
| day_name | string | Day of week name |
| is_weekend | boolean | Indicates weekend (Saturday/Sunday) |


## DimZone

NYC Taxi pickup and drop-off zone dimension.

### Columns

| Column | Type | Description |
|------|-----|------------|
| zone_id | int | NYC Taxi zone identifier |
| zone_name | string | Taxi zone name |
| borough | string | Borough name |
| service_zone | string | Service zone classification |


## DimFX

Daily foreign exchange rates used for revenue conversion. **Grain**: One row per exchange rate date.

### Columns

| Column | Type | Description |
|------|-----|------------|
| fx_date | date | Exchange rate date. Join key to DimDate.date. |
| usd_eur_rate | double | USD to EUR exchange rate |

## DimGDP

Macroeconomic GDP indicators by country and year.

### Columns

| Column | Type | Description |
|------|-----|------------|
| year | int | Calendar year |
| gdp_usd | double | Gross Domestic Product in USD |
| country_code | string | Country ISO code |
| country_name | string | Country name |

## FactAirQualityDaily

Daily aggregated air quality measurements. Sensor-level granularity allows flexible aggregation to city or zone level during analysis.

**Grain:**  
One row per `date`, `sensor`, and `pollutant`.

### Columns

| Column | Type | Description |
|------|-----|------------|
| date_key | int | Surrogate key referencing DimDate |
| date | date | Measurement date |
| sensor_id | int | Air quality sensor identifier |
| parameter_id | int | Pollutant identifier |
| parameter_name | string | Pollutant name (e.g. PM2.5, NO2) |
| parameter_unit | string | Measurement unit |
| avg_value | double | Daily average pollutant value |
| min_value | double | Daily minimum pollutant value |
| max_value | double | Daily maximum pollutant value |
| measurements_count | int | Number of measurements per day |

