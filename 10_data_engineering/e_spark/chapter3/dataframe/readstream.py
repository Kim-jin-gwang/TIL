from pyspark.sql import SparkSession

spark = SparkSession \
    .builder \
    .appName("read_stream_example") \
    .getOrCreate()

order_schema = """
    order_id STRING,
    customer_id STRING,
    order_date STRING,
    order_amount DOUBLE,
    payment_method STRING,
    category STRING
"""

stream_order_df = (spark.readStream
    .format("csv")
    .option("header", True)
    .schema(order_schema) 
     # data/stream 디렉터리에 새 CSV 파일이 추가되면 스트리밍 입력 대상으로 처리 가능
    .load("data/stream")
)

query = (
    stream_order_df.writeStream
    .format("console")
    .outputMode("append")
    .option("truncate", False)
    .start()
)

query.awaitTermination()
