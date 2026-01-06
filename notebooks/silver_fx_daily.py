#!/usr/bin/env python
# coding: utf-8

# ## silver_fx_daily
# 
# null

# In[10]:


from pyspark.sql import functions as F


# In[11]:


fx_bronze = spark.table("bronze_fx_usd")


# In[12]:


fx_silver = (
    fx_bronze
    .select(
        F.to_date("date").alias("fx_date"),
        F.col("usd_to_eur").cast("double").alias("usd_eur_rate")
    )
    .filter(F.col("usd_eur_rate").isNotNull())
)


# In[13]:


fx_silver = fx_silver.dropDuplicates(["fx_date"])


# In[14]:


fx_silver = fx_silver.filter(
    (F.col("usd_eur_rate") > 0.5) & (F.col("usd_eur_rate") < 2.0)
)


# In[15]:


(
    fx_silver
    .write
    .format("delta")
    .mode("overwrite")
    .saveAsTable("silver_fx_daily")
)

