CREATE TABLE DimDate
AS
SELECT
    date_key,
    date,
    year,
    quarter,
    month,
    month_name,
    day,
    day_of_week,
    day_name,
    is_weekend
FROM [urban_analytics_lh].[dbo].[gold_dim_date_staging];