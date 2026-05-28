from pyspark.sql import SparkSession
from pyspark.sql.functions import count


print("\n=== 08. AQE(Adaptive Query Execution) 설정 확인 ===")
print("- 목표: AQE 설정을 켠 상태에서 shuffle 집계를 실행하고, 실행 계획에서 adaptive plan을 확인합니다.")

spark = (
    SparkSession.builder
    .appName("AdaptiveQueryExecution")
    .config("spark.sql.adaptive.enabled", "true")
    .config("spark.sql.shuffle.partitions", "20")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

print("\n1. AQE 관련 설정 확인")
print(f"- spark.sql.adaptive.enabled: {spark.conf.get('spark.sql.adaptive.enabled')}")
print(f"- spark.sql.shuffle.partitions: {spark.conf.get('spark.sql.shuffle.partitions')}")
print("- shuffle partition을 20으로 크게 잡아두고, AQE가 실행 중 통계로 조정할 여지를 만듭니다.")
print("- AQE는 계획을 처음부터 고정하지 않고, Action 실행 중 얻은 통계를 보고 일부 계획을 조정합니다.")

# AQE는 실행 중 수집한 통계로 shuffle partition 병합, join 전략 변경 등을 시도한다.
event_types = ["view_item", "add_to_cart", "checkout_completed"]
data = [
    (
        event_types[i % len(event_types)],
        1,
    )
    for i in range(1000)
]
df = spark.createDataFrame(data, ["event_type", "event_count"]).repartition(4)

print("\n2. 이벤트 DataFrame 생성")
print("- 아래 파티션 수 확인은 실습용 점검이며, repartition(4) 이후 입력 구조를 확인하기 위한 값입니다.")
print(f"- 입력 DataFrame 파티션 개수: {df.rdd.getNumPartitions()}")
print("- event_type별 count 집계를 수행해 shuffle을 발생시킵니다.")
print("- 아직 collect() 같은 결과 확인 Action을 실행하지 않았으므로 groupBy 결과 계산과 AQE 런타임 통계 수집은 시작되지 않았습니다.")

result_df = (
    df
    .groupBy("event_type")
    .agg(count("*").alias("cnt"))
)

print("\n3. AQE 적용 대상 집계 정의")
print("- groupBy는 shuffle을 만들며 AQE가 shuffle partition 병합 등을 적용할 수 있는 대표 상황입니다.")
print("- 아직 Action이 없으므로 실제 실행 통계는 수집되지 않았습니다.")
print("- result_df에는 event_type별 count를 계산한다는 계획만 들어 있습니다.")

print("\n4. Action 전 실행 계획 확인")
print("- AdaptiveSparkPlan이 보이면 AQE가 활성화된 쿼리 계획입니다.")
print("- 이 시점의 계획은 실행 전 계획이므로 final plan이 아닐 수 있습니다.")
result_df.explain()

print("\n5. 집계 결과 수집")
print("- collect() Action이 실행되면서 AQE가 런타임 통계를 수집하고 계획을 조정할 수 있습니다.")
print("- shuffle 결과가 작다고 판단되면 여러 shuffle partition을 합쳐 더 적은 Task로 처리할 수 있습니다.")
result_rows = result_df.collect()

print("- 집계 결과:")
for row in result_rows:
    print(f"  event_type={row['event_type']}, cnt={row['cnt']}")

print("\n6. Action 후 실행 계획 재확인")
print("- explain()은 환경에 따라 Action 후에도 실행 전 계획처럼 보일 수 있습니다.")
print("- 여기서는 PySpark의 JVM queryExecution API로 실제 실행된 final plan을 직접 출력합니다.")
print("- isFinalPlan=true 또는 AQEShuffleRead coalesced가 보이면 AQE가 런타임 계획을 만든 것입니다.")
print("- Initial Plan과 Final Plan을 비교하면 실행 중 계획이 어떻게 조정됐는지 확인할 수 있습니다.")
print("- Spark UI의 SQL 탭에서 Adaptive Query Execution 적용 여부를 확인합니다.")
print("- Stages 탭에서는 shuffle 이후 Task 수가 처음 설정한 20개보다 줄어들었는지 확인합니다.")
print(result_df._jdf.queryExecution().executedPlan().toString())

spark.stop()
