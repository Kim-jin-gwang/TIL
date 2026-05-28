# Narrow Transform과 Wide Transform의 실행 계획 차이를 비교하는 실습입니다.
# TODO에는 row 단위 변환과 shuffle이 필요한 집계 연산을 구성하는 메서드를 채워 넣습니다.
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = (
    SparkSession.builder
    .appName("PracticeNarrowWide")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

data = [
    ("organic_search", 18500),
    ("paid_search", 92000),
    ("app_push", 38000),
    ("email_campaign", 126000),
    ("paid_search", 74000),
    ("app_push", 41000),
]
df = spark.createDataFrame(data, ["Channel", "Revenue"]).repartition(3)

print("원본 파티션 개수:", df.rdd.getNumPartitions())

narrow_df = (
    df
    .filter(col("Revenue") >= 40000)
    .withColumn("Revenue_With_Fee", col("Revenue") + 1000)
)
# 위 TODO 순서: 조건에 맞는 행만 남기는 메서드, 새 컬럼을 추가하는 메서드

print("Narrow Transform 결과")
narrow_df.show()

print("Narrow Transform 실행 계획")
narrow_df.explain()
# TODO: 실행 계획을 출력하는 메서드

wide_df = (
    df
    .groupBy("Channel")
    .sum("Revenue")
)
# 위 TODO 순서: Channel별로 데이터를 묶는 메서드, Revenue 합계를 구하는 집계 메서드

print("Wide Transform 결과")
wide_df.show()

print("Wide Transform 실행 계획")
wide_df.explain()
# TODO: 실행 계획을 출력하는 메서드

spark.stop()
