#!/usr/bin/env python
# coding: utf-8

# ## gold_dimgdp
# 
# null

# In[1]:


spark.table("silver_gdp") \
    .write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("gold_dim_gdp_staging")

