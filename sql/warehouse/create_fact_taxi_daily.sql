CREATE TABLE FactTaxiDaily
AS
SELECT
    date_key,
    pickup_zone_id,
    taxi_type,
    trips_count,
    total_distance,
    avg_trip_distance,
    total_revenue_usd,
    avg_fare_usd
FROM [urban_analytics_lh].[dbo].[gold_fact_taxi_daily_staging];