from pyspark.sql import SparkSession
from pyspark.sql.functions import col


print("\n=== 01. Job, Stage, Task 확인 ===")
print("- 목표: Action이 Job 실행을 유발하고, shuffle 경계가 Stage를 나누며, 파티션 수가 Task 수와 연결되는 흐름을 확인합니다.")

spark = (
    SparkSession.builder
    .appName("JobStageTaskExample")
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
columns = ["order_id", "region", "order_status", "order_amount"]

df = spark.createDataFrame(data, columns).repartition(3)

print("\n1. 원본 DataFrame 생성 및 repartition(3) 적용")
print("- Spark는 지연 실행을 사용하므로 createDataFrame/repartition만으로는 아직 Job이 실행되지 않습니다.")
print("- repartition(3)은 나중에 Action이 실행될 때 데이터를 3개 파티션으로 다시 나누도록 실행 계획에 기록됩니다.")
print("- 아래 파티션 수 확인은 실습용 점검이며, DataFrame 계획을 RDD로 변환해 partition 구조를 확인합니다.")

# 파티션은 Task가 처리하는 기본 단위다.
# 다만 Stage마다 처리하는 partition 구조가 다를 수 있으므로 Task 수는 Stage별로 달라질 수 있다.
# 실행 환경의 core 수에 따라 동시에 실행되는 task 수가 달라진다.
print(f"- 현재 파티션 개수: {df.rdd.getNumPartitions()}")
print("- 하나의 Stage는 여러 Task로 나뉘어 실행됩니다.")
print("- 보통 Task 수는 해당 Stage가 처리하는 partition 수와 밀접하게 연결됩니다.")
print("- 다만 Stage마다 처리하는 partition 구조가 다를 수 있어 Task 수는 Stage별로 달라질 수 있습니다.")
print("- Spark UI의 Jobs/Stages 탭에서 각 Stage의 Task 개수와 partition 수의 관계를 확인합니다.")

# Action 함수가 실행될 때 Job이 만들어진다.
print("\n2. 첫 번째 Action 실행: df.show()")
print("- show()는 Action이므로 Spark Job 실행을 유발합니다.")
print("- 일반적으로 하나의 Action이 하나 이상의 Job으로 Spark UI에 기록될 수 있습니다.")
print("- 여기서는 Action이 실행되면 실제 계산이 시작된다는 점에 집중합니다.")
print("- 실행 과정에서 repartition(3)이 실제로 수행되고, 파티션 단위로 Task가 만들어집니다.")
df.show()

print("\n3. 두 번째 Action 실행: df.count()")
print("- 같은 DataFrame이라도 별도 Action이므로 다시 Spark Job 실행을 유발합니다.")
print("- 중간 결과를 따로 저장하지 않았기 때문에 Spark는 count()에 필요한 계산을 다시 수행합니다.")
print(f"- 전체 주문 수: {df.count()}")

# filter와 groupBy는 아직 실행되지 않고 실행 계획만 만들어지는 transformation이다.
# show/count와 달리 아래 코드는 아직 실행되지 않고 실행 계획만 만들어진다.
result_df = (
    df
    .filter(col("region").isin("Seoul", "Busan"))
    .groupBy("region")
    .count()
)

print("\n4. Transformation 정의 완료")
print("- filter는 region 조건에 맞는 row만 남기는 transformation입니다.")
print("- groupBy는 같은 region 값을 모아 count를 계산하는 transformation입니다.")
print("- 같은 region 값이 여러 partition에 흩어져 있으면 데이터를 다시 모으는 과정이 필요할 수 있습니다.")
print("- 아직 Action이 없으므로 result_df 계산은 실행되지 않았습니다.")
print("- 지금은 '어떻게 계산할지'만 result_df의 실행 계획으로 쌓인 상태입니다.")

print("\n5. 실행 계획 확인: result_df.explain()")
print("- Physical plan에서 Exchange가 보이면 shuffle 경계가 생긴 것입니다.")
print("- shuffle 경계가 Stage를 나누므로, Exchange 전후가 서로 다른 Stage가 될 수 있습니다.")
print("- Spark UI에서는 shuffle 전후로 Stage가 나뉘는지 확인합니다.")
result_df.explain()

print("\n6. 세 번째 Action 실행: result_df.show()")
print("- groupBy 결과를 출력하면서 filter/groupBy/count 계산이 실제로 수행됩니다.")
print("- Spark UI Jobs 탭에서 이 Action이 별도 Job 실행으로 기록되는지 확인합니다.")
result_df.show()
input("Spark UI 확인이 끝나면 Enter를 누르세요.")


spark.stop()
