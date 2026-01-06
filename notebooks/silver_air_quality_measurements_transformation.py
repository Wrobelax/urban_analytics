#!/usr/bin/env python
# coding: utf-8

# ## silver_air_quality_measurements_transformation
# 
# null

# In[1]:


from pyspark.sql import functions as F


# In[2]:


aq_bronze = spark.table("bronze_air_quality_measurements")


# In[3]:


aq_silver = (
    aq_bronze
    .withColumn(
        "measurement_datetime",
        F.col("period_from_utc").cast("timestamp")
    )
    .withColumn(
        "measurement_date",
        F.to_date("measurement_datetime")
    )
    .select(
        F.col("sensor_id"),
        F.col("parameter_id"),
        F.col("parameter_name"),
        F.col("parameter_unit"),
        F.col("value").cast("double"),
        F.col("measurement_datetime"),
        F.col("measurement_date")
    )
)


# In[4]:


aq_silver = aq_silver.dropDuplicates(
    ["sensor_id", "parameter_id", "measurement_datetime"]
)


# In[5]:


(
    aq_silver
    .write
    .format("delta")
    .mode("overwrite")
    .saveAsTable("silver_air_quality_measurements")
)

