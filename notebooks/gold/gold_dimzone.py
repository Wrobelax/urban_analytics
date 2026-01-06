#!/usr/bin/env python
# coding: utf-8

# ## gold_dimzone
# 
# null

# In[3]:


spark.table("silver_zone_lookup") \
    .write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("gold_dim_zone_staging")

