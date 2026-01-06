#!/usr/bin/env python
# coding: utf-8

# ## gold_fact_air_quality_daily
# 
# null

# In[5]:


from pyspark.sql import functions as F


# In[6]:


aq_daily_silver = spark.table("silver_air_quality_daily")
dim_date = spark.table("gold_dim_date_staging")


# In[7]:


fact_air_quality_daily = (
    aq_daily_silver
    .withColumnRenamed("measurement_date", "date")
    .join(
        dim_date.select("date", "date_key"),
        on="date",
        how="left"
    )
)


# In[8]:


fact_air_quality_daily = fact_air_quality_daily.select(
    "date_key",
    "date",
    "parameter_id",
    "parameter_name",
    "parameter_unit",
    "avg_value",
    "min_value",
    "max_value",
    "measurements_count"
)


# In[9]:


(
    fact_air_quality_daily
    .write
    .format("delta")
    .mode("overwrite")
    .saveAsTable("gold_fact_air_quality_daily_staging")
)

