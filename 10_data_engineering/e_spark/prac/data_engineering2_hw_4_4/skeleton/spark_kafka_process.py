# Kafka topic에서 JSON 메시지를 읽고 Spark Structured Streaming으로 window count를 수행하는 과제입니다.
# 빈칸에는 Kafka source 옵션, JSON 파싱 컬럼, watermark/window, foreachBatch 출력을 채워 넣습니다.
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, window
from pyspark.sql.types import StructType, StructField, TimestampType, StringType, IntegerType


spark = (
    SparkSession.builder
    .appName("AssignmentKafkaStreaming")
    .config("spark.sql.shuffle.partitions", "4")
    .config(
        "spark.jars.packages",
        "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.4"
    )
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

df = (
    spark
    .readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "localhost:9092")
    .option("subscribe", "user_events")
    .option("startingOffsets", "earliest")
    .option("maxOffsetsPerTrigger", "10")
    .load()
)
# 위 빈칸 순서: 스트리밍 입력 속성, Kafka source 이름, 구독할 topic 이름, 처음 읽을 offset 기준, trigger당 최대 offset 수

value_df = df.selectExpr("CAST(value AS STRING) AS value")
# 빈칸: Kafka value는 bytes이므로 문자열로 변환하는 SQL 표현식

schema = StructType([
    StructField("id", IntegerType(), True),
    StructField("timestamp", TimestampType(), True),
    StructField("message", StringType(), True)
])

parsed_df = (
    value_df
    .select(from_json(col("value"), schema).alias("data"))
    .select("data.*")
)
# 위 빈칸 순서: JSON 문자열이 들어 있는 컬럼명, data 구조체 내부 컬럼을 펼치는 표현식

result_df = (
    parsed_df
    .withWatermark("timestamp", "1 minute")
    .groupBy(window("timestamp", "1 minute"))
    .count()
)
# 위 빈칸 순서: 이벤트 시간 컬럼명, window 기준 시간 컬럼명, window별 행 개수를 세는 메서드

def print_batch(batch_df, batch_id):
    print(f"batch_id={batch_id}")
    batch_df.orderBy("window").show(truncate=False)
    print("window row count:", batch_df.count())


query = (
    result_df
    .writeStream
    .outputMode("complete")
    .foreachBatch(print_batch)
    .start()
)
# 위 빈칸 순서: 스트리밍 출력을 만드는 속성, 집계 결과 전체를 출력하는 output mode, micro-batch마다 호출할 함수

query.awaitTermination()
