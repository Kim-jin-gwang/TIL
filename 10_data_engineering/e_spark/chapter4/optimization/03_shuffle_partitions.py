from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count


print("\n=== 03. spark.sql.shuffle.partitions 확인 ===")
print("- 목표: shuffle 이후 만들어지는 파티션 수가 spark.sql.shuffle.partitions 설정의 영향을 받는지 확인합니다.")

spark = (
    SparkSession.builder
    .appName("ShufflePartitions")
    .config("spark.sql.adaptive.enabled", "false")
    .config("spark.sql.shuffle.partitions", "4")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

campaigns = ["brand_search", "retargeting", "newsletter", "affiliate", "app_push"]
data = [
    (campaigns[i % len(campaigns)], 35 + (i * 17) % 420)
    for i in range(100)
]
df = spark.createDataFrame(data, ["campaign", "session_seconds"]).repartition(2)

print("\n1. 원본 DataFrame 생성")
print("- 아래 파티션 수 확인은 실습용 점검이며, repartition(2) 이후 구조를 확인하기 위한 값입니다.")
print(f"- shuffle 전 파티션 개수: {df.rdd.getNumPartitions()}")
print(f"- spark.sql.shuffle.partitions 설정값: {spark.conf.get('spark.sql.shuffle.partitions')}")
print("- 현재 예제는 shuffle 결과 파티션 수가 4가 되도록 설정했습니다.")
print("- 설정값이 그대로 보이도록 실행 중 partition 수 자동 조정은 꺼 두었습니다.")
print("- 자동 조정 기능의 자세한 의미는 뒤의 08번 예제에서 따로 다룹니다.")
print("- repartition(2)로 입력 파티션을 2개로 맞춰 두고, groupBy 이후 파티션 수가 어떻게 달라지는지 봅니다.")

# groupBy 이후 만들어지는 shuffle 결과 파티션 개수는 spark.sql.shuffle.partitions의 영향을 받는다.
grouped_df = (
    df
    .filter(col("session_seconds") >= 120)
    .groupBy("campaign")
    .agg(count("*").alias("cnt"))
)

print("\n2. filter + groupBy Transformation 정의")
print("- filter는 narrow transformation이라 shuffle을 만들지 않습니다.")
print("- groupBy는 campaign별 데이터를 모으기 위해 shuffle을 만듭니다.")
print("- 이 시점에는 아직 Action이 없어 실제 계산은 수행되지 않았습니다.")
print("- grouped_df에는 '120초 이상 세션만 남기고 campaign별 count를 계산한다'는 계획만 저장되어 있습니다.")

print("\n3. groupBy 이후 DataFrame 파티션 개수 확인")
print("- grouped_df.rdd.getNumPartitions()는 실행 계획을 RDD로 변환하며 파티션 수를 확인합니다.")
print("- 이 확인은 학습을 위한 점검 코드이며, 실제 결과 출력은 뒤의 show() Action에서 수행합니다.")
print("- 이 값은 groupBy로 생기는 shuffle 결과가 몇 개 partition으로 나뉘는지 보여줍니다.")
print("- 자동 조정을 꺼 두었기 때문에 여기서는 spark.sql.shuffle.partitions 값인 4가 그대로 보여야 합니다.")
print(f"- groupBy 이후 파티션 개수: {grouped_df.rdd.getNumPartitions()}")

print("\n4. 실행 계획 확인")
print("- Exchange hashpartitioning(..., 4)가 보이면 shuffle partition 설정이 적용된 것입니다.")
print("- 4는 spark.sql.shuffle.partitions 설정값에서 온 숫자입니다.")
print("- 너무 큰 값은 작은 데이터에서 불필요한 Task를 많이 만들고, 너무 작은 값은 한 Task가 처리할 데이터가 커질 수 있습니다.")
grouped_df.explain()

print("\n5. 집계 결과 출력")
print("- show() Action으로 실제 집계 결과를 계산합니다.")
print("- Spark UI Stages 탭에서 shuffle 이후 Task 수가 설정값 4와 어떻게 연결되는지 확인합니다.")
print("- 자동 조정을 꺼 두었으므로 이 예제에서는 shuffle 이후 Task 수가 설정값과 대체로 직접 대응됩니다.")
grouped_df.show()

spark.stop()
