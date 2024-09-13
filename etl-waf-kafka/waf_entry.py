from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, regexp_extract, col
from pyspark.sql.types import StructType, StructField, StringType
from pyspark import SparkFiles

print("test deploy")

spark = SparkSession.builder.appName("taijituTest").getOrCreate()

kafka_params = {
    "kafka.bootstrap.servers": "alikafka-post-cn-9t93w71ti003-1.alikafka.aliyuncs.com:9093,alikafka-post-cn-9t93w71ti003-2.alikafka.aliyuncs.com:9093,alikafka-post-cn-9t93w71ti003-3.alikafka.aliyuncs.com:9093",
    "kafka.security.protocol": "SASL_SSL",
    "kafka.sasl.mechanism": "PLAIN",
    "kafka.sasl.jaas.config": 'org.apache.kafka.common.security.plain.PlainLoginModule required username="test1234" password="Test1234";',
    "kafka.ssl.truststore.location": '/tmp/mix.4096.client.truststore.jks',
    "kafka.ssl.truststore.password": "KafkaOnsClient",
    "kafka.ssl.endpoint.identification.algorithm": "",
    "kafka.group.id": "test",
    "subscribe": "test",
    "startingoffsets": "latest"
}

df = spark.readStream.format("kafka") \
    .options(**kafka_params) \
    .load() \
    .selectExpr("CAST(value AS STRING)") \
    .select(from_json("value", schema).alias("data")) \
    .select("data.*")

body_schema = spark.read.json(df.rdd.map(lambda row: row.request_body)).schema
tbl_schema = spark.read.json(df.rdd.map(lambda row: row.wxbb_info_tbl)).schema

json_df = df.withColumn('wxbbInfoTbl', from_json(col('wxbb_info_tbl'), tbl_schema)) \
    .withColumn('requestBody', from_json(col('request_body'), body_schema)) \
    .drop('request_body', 'wxbb_info_tbl') \
 \
    request_body_df = json_df.select(col('requestBody'))


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

data_location = 's3://nike-commerce-test-app-internal/testKafka/dataDir'

checkpoint_location = 's3://nike-commerce-test-app-internal/testKafka/checkPointDir'

query = flatten_df.withColumn("dataDate", to_date(current_timestamp(), "yyyy-MM-dd")) \
    .coalesce(1).writeStream \
    .outputMode("append") \
    .format("csv") \
    .option("header", "true") \
    .option("mapreduce.fileoutputcommitter.marksuccessfuljobs", "false") \
    .option("sep", ",") \
    .option("path", data_location) \
    .option("checkpointLocation", checkpoint_location) \
    .start()

query.awaitTermination()