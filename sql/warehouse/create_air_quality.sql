CREATE TABLE FactAirQualityDaily
AS
SELECT
    date_key,
    parameter_id,
    parameter_name,
    parameter_unit,
    avg_value,
    min_value,
    max_value,
    measurements_count
FROM [urban_analytics_lh].[dbo].[gold_fact_air_quality_daily_staging];