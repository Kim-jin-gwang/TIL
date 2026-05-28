# 일반 Join과 Broadcast Join, AQE 설정을 실행 계획으로 비교하는 실습입니다.
# TODO에는 Join 메서드, broadcast 힌트 함수, 실행 계획 확인 메서드를 채워 넣습니다.
from pyspark.sql import SparkSession
from pyspark.sql.functions import broadcast

spark = (
    SparkSession.builder
    .appName("PracticeJoinPlanAqe")
    .config("spark.sql.shuffle.partitions", "8")
    .config("spark.sql.adaptive.enabled", "true")
    .config("spark.sql.autoBroadcastJoinThreshold", "-1")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

orders = [
    ("ORD-1001", "C-204", 129000),
    ("ORD-1002", "C-118", 83000),
    ("ORD-1003", "C-204", 214000),
    ("ORD-1004", "C-331", 57000),
    ("ORD-1005", "C-118", 176000),
]
customers = [
    ("C-118", "loyal", "Busan"),
    ("C-204", "premium", "Seoul"),
    ("C-331", "new", "Daejeon"),
]

large_df = spark.createDataFrame(orders, ["OrderID", "CustomerID", "OrderAmount"])
small_df = spark.createDataFrame(customers, ["CustomerID", "CustomerSegment", "HomeRegion"])

print("AQE 설정:", spark.conf.get("spark.sql.adaptive.enabled"))
print("shuffle partition 설정:", spark.conf.get("spark.sql.shuffle.partitions"))
# TODO: Spark 설정 값을 읽는 메서드

normal_join_df = large_df.join(small_df, on="CustomerID", how="inner")
# TODO: 두 DataFrame을 CustomerID 기준으로 결합하는 메서드

print("일반 Join 결과")
normal_join_df.show()

print("일반 Join 실행 계획")
normal_join_df.explain(extended=True)
# TODO: 일반 Join의 Logical/Physical Plan을 출력하는 메서드

broadcast_join_df = large_df.join(broadcast(small_df), on="CustomerID", how="inner")
# TODO: 작은 DataFrame을 executor에 복사해서 Join하도록 알려주는 함수

print("Broadcast Join 결과")
broadcast_join_df.show()

print("Broadcast Join 실행 계획")
broadcast_join_df.explain(extended=True)
# TODO: Broadcast Join의 Logical/Physical Plan을 출력하는 메서드

spark.stop()
