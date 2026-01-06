CREATE TABLE DimGDP
AS
SELECT
    year,
    gdp_usd
FROM [urban_analytics_lh].[dbo].[gold_dim_gdp_staging];