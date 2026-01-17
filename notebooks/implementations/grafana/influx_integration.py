#!/usr/bin/env python
# coding: utf-8

# ## influx_integration
# 
# null

# In[1]:


from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime, timedelta


# In[2]:


df = spark.table("gold_fact_weather_daily_staging")
df = df.toPandas()


# In[3]:


today = datetime.utcnow().date()
last_month = today - timedelta(days=29)
df = df[(df["date"] >= last_month) & (df["date"] <= today)]


# In[4]:


influx_url = "xyz"
influx_token = "xyz"
influx_org = "Urban Analytics"
influx_bucket = "weather"


# In[5]:


client = InfluxDBClient(url=influx_url, token=influx_token, org=influx_org)
write_api = client.write_api(write_options=SYNCHRONOUS)

for _, row in df.iterrows():
    point = (
        Point("weather_daily")
        .tag("location", "NYC")
        .field("temp_max", float(row["temp_max"]))
        .field("temp_min", float(row["temp_min"]))
        .field("precip_sum", float(row["precip_sum"]))
        .field("wind_max", float(row["wind_max"]))
        .time(datetime.combine(row["date"], datetime.min.time()), WritePrecision.NS)
    )
    write_api.write(bucket=influx_bucket, org=influx_org, record=point)

client.close()

