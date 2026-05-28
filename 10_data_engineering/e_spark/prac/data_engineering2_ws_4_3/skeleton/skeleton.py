# shuffle partition 설정과 cache 사용이 반복 Action에 어떤 의미를 갖는지 확인하는 실습입니다.
# TODO에는 설정 조회, 필터링, 집계, 캐시 관련 메서드를 채워 넣습니다.
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count

spark = (
    SparkSession.builder
    .appName("PracticeShuffleCache")
    .config("spark.sql.shuffle.partitions", "4")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

campaigns = ["brand_search", "retargeting", "newsletter", "affiliate", "app_push"]
data = [
    (campaigns[i % len(campaigns)], 35 + (i * 17) % 420)
    for i in range(100)
]
df = spark.createDataFrame(data, ["Campaign", "SessionSeconds"]).repartition(2)

print("shuffle 전 파티션 개수:", df.rdd.getNumPartitions())
print("shuffle partition 설정:", spark.conf.get("spark.sql.shuffle.partitions"))
# TODO: Spark 설정 값을 읽는 메서드

grouped_df = (
    df
    .filter(col("SessionSeconds") >= 120)
    .groupBy("Campaign")
    .agg(count("*").alias("Cnt"))
)
# 위 TODO 순서: 조건 필터 메서드, 그룹화 메서드, 행 개수를 세는 집계 함수

grouped_df.cache()
# TODO: 이후 Action에서 재사용할 수 있도록 DataFrame을 메모리에 보관하는 메서드

print("첫 번째 Action")
print(grouped_df.count())

print("두 번째 Action")
grouped_df.show()

print("실행 계획")
grouped_df.explain()
# TODO: 실행 계획을 출력하는 메서드

grouped_df.unpersist()
# TODO: cache/persist로 보관한 데이터를 해제하는 메서드

spark.stop()
