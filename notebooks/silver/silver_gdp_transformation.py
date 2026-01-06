#!/usr/bin/env python
# coding: utf-8

# ## silver_gdp_transformation
# 
# null

# In[3]:


from pyspark.sql import functions as F


# In[4]:


gdp_bronze = spark.table("bronze_gdp_usa")


# In[5]:


gdp_silver = (
    gdp_bronze
    .select(
        "country_code",
        "country_name",
        F.col("year").cast("int").alias("year"),
        F.col("gdp_usd").cast("double").alias("gdp_usd")
    )
    .filter(F.col("gdp_usd").isNotNull())
)


# In[6]:


(
    gdp_silver
    .write
    .format("delta")
    .mode("overwrite")
    .saveAsTable("silver_gdp")
)

