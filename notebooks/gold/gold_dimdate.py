#!/usr/bin/env python
# coding: utf-8

# ## gold_dimdate
# 
# null

# In[5]:


from pyspark.sql import functions as F


# In[6]:


dates = (
    spark.table("silver_taxi_daily")
    .select(F.col("service_date").alias("date"))
    .union(
        spark.table("silver_air_quality_daily")
        .select(F.col("measurement_date").alias("date"))
    )
    .union(
        spark.table("silver_fx_daily")
        .select(F.col("fx_date").alias("date"))
    )
    .filter(F.col("date").isNotNull())
    .distinct()
)


# In[7]:


dim_date = (
    dates
    .withColumn("date_key", F.date_format("date", "yyyyMMdd").cast("int"))
    .withColumn("year", F.year("date"))
    .withColumn("quarter", F.quarter("date"))
    .withColumn("month", F.month("date"))
    .withColumn("month_name", F.date_format("date", "MMMM"))
    .withColumn("day", F.dayofmonth("date"))
    .withColumn("day_of_week", F.dayofweek("date"))
    .withColumn("day_name", F.date_format("date", "EEEE"))
    .withColumn(
        "is_weekend",
        F.col("day_of_week").isin([1, 7])
    )
)


# In[8]:


(
    dim_date
    .write
    .format("delta")
    .mode("overwrite")
    .saveAsTable("gold_dim_date_staging")
)

