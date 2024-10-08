import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import col, from_json, explode_outer, current_timestamp, lpad, year, month, dayofmonth
from pyspark.sql.types import StringType, StructType, StructField, ArrayType, DoubleType


args = getResolvedOptions(sys.argv, ["KAFKA_BOOTSTRAP_SERVERS",
                                     "KAFKA_SASL_JAAS_CONFIG",
                                     "KAFKA_SSL_TRUSTSTORE_LOCATION",
                                     "KAFKA_SSL_TRUSTSTORE_PASSWORD",
                                     "DATA_LOCATION",
                                     "CHECKPOINT_LOCATION"])
print(args)

sc = SparkContext.getOrCreate()

glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init("waf_entry", args)


# KAFKA_BOOTSTRAP_SERVERS = 'alikafka-post-cn-9t93w71ti003-1.alikafka.aliyuncs.com:9093,alikafka-post-cn-9t93w71ti003-2.alikafka.aliyuncs.com:9093,alikafka-post-cn-9t93w71ti003-3.alikafka.aliyuncs.com:9093'
# KAFKA_SASL_JAAS_CONFIG = 'org.apache.kafka.common.security.plain.PlainLoginModule required username="test1234" password="Test1234";'
# KAFKA_SSL_TRUSTSTORE_LOCATION = '/tmp/mix.4096.client.truststore.jks'
# KAFKA_SSL_TRUSTSTORE_PASSWORD = 'KafkaOnsClient'
# KAFKA_SUBSCRIBE = 'test'
# DATA_LOCATION = 's3://nike-commerce-test-app-internal/testKafka/dataDir'
# CHECKPOINT_LOCATION = 's3://nike-commerce-test-app-internal/testKafka/checkPointDir'

KAFKA_BOOTSTRAP_SERVERS = 'alikafka-post-cn-9t93w71ti003-1.alikafka.aliyuncs.com:9093,alikafka-post-cn-9t93w71ti003-2.alikafka.aliyuncs.com:9093,alikafka-post-cn-9t93w71ti003-3.alikafka.aliyuncs.com:9093'
KAFKA_SASL_JAAS_CONFIG = 'org.apache.kafka.common.security.plain.PlainLoginModule required username="test1234" password="Test1234";'
KAFKA_SSL_TRUSTSTORE_LOCATION = '/tmp/mix.4096.client.truststore.jks'
KAFKA_SSL_TRUSTSTORE_PASSWORD = 'KafkaOnsClient'
KAFKA_SUBSCRIBE = 'test'
DATA_LOCATION = 's3://nike-commerce-test-app-internal/testKafka/dataDir'
CHECKPOINT_LOCATION = 's3://nike-commerce-test-app-internal/testKafka/checkPointDir'

kafka_params = {
    "kafka.bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS,
    "kafka.security.protocol": "SASL_SSL",
    "kafka.sasl.mechanism": "PLAIN",
    "kafka.sasl.jaas.config": KAFKA_SASL_JAAS_CONFIG,
    "kafka.ssl.truststore.location": KAFKA_SSL_TRUSTSTORE_LOCATION,
    "kafka.ssl.truststore.password": KAFKA_SSL_TRUSTSTORE_PASSWORD,
    "kafka.ssl.endpoint.identification.algorithm": "",
    "subscribe": KAFKA_SUBSCRIBE,
    "startingoffsets": "latest"
}

schema = StructType([
    StructField("real_client_ip", StringType(), True),
    StructField("user_id", StringType(), True),
    StructField("status", StringType(), True),
    StructField("response_set_cookie", StringType(), True),
    StructField("bypass_matched_ids", StringType(), True),
    StructField("matched_host", StringType(), True),
    StructField("request_traceid", StringType(), True),
    StructField("http_user_agent", StringType(), True),
    StructField("request_length", StringType(), True),
    StructField("wxbb_info_tbl", StringType(), True),
    StructField("upstream_addr", StringType(), True),
    StructField("upstream_response_time", StringType(), True),
    StructField("http_x_forwarded_for", StringType(), True),
    StructField("region", StringType(), True),
    StructField("request_time_msec", StringType(), True),
    StructField("body_bytes_sent", StringType(), True),
    StructField("wxbb_invalid_wua", StringType(), True),
    StructField("remote_addr", StringType(), True),
    StructField("https", StringType(), True),
    StructField("request_traceid_origin", StringType(), True),
    StructField("request_body", StringType(), True),
    StructField("request_method", StringType(), True),
    StructField("http_referer", StringType(), True),
    StructField("server_port", StringType(), True),
    StructField("server_protocol", StringType(), True),
    StructField("upstream_status", StringType(), True),
    StructField("querystring", StringType(), True),
    StructField("http_cookie", StringType(), True),
    StructField("ssl_protocol", StringType(), True),
    StructField("host", StringType(), True),
    StructField("request_path", StringType(), True),
    StructField("ssl_cipher", StringType(), True),
    StructField("remote_port", StringType(), True),
    StructField("content_type", StringType(), True),
    StructField("time", StringType(), True),
    StructField("__pack_meta__", StringType(), True),
    StructField("__topic__", StringType(), True),
    StructField("__source__", StringType(), True),
    StructField("__time__", StringType(), True)
])

