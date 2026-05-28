from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, count
import time


print("\n=== 04. persist/cache로 반복 계산 줄이기 ===")
print("- 목표: cache()가 언제 실제로 저장되는지, 이후 Action이 캐시를 재사용하는지 확인합니다.")

spark = (
    SparkSession.builder
    .appName("PersistCacheExample")
    .config("spark.sql.shuffle.partitions", "4")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")


# 주문 데이터 생성
# region과 order_status가 반복되도록 구성하여 집계 결과를 확인하기 쉽게 만듭니다.
regions = ["Seoul", "Busan", "Daegu", "Daejeon"]
statuses = ["delivered", "delivered", "returned", "cancelled"]

data = [
    (
        f"ORD-{202605180000 + i}",
        regions[i % len(regions)],
        statuses[i % len(statuses)],
        30000 + (i * 7300) % 240000,
    )
    for i in range(1000)
]

df = spark.createDataFrame(
    data,
    ["order_id", "region", "order_status", "order_amount"]
)

print("1. 원본 DataFrame 생성 완료")
print("- 아직 Action을 실행하지 않았으므로 실제 Spark Job은 실행되지 않았습니다.")
print("- 아래 transformation들은 이 원본 DataFrame에서 출발해 실행 계획으로만 연결됩니다.")


# filter, groupBy, agg는 Transformation입니다.
# 이 시점에는 실제 계산이 수행되지 않고, 실행 계획만 만들어집니다.
aggregated_df = (
    df
    .filter(col("order_status") == "delivered")
    .groupBy("region")
    .agg(
        avg("order_amount").alias("avg_order_amount"),
        count("*").alias("cnt")
    )
)

print("\n2. Transformation 정의 완료")
print("- delivered 주문만 남긴 뒤, region별 평균 주문 금액과 주문 건수를 계산하도록 정의했습니다.")
print("- 아직 count(), show() 같은 Action이 없으므로 실제 계산은 수행되지 않았습니다.")


print("\n3. cache() 호출 전 상태")
print(f"- aggregated_df.is_cached: {aggregated_df.is_cached}")
print("- False라면 아직 캐시 대상으로 등록되지 않은 상태입니다.")


# cache()는 즉시 데이터를 저장하지 않습니다.
# 첫 번째 Action이 실행될 때 실제 계산 결과가 캐시에 저장됩니다.
aggregated_df.cache()

print("\n4. cache() 호출 후 상태")
print(f"- aggregated_df.is_cached: {aggregated_df.is_cached}")
print(f"- Storage Level: {aggregated_df.storageLevel}")
print("- True라면 캐시 대상으로 등록된 상태입니다.")
print("- 단, 아직 실제 데이터가 캐시에 저장된 것은 아니며 첫 번째 Action에서 캐시가 만들어집니다.")


print("\n5. 첫 번째 Action 실행: aggregated_df.count()")
print("- 이때 filter/groupBy/agg 계산이 실제로 수행됩니다.")
print("- 계산된 aggregated_df 결과가 캐시에 저장됩니다.")

row_count = aggregated_df.count()

print(f"- aggregated_df 결과 row 수: {row_count}")
print("- 현재 결과는 region별 집계 결과이므로 row 수는 집계된 region 개수입니다.")


print("\n6. 첫 번째 Action 이후 실행 계획 확인")
print("- InMemoryRelation 또는 InMemoryTableScan이 보이면 캐시가 적용된 것입니다.")
print("- InMemoryRelation: 캐시 저장 대상으로 관리되는 데이터")
print("- InMemoryTableScan: 캐시에 저장된 데이터를 읽는 작업")
print("- 실행 계획 안쪽에 Scan, Filter, Exchange가 보여도 원래 캐시를 만들기 위한 계산 흐름으로 보면 됩니다.")

aggregated_df.explain()


print("\n7. 두 번째 Action 실행: aggregated_df.show()")
print("- 앞에서 만든 캐시를 재사용할 수 있습니다.")
print("- 원본 데이터부터 다시 filter/groupBy/agg를 반복하는 것이 아니라 캐시된 집계 결과를 읽습니다.")

aggregated_df.show()


print("\n8. 두 번째 Action 이후 실행 계획 확인")
print("- 여기서도 InMemoryTableScan이 보이면 캐시된 데이터를 읽고 있다는 의미입니다.")

aggregated_df.explain()


print("\n9. Spark UI Storage 탭 확인")
print("- 브라우저에서 http://localhost:4040 접속 후 Storage 탭을 확인합니다.")
print("- Storage Level: 캐시 저장 방식")
print("- Cached Partitions: 전체 파티션 중 캐시된 파티션 수")
print("- Fraction Cached: 전체 데이터 중 캐시된 비율")
print("- Size in Memory: 메모리에 저장된 캐시 크기")
print("- Size on Disk: 디스크에 저장된 캐시 크기")
print("- Storage 탭에 항목이 보이면 실제 캐시가 만들어진 상태입니다.")

print("\nSpark UI 확인을 위해 100초 동안 대기합니다.")
time.sleep(100)


print("\n10. 캐시 해제: aggregated_df.unpersist()")
print("- 더 이상 반복해서 사용하지 않는 DataFrame은 캐시를 해제하는 것이 좋습니다.")

aggregated_df.unpersist()

print(f"- unpersist 이후 aggregated_df.is_cached: {aggregated_df.is_cached}")
print("- False라면 캐시 대상 등록이 해제된 상태입니다.")

spark.stop()
