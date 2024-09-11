import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)

input_df = glueContext.create_dynamic_frame_from_options(
  connection_type="s3",
  connection_options = {
    "paths": ["s3://bots-taijitu-intermediate-data-export/example.ddb.insert.json.txt"]
  },
  format = "json"
)

input_df.show()

df = input_df.toDF()

df_pd = df.toPandas()

df_pd.head()

print('test script has successfully ran')