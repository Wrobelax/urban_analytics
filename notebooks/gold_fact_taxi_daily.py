#!/usr/bin/env python
# coding: utf-8

# ## gold_fact_taxi_daily
# 
# null

# In[9]:


from pyspark.sql import functions as F


# In[10]:


taxi_silver = spark.table("silver_taxi_trips")


# In[11]:


taxi_daily_raw = (
    taxi_silver
    .groupBy(
        "service_date",
        "taxi_type",
        "PULocationID"
    )
    .agg(
        F.count("*").alias("trips_count"),
        F.sum("total_amount").alias("total_revenue_usd"),
        F.avg("fare_amount").alias("avg_fare_usd"),
        F.sum("trip_distance").alias("total_distance"),
        F.avg("trip_distance").alias("avg_trip_distance")
    )
)


# In[12]:


dim_date = spark.table("gold_dim_date_staging")

fact_taxi_daily_with_date = (
    taxi_daily_raw.alias("f")
    .join(
        dim_date.alias("d"),
        F.col("f.service_date") == F.col("d.date"),
        how="inner"
    )
    .select(
        F.col("d.date_key"),
        F.col("f.service_date"),
        F.col("f.taxi_type"),
        F.col("f.PULocationID"),
        F.col("f.trips_count"),
        F.col("f.total_revenue_usd"),
        F.col("f.avg_fare_usd"),
        F.col("f.total_distance"),
        F.col("f.avg_trip_distance")
    )
)


# In[13]:


fact_taxi_daily = (
    fact_taxi_daily_with_date
    .select(
        F.col("service_date").alias("date"),
        F.col("PULocationID").alias("pickup_zone_id"),
        F.col("taxi_type"),
        F.col("trips_count"),
        F.col("total_distance"),
        F.col("avg_trip_distance"),
        F.col("total_revenue_usd"),
        F.col("avg_fare_usd"),
        F.col("date_key")
    )
)


# In[14]:


(
    fact_taxi_daily
    .write
    .format("delta")
    .mode("overwrite")
    .saveAsTable("gold_fact_taxi_daily_staging")
)

