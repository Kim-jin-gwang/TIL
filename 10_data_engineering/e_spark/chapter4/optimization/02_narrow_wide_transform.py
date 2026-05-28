from pyspark.sql import SparkSession
from pyspark.sql.functions import col


print("\n=== 02. Narrow Transformation과 Wide Transformation ===")
print("- 목표: shuffle 없이 이어지는 연산과 shuffle을 만드는 연산의 차이를 실행 계획에서 확인합니다.")

spark = (
    SparkSession.builder
    .appName("NarrowWideTransform")
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

df = spark.createDataFrame(data, ["channel", "revenue"]).repartition(3)

print("\n1. 원본 DataFrame 생성")
print("- 아래 파티션 수 확인은 실습용 점검이며, 이후 transformation들이 어떤 partition 구조에서 출발하는지 보기 위한 값입니다.")
print(f"- 원본 파티션 개수: {df.rdd.getNumPartitions()}")
print("- 이후 실행 계획에서 파티션 간 데이터 이동 여부를 비교합니다.")
print("- 아직 show(), count() 같은 결과 확인 Action을 실행하지 않았으므로 narrow/wide transformation의 결과 계산은 시작되지 않았습니다.")

# filter와 withColumn은 각 파티션 안에서 처리할 수 있는 narrow transform이다.
# 부모 파티션의 데이터가 다른 파티션으로 이동하지 않으므로 shuffle이 생기지 않는다.
narrow_df = (
    df
    .filter(col("revenue") >= 40000)
    .withColumn("revenue_with_fee", col("revenue") + 1000)
)

print("\n2. Narrow Transformation 정의")
print("- filter: 조건에 맞는 row만 각 파티션 내부에서 남깁니다.")
print("- withColumn: 각 row의 revenue 값으로 새 컬럼을 계산합니다.")
print("- 두 연산 모두 다른 파티션의 데이터가 필요하지 않으므로 shuffle이 없어야 합니다.")
print("- 현재 narrow_df는 실제 결과가 아니라, 나중에 실행할 계산 절차를 담은 DataFrame입니다.")

print("\n3. Narrow Transformation 실행 계획 확인")
print("- Exchange가 없다면 shuffle 없이 처리되는 계획입니다.")
print("- 단, 처음 df를 만들 때 사용한 repartition(3)은 데이터 재분배이므로 계획에 Exchange로 보일 수 있습니다.")
print("- 여기서 핵심은 filter/withColumn 자체가 새로운 shuffle 경계를 만들지 않는다는 점입니다.")
narrow_df.explain()

print("\n4. Narrow Transformation 결과 출력")
print("- show() Action이 실행되면서 위 transformation들이 실제로 계산됩니다.")
print("- Spark는 각 파티션에서 filter와 컬럼 계산을 이어서 처리할 수 있습니다.")
narrow_df.show()

# groupBy는 같은 key를 모으기 위해 shuffle이 필요한 wide transform이다.
# 여러 파티션에 흩어진 같은 channel 값을 한곳으로 모아야 하므로 Exchange가 나타난다.
wide_df = (
    df
    .groupBy("channel")
    .sum("revenue")
)

print("\n5. Wide Transformation 정의")
print("- groupBy('channel')은 같은 channel 값을 한 파티션 쪽으로 모아야 합니다.")
print("- 이 데이터 이동이 shuffle이며 실행 계획에서는 Exchange로 나타납니다.")
print("- Exchange는 비용이 큰 연산일 수 있지만, groupBy, join, orderBy처럼 데이터 재배치가 필요한 작업에서는 자연스럽게 발생합니다.")
print("- 중요한 것은 Exchange를 무조건 없애는 것이 아니라, 불필요한 shuffle을 줄이고 적절한 partition 수로 조정하는 것입니다.")
print("- wide_df도 아직 계산된 결과가 아니라 groupBy 집계 계획만 가진 상태입니다.")

print("\n6. Wide Transformation 실행 계획 확인")
print("- HashAggregate 앞뒤에 Exchange가 있는지 확인합니다.")
print("- Exchange 이후에는 같은 channel 값들이 같은 partition으로 모인 뒤 최종 합계가 계산됩니다.")
wide_df.explain()

print("\n7. Wide Transformation 결과 출력")
print("- groupBy 집계를 실제로 실행합니다.")
print("- Spark UI Stages 탭에서 shuffle read/write가 생기는지 narrow 예제와 비교합니다.")
wide_df.show()

spark.stop()
