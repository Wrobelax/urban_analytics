CREATE TABLE DimFX
AS
SELECT
    fx_date,
    usd_eur_rate
FROM [urban_analytics_lh].[dbo].[gold_dim_fx_staging];