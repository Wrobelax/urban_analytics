#!/usr/bin/env python
# coding: utf-8

# ## gold_dimfx
# 
# null

# In[2]:


spark.table("silver_fx_daily") \
    .write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("gold_dim_fx_staging")

