# DataFrame VS Spark SQL 성능 비교 실습
# 아래의 빈칸(____)을 채운 후 PySpark 환경에서 실행하세요.
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import time
spark = SparkSession.builder.appName("DataFrameVsSQL").getOrCreate()

# 1. CSV 파일 로딩
df = spark.read.option("header", True).option("inferSchema", True).csv("../data/people.csv")

# 2. DataFrame API 방식
start_df = time.time()
count_df = df.filter(col("Age") >= 30).count()
end_df = time.time()
elapsed_df = end_df - start_df

print(f"DataFrame API 방식 - 30세 이상 인원 수: {count_df}")
print(f"DataFrame API 처리 시간: {elapsed_df:.6f}초")

# 3. Spark SQL 방식
df.createOrReplaceTempView("people") # 뷰 등록

start_sql = time.time()
count_sql = spark.sql("SELECT COUNT(*) FROM people WHERE Age >= 30").collect()[0][0]
end_sql = time.time()
elapsed_sql = end_sql - start_sql

print(f"Spark SQL 방식 - 30세 이상 인원 수: {count_sql}")
print(f"Spark SQL 처리 시간: {elapsed_sql:.6f}초")

# 4. 성능 비교
if elapsed_df < elapsed_sql:
    print("DataFrame API 방식이 더 빠릅니다.")
elif elapsed_sql < elapsed_df:
    print("Spark SQL 방식이 더 빠릅니다.")
else:
    print("두 방식의 성능이 거의 동일합니다.")
