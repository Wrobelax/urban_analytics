#!/usr/bin/env python
# coding: utf-8

# ## great_expectations_conf
# 
# null

# In[49]:


import great_expectations as gx


# In[50]:


context = gx.get_context()
context.add_or_update_expectation_suite("weather_expectation_suite")


# In[51]:


datasource = context.sources.add_spark("weather_spark_datasource")
data_asset = datasource.add_dataframe_asset("weather_df_asset")


# In[52]:


weather_df = spark.read.table("gold_fact_weather_daily_staging")
my_batch_request = data_asset.build_batch_request(dataframe=weather_df)


# In[53]:


validator = context.get_validator(
    batch_request=my_batch_request,
    expectation_suite_name="weather_expectation_suite",
)


# In[54]:


validator.expect_column_values_to_not_be_null(column='temp_max')
validator.expect_column_values_to_not_be_null(column='temp_min')
validator.expect_column_values_to_not_be_null(column='precip_sum')
validator.expect_column_values_to_not_be_null(column='wind_max')

validator.expect_column_values_to_be_between("temp_max", min_value=-50, max_value=60)
validator.expect_column_values_to_be_between("temp_min", min_value=-60, max_value=50)
validator.expect_column_values_to_be_between("wind_max", min_value=0, max_value=250)
validator.expect_column_values_to_be_between("precip_sum", min_value=0, max_value=500)

validator.save_expectation_suite(discard_failed_expectations=False)


# In[55]:


checkpoint_name = "weather_checkpoint"

yaml_config = f"""
name: weather_checkpoint
config_version: 1.0
class_name: SimpleCheckpoint
run_name_template: "%Y%m%d-%H%M%S-weather-run-name-template"
validations:
   - batch_request:
        datasource_name: weather_spark_datasource
        data_asset_name: weather_df_asset
expectation_suite_name: weather_expectation_suite
"""

weather_checkpoint = context.test_yaml_config(yaml_config=yaml_config)

context.add_checkpoint(checkpoint=weather_checkpoint)

checkpoint_run_result = context.run_checkpoint(
    checkpoint_name="weather_checkpoint"
)


# In[56]:


context = context.convert_to_file_context()

get_ipython().system('cp -r great_expectations/ /lakehouse/default/Files/')

