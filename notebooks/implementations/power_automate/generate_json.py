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


dbx_token = "sl.u.AGOex_wvyQl2jcTef7WXZq9kOdcBuNV_FKy-clE30p1olPsE5wgqBnMCUlog_VyM6YttF-vKY7jjxM9DhI06g3rb8F8z_QKUxfMuRvrFzA-Jb-q9GzS7o_8SYwwsET-us-ooHLPm1Ha6YsN18RDdFy74h00TuZNa_oeUlgD8LuGbU_i_KCQNRXGt-YihNb8d-ISnFhrCidpAtNg0NAlOOLaiSK7T9j7mcxxTUzXWoFGvKGzKM_rBAc4sL8KD_1mT4tXewJyCKNy8nItKjjL8VdnzfT9rwoSvbMvTv9Y26h-khs0-fklNwUd7lGJClS7nzySI9OGqvBmmcyW5OKHC2lghVmHoQu9CPD-19ppuMxteQS4EfntfkH1y78-CZCRzTUfMEiLkC_Sb3z-G_gqKTHqqqS_wlucwNcpFVyJKW41_VVOzr4xzfqK9ofQHMMbTpKNZ4Bbnnt1dG3UZZuBN8I_Q9Ot4qP8atHpLa4dCbyIzRi5l1LtsTbhOi6-aqND6KaYEJkKHvrtCaCqiv7fa48RZjwLgPqZRpqaf-X0siOIcE6L4b9a4uGr5V3l0lI9J1nYxR2zYyiG-I4-w_00uPhb1aFTMY_UALcUgncZv-G7Y_x8lO2N0XwodAa0L80zy7PqfYOmrmM3AGDS6UE8BDWZ4V0kATliVUvcrN5K0VcGhbJqsB_pFJHnnjj60FbxqtwTjWutUw2ICtWSGLokHrwZqTNC99NqxWVsVBJnyqFixlhILSc_n8iyikH6DinkF_ETf6IswYg79ZQVN3sAAXd6A7bUqUPK04MjCvaQz77-17LqsSngzeAWRf7CpJFmXLiqsvEA_EwSvZOfaFkuWFcczKzvST26vb5ZgiR1NlmaoM3R8wqGrE-ghea_U1Ky_PKPpFtDUOK8hXX-4al5YKjCCWGcSa_BzvSAGuJ1dxjBl--8vAB3j-_lIXcZI1_Kjt0Ies8uHxVXck1w51sE3LhlRM_5FPeJJQmLBCiF1TdhuPY75jJP490UYF1UKwaaSPuNyL1Tdu8zU99PcLLexkuKwYmRhfji32cD4SCuuTxtPdZgEOThngkjZ15chAGVEOZ-VrAeyQhivc5XyZevAfyGpKmyPMBZsd5BGUf5QnJKv4r7vdIFgPCaXdi2xmJZGwpO63f0rwUKhOhA9LDbZPOhvAOBhsIBTBUtTuPF-bMVRdozaVdEnGONyUEr9kigJzaov0fTKPXvD3fjJPmjOb_tDEc0irxU3F9SAPTa7AGGZsZ3uDi-yF8Q6sjUAy8mn60vGh_pbDNiZkPh23_MfoAeIA47zw5AWiP7-RjEkrUr7WwVFJi8V5zQBR2KRcBxMKBZxqPxH3nVbjBaieuQEVq_YTLM86tzPYjIjAjYJDfUa7sVfHtP_OcgYdppipZ1N2ujAgQkXh0yqXpJWqlt-mmAX"
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

