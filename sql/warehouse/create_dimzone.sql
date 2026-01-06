CREATE TABLE DimZone
AS
SELECT
    zone_id,
    borough,
    zone_name,
    service_zone
FROM [urban_analytics_lh].[dbo].[gold_dim_zone_staging];