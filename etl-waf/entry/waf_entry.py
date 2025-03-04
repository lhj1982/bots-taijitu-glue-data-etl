import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import col, from_json, explode_outer, lpad, year, month, dayofmonth, \
    translate, regexp_extract
from pyspark.sql.types import StringType, StructType, StructField, ArrayType, DoubleType


args = getResolvedOptions(sys.argv, ["KAFKA_BOOTSTRAP_SERVERS",
                                     "KAFKA_USERNAME",
                                     "KAFKA_PASSWORD",
                                     "KAFKA_SSL_TRUSTSTORE_LOCATION",
                                     "KAFKA_SSL_TRUSTSTORE_PASSWORD",
                                     "KAFKA_SUBSCRIBE",
                                     "DATA_LOCATION",
                                     "CHECKPOINT_LOCATION"])
print(args)

sc = SparkContext.getOrCreate()

glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init("waf_entry", args)


KAFKA_USERNAME = args['KAFKA_USERNAME']
KAFKA_PASSWORD = args['KAFKA_PASSWORD']

KAFKA_BOOTSTRAP_SERVERS = args['KAFKA_BOOTSTRAP_SERVERS']
KAFKA_SASL_JAAS_CONFIG = f'org.apache.kafka.common.security.plain.PlainLoginModule required username="{KAFKA_USERNAME}" password="{KAFKA_PASSWORD}";'
KAFKA_SSL_TRUSTSTORE_LOCATION = args['KAFKA_SSL_TRUSTSTORE_LOCATION']
KAFKA_SSL_TRUSTSTORE_PASSWORD = args['KAFKA_SSL_TRUSTSTORE_PASSWORD']
KAFKA_SUBSCRIBE = args['KAFKA_SUBSCRIBE']
DATA_LOCATION = args['DATA_LOCATION']
CHECKPOINT_LOCATION = args['CHECKPOINT_LOCATION']

kafka_params = {
    "kafka.bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS,
    "kafka.security.protocol": "SASL_SSL",
    "kafka.sasl.mechanism": "PLAIN",
    "kafka.sasl.jaas.config": KAFKA_SASL_JAAS_CONFIG,
    "kafka.ssl.truststore.location": KAFKA_SSL_TRUSTSTORE_LOCATION,
    "kafka.ssl.truststore.password": KAFKA_SSL_TRUSTSTORE_PASSWORD,
    "kafka.ssl.endpoint.identification.algorithm": "",
    "subscribe": KAFKA_SUBSCRIBE,
    "group.id": "waf_entry",
    "startingoffsets": "latest"
}

request_body_schema = StructType([
    StructField("launchId", StringType(), nullable=True),
    StructField("skuId", StringType(), nullable=True),
    StructField("locale", StringType(), nullable=True),
    StructField("shipping", StructType([
        StructField("recipient", StructType([
            StructField("firstName", StringType(), nullable=True),
            StructField("altFirstName", StringType(), nullable=True),
            StructField("lastName", StringType(), nullable=True),
            StructField("altLastName", StringType(), nullable=True),
            StructField("middleName", StringType(), nullable=True),
            StructField("phoneNumber", StringType(), nullable=True),
            StructField("email", StringType(), nullable=True)
        ]), nullable=True),
        StructField("address", StructType([
            StructField("address1", StringType(), nullable=True),
            StructField("address2", StringType(), nullable=True),
            StructField("address3", StringType(), nullable=True),
            StructField("city", StringType(), nullable=True),
            StructField("state", StringType(), nullable=True),
            StructField("postalCode", StringType(), nullable=True),
            StructField("country", StringType(), nullable=True),
            StructField("county", StringType(), nullable=True)
        ]), nullable=True),
        StructField("getBy", StructType([
            StructField("minDate", StructType([
                StructField("dateTime", StringType(), nullable=True),
                StructField("timezone", StringType(), nullable=True),
                StructField("precision", StringType(), nullable=True)
            ]), nullable=True),
            StructField("maxDate", StructType([
                StructField("dateTime", StringType(), nullable=True),
                StructField("timezone", StringType(), nullable=True),
                StructField("precision", StringType(), nullable=True)
            ]), nullable=True)
        ]), nullable=True),
        StructField("fulfillmentAnnotation", StringType(), nullable=True)
    ]), nullable=True),
    StructField("totals", StructType([
        StructField("items", StructType([
            StructField("total", DoubleType(), nullable=True),
            StructField("details", StructType([
                StructField("price", DoubleType(), nullable=True),
                StructField("discount", DoubleType(), nullable=True)
            ]), nullable=True)
        ]), nullable=True),
        StructField("valueAddedServices", StructType([
            StructField("total", DoubleType(), nullable=True),
            StructField("details", StructType([
                StructField("price", DoubleType(), nullable=True),
                StructField("discount", DoubleType(), nullable=True)
            ]), nullable=True)
        ]), nullable=True),
        StructField("taxes", StructType([
            StructField("total", DoubleType(), nullable=True),
            StructField("details", StructType([
                StructField("items", StructType([
                    StructField("tax", DoubleType(), nullable=True),
                    StructField("type", StringType(), nullable=True)
                ]), nullable=True),
                StructField("shipping", StructType([
                    StructField("tax", DoubleType(), nullable=True),
                    StructField("type", StringType(), nullable=True)
                ]), nullable=True),
                StructField("valueAddedServices", StructType([
                    StructField("tax", DoubleType(), nullable=True),
                    StructField("type", StringType(), nullable=True)
                ]), nullable=True),
            ]), nullable=True),
        ]), nullable=True),
        StructField("fulfillment", StructType([
            StructField("total", DoubleType(), nullable=True),
            StructField("details", StructType([
                StructField("price", DoubleType(), nullable=True),
                StructField("discount", DoubleType(), nullable=True)
            ]), nullable=True)
        ]), nullable=True)
    ]), nullable=True),
    StructField("currency", StringType(), nullable=True),
    StructField("paymentToken", StringType(), nullable=True),
    StructField("channel", StringType(), nullable=True),
    StructField("checkoutId", StringType(), nullable=True),
    StructField("deviceId", StringType(), nullable=True),
    StructField("previousEntryId", StringType(), nullable=True),
    StructField("offerId", StringType(), nullable=True),
    StructField("postpayLink", StringType(), nullable=True),
    StructField("invoiceInfo", ArrayType(StructType([
        StructField("type", StringType(), nullable=True),
        StructField("detail", StringType(), nullable=True),
        StructField("taxId", StringType(), nullable=True)
    ])), nullable=True),
    StructField("storeId", StringType(), nullable=True),
    StructField("retailPickupId", StringType(), nullable=True),
    StructField("geolocation", StructType([
        StructField("latitude", DoubleType(), nullable=True),
        StructField("longitude", DoubleType(), nullable=True)
    ]), nullable=True),
    StructField("retailPickupPerson", StructType([
        StructField("givenName", StringType(), nullable=True),
        StructField("familyName", StringType(), nullable=True)
    ]), nullable=True)
])

