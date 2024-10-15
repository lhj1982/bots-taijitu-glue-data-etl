import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import col, from_json, explode_outer, current_timestamp, lpad, year, month, dayofmonth, \
    translate, regexp_replace
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

df = spark.readStream.format("kafka") \
    .options(**kafka_params) \
    .load() \
    .selectExpr("CAST(value AS STRING)") \
    .withColumn("value", translate(col("value"), "\n\t", "")) \
    .withColumn("value", regexp_replace(col("value"), "^\"", "")) \
    .withColumn("value", regexp_replace(col("value"), "\"$", "")) \
    .withColumn('requestBody', from_json(col('value'), request_body_schema)) \
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


flatten_df = flatten(df)

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
    .option("encoding", "UTF-8") \
    .start()

query.awaitTermination()

job.commit()