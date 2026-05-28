# Spark Action이 Job을 만들고, 집계 연산이 Stage/Task 흐름에 어떤 영향을 주는지 확인하는 실습입니다.
# TODO에는 DataFrame 생성, Action, Transform, 실행 계획 확인에 필요한 메서드를 채워 넣습니다.
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = (
    SparkSession.builder
    .appName("PracticeJobStageTask")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

data = [
    ("ORD-20260511-001", "Seoul", "delivered", 129000),
    ("ORD-20260511-002", "Busan", "delivered", 83000),
    ("ORD-20260511-003", "Seoul", "cancelled", 42000),
    ("ORD-20260511-004", "Daegu", "delivered", 158000),
    ("ORD-20260511-005", "Busan", "returned", 57000),
    ("ORD-20260511-006", "Seoul", "delivered", 214000),
]
columns = ["OrderID", "Region", "OrderStatus", "OrderAmount"]

df = spark.createDataFrame(data, columns).repartition(3)
# 첫 번째 TODO: SparkSession에서 리스트 데이터를 DataFrame으로 만드는 메서드
# 두 번째 TODO: 파티션 수를 3개로 다시 나누는 메서드

print("파티션 개수:", df.rdd.getNumPartitions())
# TODO: 현재 RDD의 파티션 개수를 확인하는 메서드

print("첫 번째 Action: show()")
df.show()
# TODO: DataFrame 내용을 화면에 출력하는 Action

print("두 번째 Action: count()")
print(df.count())
# TODO: 전체 행 개수를 계산하는 Action

result_df = (
    df
    .filter(col("Region").isin("Seoul", "Busan"))
    .groupBy("Region")
    .count()
)
# 위 TODO 순서: 조건으로 행을 거르는 Transform, 지역별로 묶는 Transform, 그룹별 행 개수를 세는 집계

print("filter + groupBy 실행 계획")
result_df.explain()
# TODO: Spark가 어떤 물리 실행 계획을 세웠는지 출력하는 메서드

print("집계 결과")
result_df.show()

spark.stop()
