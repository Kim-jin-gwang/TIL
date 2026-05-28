from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg

# 세션 생성
spark = SparkSession.builder \
    .appName("DataFrameTest") \
    .getOrCreate()

# 간단한 데이터 생성
data = [
    ("Alice", "Math", 85),
    ("Bob", "Math", 90),
    ("Alice", "English", 78),
    ("Bob", "English", 83),
    ("Alice", "Science", 92),
    ("Bob", "Science", 87)
]

columns = ["name", "subject", "score"]

df = spark.createDataFrame(data, columns)

# 평균 점수 계산
avg_scores = df.groupBy("name").agg(avg("score").alias("average_score"))

avg_scores.show()

spark.stop()
