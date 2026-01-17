#!/usr/bin/env python
# coding: utf-8

# ## great_expectations_run
# 
# null

# In[9]:


from great_expectations.data_context import FileDataContext


# In[10]:


path_to_local_context = '/lakehouse/default/Files'

context = FileDataContext.create(project_root_dir=path_to_local_context)


# In[11]:


testing_df = spark.read.table("gold_fact_weather_daily_staging")

weather_asset = context.get_datasource("weather_spark_datasource").get_asset("weather_df_asset")

weather_asset.build_batch_request(dataframe=testing_df)


# In[12]:


results = context.run_checkpoint(checkpoint_name="weather_checkpoint")


# In[13]:


import pandas as pd
from datetime import datetime

def load_data(validated_data):
    validated_data.write.format("delta").mode("overwrite").saveAsTable("validated_weather_data")


# In[14]:


def parse_and_load_checkpoint_result(results):

    validation_results = results['run_results'][next(iter(results['run_results']))]['validation_result']
    success = validation_results['success']

    restructured = {
        "run_name": [results['run_id']['run_name']],
        "run_time": [datetime.strptime(results['run_id']['run_time'][:19], "%Y-%m-%dT%H:%M:%S")],
        "validation_result": [success],
        "evaluated_expectations": [validation_results['statistics']['evaluated_expectations']],
        "successful_expectations": [validation_results['statistics']['successful_expectations']],
        "unsuccessful_expectations": [validation_results['statistics']['unsuccessful_expectations']],
        "success_percent": [validation_results['statistics']['success_percent']],
        "expectation_suite_name": [validation_results['meta']['expectation_suite_name']]
    }

    pandas_df = pd.DataFrame(restructured)
    spark_df = spark.createDataFrame(pandas_df)
    spark_df.write.format("delta").mode("append").saveAsTable("validation_results")

    return success


# In[15]:


success = parse_and_load_checkpoint_result(results.to_json_dict())


# In[16]:


import requests
import json

def send_telegram_report(results_json, success):
    token = "8554748544:AAHEJwTpe3LIQ72K4PHO286ODPYlbBI9jbc"
    chat_id = "7091909358"

    run_result_key = next(iter(results_json['run_results']))
    validation_result = results_json['run_results'][run_result_key]['validation_result']
    stats = validation_result['statistics']
    suite_name = validation_result['meta']['expectation_suite_name']
    

    status_icon = "✅" if success else "❌"
    status_text = "PASSED" if success else "FAILED"
    

    message = f"{status_icon} *Data Quality Report*\n"
    message += f"━━━━━━━━━━━━━━━\n"
    message += f"*Suite:* `{suite_name}`\n"
    message += f"*Status:* {status_text}\n"
    message += f"*Success Rate:* `{stats['success_percent']:.1f}%`\n"
    message += f"*Evaluated:* `{stats['evaluated_expectations']}`\n"
    message += f"*Failed:* `{stats['unsuccessful_expectations']}`\n"
    

    if not success:
        message += "\n *Top Failures:*\n"
        failed_tests = [r for r in validation_result['results'] if not r['success']]
        for fail in failed_tests[:5]: 
            config = fail['expectation_config']
            col = config['kwargs'].get('column', 'Table-level')
            exp_type = config['expectation_type'].replace('expect_column_values_to_', '')
            message += f"• `{col}`: {exp_type}\n"


    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id, 
        "text": message, 
        "parse_mode": "Markdown"
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("Report succesfully sent.")
        else:
            print(f"Telegram Error: {response.text}")
    except Exception as e:
        print(f"Sending error: {e}")


results_dict = results.to_json_dict()


success = parse_and_load_checkpoint_result(results_dict)


send_telegram_report(results_dict, success)


if success:
    load_data(testing_df)
    print("Data loaded to the table.")
else:
    print("Data Quality Check Failed - Check Telegram.")

