#!/usr/bin/env python
# coding: utf-8

# ## gold_weather
# 
# null

# In[1]:


from pyspark.sql import functions as F


# In[2]:


weather_silver = spark.table("silver_weather_daily")
dim_date = spark.table("gold_dim_date_staging")


# In[3]:


weather_gold = (
    weather_silver
    .join(dim_date.select("date", "date_key"), on="date", how="left")
)


# In[4]:


weather_gold = weather_gold.select(
    "date_key",
    "date",
    "temp_max",
    "temp_min",
    "precip_sum",
    "wind_max"
)


# In[5]:


weather_gold.write.format("delta") \
    .mode("overwrite") \
    .saveAsTable("gold_fact_weather_daily_staging")

