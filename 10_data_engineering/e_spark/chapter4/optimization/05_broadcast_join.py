from pyspark.sql import SparkSession
from pyspark.sql.functions import broadcast


print("\n=== 05. Join 전략 비교: SortMergeJoin vs BroadcastHashJoin ===")
print("- 목표: 일반 join과 broadcast 힌트를 준 join의 실행 계획 차이를 비교합니다.")
print("- 강의안의 Join 전략 중 Sort Merge Join과 Broadcast Hash Join을 코드로 확인합니다.")

spark = (
    SparkSession.builder
    .appName("BroadcastJoinExample")
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

large_df = spark.createDataFrame(orders, ["order_id", "customer_id", "order_amount"])
small_df = spark.createDataFrame(customers, ["customer_id", "customer_segment", "home_region"])

print("\n1. 주문 DataFrame과 고객 DataFrame 생성")
print("- large_df: 주문 데이터처럼 상대적으로 큰 쪽이라고 가정합니다.")
print("- small_df: 고객 등급/지역 같은 작은 dimension 테이블이라고 가정합니다.")
print(f"- spark.sql.autoBroadcastJoinThreshold: {spark.conf.get('spark.sql.autoBroadcastJoinThreshold')}")
print("- 이 예제에서는 자동 broadcast를 끄고, broadcast() 힌트 효과를 명확하게 봅니다.")
print("- 따라서 첫 번째 join은 일반적인 shuffle 기반 join 전략을, 두 번째 join은 broadcast 전략을 관찰합니다.")
print("- 아직 join Action을 실행하지 않았으므로 두 DataFrame은 메모리에 결과로 합쳐진 상태가 아닙니다.")

# autoBroadcastJoinThreshold를 -1로 꺼 두었기 때문에 기본 join은 broadcast를 자동 선택하지 않는다.
# Spark는 양쪽 데이터를 join key 기준으로 shuffle하고 정렬한 뒤 병합하는 SortMergeJoin을 선택할 수 있다.
normal_join_df = large_df.join(small_df, on="customer_id", how="inner")

print("\n2. 일반 Join 정의: Sort Merge Join 관찰")
print("- 자동 broadcast를 꺼 두었으므로 Spark는 일반적인 shuffle 기반 join을 선택할 수 있습니다.")
print("- 등가 join에서 양쪽 데이터가 broadcast되지 않으면 SortMergeJoin이 자주 선택됩니다.")
print("- join도 Transformation이므로 normal_join_df에는 join 결과가 아니라 join 실행 계획만 들어 있습니다.")

print("\n3. 일반 Join 실행 계획 확인")
print("- SortMergeJoin이 보이면 양쪽 데이터를 join key 기준으로 정렬한 뒤 병합하는 전략입니다.")
print("- Exchange가 보이면 같은 customer_id가 같은 partition으로 모이도록 shuffle이 발생한 것입니다.")
print("- 즉, 일반 join은 양쪽 DataFrame의 데이터 이동 비용이 생길 수 있습니다.")
normal_join_df.explain()

print("\n4. 일반 Join 결과 출력")
print("- show() Action이 실행되면서 일반 join 계획이 실제 Spark Job으로 수행됩니다.")
normal_join_df.show()

# broadcast() 힌트를 주면 작은 테이블을 각 executor로 복사해 shuffle join을 피할 수 있다.
# 이때 Spark는 작은 테이블을 해시 테이블 형태로 준비한 뒤 BroadcastHashJoin을 사용할 수 있다.
broadcast_join_df = large_df.join(broadcast(small_df), on="customer_id", how="inner")

print("\n5. Broadcast Join 정의: Broadcast Hash Join 관찰")
print("- broadcast(small_df)는 작은 테이블을 각 executor로 복사하라는 힌트입니다.")
print("- 큰 테이블 쪽 shuffle을 줄일 수 있어 작은 dimension 테이블 join에 자주 사용합니다.")
print("- 작은 테이블은 executor 메모리에 올라가므로, 너무 큰 테이블을 broadcast하면 메모리 부담이 커질 수 있습니다.")
print("- broadcast_join_df도 아직 실행 전이며, show()가 호출될 때 실제 broadcast가 일어납니다.")

print("\n6. Broadcast Join 실행 계획 확인")
print("- BroadcastHashJoin이 보이면 작은 테이블을 해시 테이블로 만들어 join하는 전략입니다.")
print("- BroadcastExchange가 보이면 small_df를 각 executor로 전달할 broadcast 데이터로 준비하는 단계입니다.")
print("- 일반 join의 Exchange/SortMergeJoin 흐름과 비교해 shuffle 비용이 어떻게 달라지는지 봅니다.")
broadcast_join_df.explain()

print("\n7. Broadcast Join 결과 출력")
print("- show() Action으로 broadcast join을 실행합니다.")
print("- Spark UI에서 일반 join보다 shuffle read/write가 줄어드는지 비교합니다.")
broadcast_join_df.show()

spark.stop()