wxbb_info_tbl_schema = StructType([
    StructField("umid", StringType(), nullable=True)
])

request_header_schema = StructType([
    StructField("x-nike-upmid", StringType(), nullable=True),
])

# the format of message form kafka: request_path(path), request_method(method), request_body(json)...
df = spark.readStream.format("kafka") \
    .options(**kafka_params) \
    .load() \
    .selectExpr("CAST(value AS STRING)") \
    .withColumn("value", translate(col("value"), "\n\t", "")) \
    .withColumn("host", regexp_extract(col("value"), r"host\((.*?)\)", 1)) \
    .withColumn("http_user_agent", regexp_extract(col("value"), r"http_user_agent\((.*?)\)", 1)) \
    .withColumn("https", regexp_extract(col("value"), r"https\((.*?)\)", 1)) \
    .withColumn("http_cookie", regexp_extract(col("value"), r"http_cookie\((.*?)\)", 1)) \
    .withColumn("real_client_ip", regexp_extract(col("value"), r"real_client_ip\((.*?)\)", 1)) \
    .withColumn("status", regexp_extract(col("value"), r"status\((.*?)\)", 1)) \
    .withColumn("request_method", regexp_extract(col("value"), r"request_method\((.*?)\)", 1)) \
    .withColumn("request_body", regexp_extract(col("value"), r"request_body\((.*?)\)", 1)) \
    .withColumn("request_path", regexp_extract(col("value"), r"request_path\((.*?)\)", 1)) \
    .withColumn("request_traceid", regexp_extract(col("value"), r"request_traceid\((.*?)\)", 1)) \
    .withColumn("time", regexp_extract(col("value"), r"time\((.*?)\)", 1)) \
    .withColumn("user_id", regexp_extract(col("value"), r"user_id\((.*?)\)", 1)) \
    .withColumn("wxbb_info_tbl", regexp_extract(col("value"), r"wxbb_info_tbl\((.*?)\)", 1)) \
    .withColumn("request_header", regexp_extract(col("value"), r"request_header\((.*?)\)", 1)) \
    .drop(col("value")) \
    .where((col("request_path").like("/launch/entries%")) & (col("request_method") == "POST")) \
    .withColumn('requestBody', from_json(col('request_body'), request_body_schema)) \
    .withColumn('wxbbInfoTbl', from_json(col('wxbb_info_tbl'), wxbb_info_tbl_schema)) \
    .withColumn('requestHeader', from_json(col('request_header'), request_header_schema)) \
    .select(col("requestBody.*"), col("wxbbInfoTbl.*"), col("requestHeader.*"),
            col("host"), col("http_user_agent"), col("https"), col("http_cookie"), col("real_client_ip"), col("status"),
            col("request_method"), col("request_path"), col("request_traceid"), col("time"), col("user_id"),
            col("request_body"), col("wxbb_info_tbl"), col("request_header")) \

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


flatten_df = flatten(df)

query = flatten_df.withColumn("year", year(col("time"))) \
    .withColumn("month", lpad(month(col("time")), 2, "0")) \
    .withColumn("day", lpad(dayofmonth(col("time")), 2, "0")) \
    .writeStream \
    .outputMode('append') \
    .format("csv") \
    .partitionBy("year", "month", "day") \
    .option("header", True) \
    .option("compression", "gzip") \
    .option("sep", ",") \
    .option("path", DATA_LOCATION) \
    .option("checkpointLocation", CHECKPOINT_LOCATION) \
    .option("encoding", "UTF-8") \
    .start()

query.awaitTermination()

job.commit()