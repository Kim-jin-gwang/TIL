from pyspark.sql import SparkSession

# SparkSession 생성
spark = SparkSession.builder \
    .appName("Example") \
    .getOrCreate()

# 간단한 데이터 생성
data = [
    ("Alice", 20),
    ("Bob", 30),
    ("Cathy", 40)
]
columns = ["name", "age"]

# DataFrame 생성
df = spark.createDataFrame(data, columns)

# 결과 출력
df.show()

# Spark 종료
spark.stop()
