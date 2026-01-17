#!/usr/bin/env python
# coding: utf-8

# ## silver_weather
# 
# null

# In[1]:


from pyspark.sql import functions as F


# In[2]:


bronze_weather = spark.table("bronze_weather_data")


# In[3]:


silver_weather = (
    bronze_weather
    .withColumn("date", F.to_date("date"))
    .withColumn("temp_max", F.col("temp_max").cast("double"))
    .withColumn("temp_min", F.col("temp_min").cast("double"))
    .withColumn("precip_sum", F.col("precip_sum").cast("double"))
    .withColumn("wind_max", F.col("wind_max").cast("double"))
)


# In[4]:


silver_weather.write.format("delta") \
    .mode("overwrite") \
    .saveAsTable("silver_weather_daily")

