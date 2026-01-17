#!/usr/bin/env python
# coding: utf-8

# ## generate_json
# 
# null

# In[1]:


import requests
import json
from datetime import datetime
from pyspark.sql import functions as F


# In[2]:


dbx_token = "xyz"
file_name = f"weather_report_{datetime.now().strftime('%Y%m%d_%H%M')}.json"


# In[3]:


df = spark.read.table("gold_fact_weather_daily_staging").limit(10)
df_spark = df.withColumn("date", F.col("date").cast("string"))

json_data = df_spark.toPandas().to_json(orient='records')


# In[4]:


url = "https://content.dropboxapi.com/2/files/upload"

headers = {
    "Authorization": f"Bearer {dbx_token}",
    "Dropbox-API-Arg": json.dumps({
        "path": f"/{file_name}",
        "mode": "add",
        "autorename": True,
        "mute": False
    }),
    "Content-Type": "application/octet-stream"
}


# In[5]:


response = requests.post(url, headers=headers, data=json_data.encode('utf-8'))

print(f"Dropbox Status: {response.status_code}")
if response.status_code == 200:
    print(f"File {file_name} uploaded on Dropbox.")
else:
    print(f"Error: {response.text}")