df = spark.readStream.format("kafka") \
    .options(**kafka_params) \
    .load() \
    .selectExpr("CAST(value AS STRING)") \
    .select(from_json("value", schema).alias("data")) \
    .select("data.*")

request_body_schema = StructType([
    StructField("locale", StringType(), nullable=True),
    StructField("totals", StructType([
        StructField("fulfillment", StructType([
            StructField("details", StructType([
                StructField("price", DoubleType(), nullable=True),
                StructField("discount", DoubleType(), nullable=True)
            ]), nullable=True),
            StructField("total", DoubleType(), nullable=True)
        ]), nullable=True),
        StructField("items", StructType([
            StructField("details", StructType([
                StructField("price", DoubleType(), nullable=True),
                StructField("discount", DoubleType(), nullable=True)
            ]), nullable=True),
            StructField("total", DoubleType(), nullable=True)
        ]), nullable=True),
        StructField("taxes", StructType([
            StructField("details", StructType([
                StructField("items", StructType([
                    StructField("type", StringType(), nullable=True)
                ]), nullable=True)
            ]), nullable=True)
        ]), nullable=True)
    ]), nullable=True),
    StructField("checkoutId", StringType(), nullable=True),
    StructField("shipping", StructType([
        StructField("address", StructType([
            StructField("county", StringType(), nullable=True),
            StructField("state", StringType(), nullable=True),
            StructField("address1", StringType(), nullable=True),
            StructField("city", StringType(), nullable=True),
            StructField("country", StringType(), nullable=True)
        ]), nullable=True),
        StructField("recipient", StructType([
            StructField("firstName", StringType(), nullable=True),
            StructField("email", StringType(), nullable=True),
            StructField("lastName", StringType(), nullable=True),
            StructField("phoneNumber", StringType(), nullable=True)
        ]), nullable=True),
        StructField("getBy", StructType([
            StructField("maxDate", StructType([
                StructField("dateTime", StringType(), nullable=True),
                StructField("timezone", StringType(), nullable=True),
                StructField("precision", StringType(), nullable=True)
            ]), nullable=True)
        ]), nullable=True)
    ]), nullable=True),
    StructField("paymentToken", StringType(), nullable=True),
    StructField("channel", StringType(), nullable=True),
    StructField("postpayLink", StringType(), nullable=True),
    StructField("skuId", StringType(), nullable=True),
    StructField("currency", StringType(), nullable=True),
    StructField("launchId", StringType(), nullable=True)
])

request_body_df = df.withColumn('requestBody', from_json(col('request_body'), request_body_schema)) \
    .select(col('requestBody.*')) \

def flatten(df):
    # compute Complex Fields (Lists and Structs) in Schema
    complex_fields = dict([(field.name, field.dataType)
                           for field in df.schema.fields
                           if type(field.dataType) == ArrayType or type(field.dataType) == StructType])
    while len(complex_fields) != 0:
        col_name = list(complex_fields.keys())[0]
        print("Processing :" + col_name + " Type : " + str(type(complex_fields[col_name])))

        # if StructType then convert all sub element to columns.
        # i.e. flatten structs
        if (type(complex_fields[col_name]) == StructType):
            expanded = [col(col_name + '.' + k).alias(col_name + '_' + k) for k in
                        [n.name for n in complex_fields[col_name]]]
            print(f"------expanded:{expanded}")
            df = df.select("*", *expanded).drop(col_name)

        # if ArrayType then add the Array Elements as Rows using the explode function
        # i.e. explode Arrays
        elif (type(complex_fields[col_name]) == ArrayType):
            df = df.withColumn(col_name, explode_outer(col_name))

        # recompute remaining Complex Fields in Schema
        complex_fields = dict([(field.name, field.dataType)
                               for field in df.schema.fields
                               if type(field.dataType) == ArrayType or type(field.dataType) == StructType])
    return df


flatten_df = flatten(request_body_df)

query = flatten_df.withColumn("current_timestamp", current_timestamp()) \
    .withColumn("year", year(col("current_timestamp"))) \
    .withColumn("month", lpad(month(col("current_timestamp")), 2, "0")) \
    .withColumn("day", lpad(dayofmonth(col("current_timestamp")), 2, "0")) \
    .writeStream \
    .outputMode('append') \
    .format("csv") \
    .partitionBy("year", "month", "day") \
    .option("header", True) \
    .option("compression", "gzip") \
    .option("sep", ",") \
    .option("path", DATA_LOCATION) \
    .option("checkpointLocation", CHECKPOINT_LOCATION) \
    .start()

query.awaitTermination()

job.commit()