#!/usr/bin/env python
# coding: utf-8

# ## silver_taxi_zones_lookup
# 
# null

# In[1]:


from pyspark.sql import functions as F


# In[2]:


silver_zone_lookup = (
    spark.table("bronze_taxi_zone_lookup")
    .select(
        F.col("LocationID").cast("int").alias("zone_id"),
        F.col("Borough").alias("borough"),
        F.col("Zone").alias("zone_name"),
        F.col("service_zone")
    )
)


# In[3]:


silver_zone_lookup.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("silver_zone_lookup")

