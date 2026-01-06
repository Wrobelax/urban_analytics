#!/usr/bin/env python
# coding: utf-8

# ## silver_air_quality_daily_transformation
# 
# null

# In[1]:


from pyspark.sql import functions as F


# In[2]:


aq_measurements = spark.table("silver_air_quality_measurements")


# In[3]:


aq_clean = (
    aq_measurements
    .filter(F.col("value").isNotNull())
    .filter(F.col("value") >= 0)
)


# In[4]:


aq_daily = (
    aq_clean
    .groupBy(
        "measurement_date",
        "parameter_id",
        "parameter_name",
        "parameter_unit"
    )
    .agg(
        F.avg("value").alias("avg_value"),
        F.min("value").alias("min_value"),
        F.max("value").alias("max_value"),
        F.count("*").alias("measurements_count")
    )
)


# In[5]:


aq_daily = aq_daily.select(
    "measurement_date",
    "parameter_id",
    "parameter_name",
    "parameter_unit",
    "avg_value",
    "min_value",
    "max_value",
    "measurements_count"
)


# In[6]:


(
    aq_daily
    .write
    .format("delta")
    .mode("overwrite")
    .saveAsTable("silver_air_quality_daily")
)

