#!/usr/bin/env python
# coding: utf-8

# ## silver_nyc_taxi_transformation
# 
# null

# In[17]:


from pyspark.sql import functions as F


# In[18]:


yellow_raw = spark.read.parquet("Files/Bronze/nyc_taxi/yellow/trip-data/*")
green_raw = spark.read.parquet("Files/Bronze/nyc_taxi/green/trip-data/*")


# In[19]:


yellow = (
    yellow_raw
    .withColumn("taxi_type", F.lit("yellow"))
    .select(
        F.col("VendorID"),
        F.col("tpep_pickup_datetime").alias("pickup_datetime"),
        F.col("tpep_dropoff_datetime").alias("dropoff_datetime"),
        F.to_date("tpep_pickup_datetime").alias("service_date"),
        F.col("store_and_fwd_flag"),
        F.col("RatecodeID"),
        F.col("PULocationID"),
        F.col("DOLocationID"),
        F.col("passenger_count"),
        F.col("trip_distance"),
        F.col("fare_amount"),
        F.col("extra"),
        F.col("mta_tax"),
        F.col("tip_amount"),
        F.col("tolls_amount"),
        F.lit(None).cast("double").alias("ehail_fee"),
        F.col("improvement_surcharge"),
        F.col("total_amount"),
        F.col("payment_type"),
        F.lit(None).cast("bigint").alias("trip_type"),
        F.col("congestion_surcharge"),
        F.col("Airport_fee"),
        F.col("cbd_congestion_fee"),
        F.col("taxi_type")
    )
)


# In[20]:


green = (
    green_raw
    .withColumn("taxi_type", F.lit("green"))
    .select(
        F.col("VendorID"),
        F.col("lpep_pickup_datetime").alias("pickup_datetime"),
        F.col("lpep_dropoff_datetime").alias("dropoff_datetime"),
        F.to_date("lpep_pickup_datetime").alias("service_date"),
        F.col("store_and_fwd_flag"),
        F.col("RatecodeID"),
        F.col("PULocationID"),
        F.col("DOLocationID"),
        F.col("passenger_count"),
        F.col("trip_distance"),
        F.col("fare_amount"),
        F.col("extra"),
        F.col("mta_tax"),
        F.col("tip_amount"),
        F.col("tolls_amount"),
        F.col("ehail_fee"),
        F.col("improvement_surcharge"),
        F.col("total_amount"),
        F.col("payment_type"),
        F.col("trip_type"),
        F.col("congestion_surcharge"),
        F.lit(None).cast("double").alias("Airport_fee"),
        F.col("cbd_congestion_fee"),
        F.col("taxi_type")
    )
)


# In[21]:


taxi_trips = yellow.unionByName(green)


# In[22]:


valid_events = (
    taxi_trips
    .filter(F.col("pickup_datetime").isNotNull())
    .filter(F.col("dropoff_datetime").isNotNull())
    .filter(F.col("pickup_datetime") <= F.col("dropoff_datetime"))
)


# In[23]:


events_with_ts = valid_events.withColumn(
    "pickup_ts",
    F.unix_timestamp("pickup_datetime")
)

bounds = events_with_ts.approxQuantile(
    "pickup_ts",
    [0.001, 0.999],
    0.0
)

lower_bound_ts, upper_bound_ts = bounds

taxi_clean = (
    events_with_ts
    .filter(
        (F.col("pickup_ts") >= F.lit(lower_bound_ts)) &
        (F.col("pickup_ts") <= F.lit(upper_bound_ts))
    )
    .withColumn(
        "service_date",
        F.to_date("pickup_datetime")
    )
    .drop("pickup_ts")
)


# In[24]:


(
    taxi_clean
    .write
    .format("delta")
    .mode("overwrite")
    .saveAsTable("silver_taxi_trips")
)

