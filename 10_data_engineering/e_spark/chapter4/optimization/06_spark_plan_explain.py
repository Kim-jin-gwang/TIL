from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg


print("\n=== 06. Spark 실행 계획 explain() 읽기 ===")
print("- 목표: logical plan과 physical plan에서 filter, aggregate, sort가 어떤 연산자로 바뀌는지 확인합니다.")

spark = (
    SparkSession.builder
    .appName("SparkPlanExplain")
    .config("spark.sql.shuffle.partitions", "4")
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
df = spark.createDataFrame(data, ["order_id", "region", "order_status", "order_amount"])

print("\n1. 주문 DataFrame 생성")
print("- order_amount가 100000 이상인 주문만 남긴 뒤 region별 평균 주문 금액을 계산합니다.")
print("- 마지막에 orderBy('region')을 사용해 정렬까지 포함합니다.")
print("- 아직 Action을 실행하지 않았으므로 실제 filter/aggregate/sort는 수행되지 않았습니다.")

result_df = (
    df
    .filter(col("order_amount") >= 100000)
    .groupBy("region")
    .agg(avg("order_amount").alias("avg_order_amount"))
    .orderBy("region")
)

print("\n2. Transformation 체인 정의 완료")
print("- filter는 조건에 맞는 주문만 남기는 논리 계획으로 기록됩니다.")
print("- groupBy + avg는 region별 집계를 위한 논리 계획으로 기록됩니다.")
print("- orderBy는 최종 결과를 region 기준으로 정렬하는 계획으로 기록됩니다.")
print("- explain()은 이 계획이 Catalyst를 거치며 어떻게 바뀌는지 확인하기 위해 사용합니다.")

# explain()에서는 filter, aggregate, sort가 어떤 physical operator로 바뀌는지 확인한다.
print("\n3. 기본 실행 계획 확인: result_df.explain()")
print("- Physical plan 중심으로 출력됩니다.")
print("- Filter, HashAggregate, Exchange, Sort 같은 operator를 확인합니다.")
print("- Exchange는 groupBy 또는 orderBy 때문에 partition 간 데이터 이동이 필요하다는 뜻입니다.")
result_df.explain()

# extended=True는 parsed/analyzed/optimized/physical plan을 모두 보여준다.
print("\n4. 자세한 실행 계획 확인: result_df.explain(extended=True)")
print("- Parsed Logical Plan: 코드가 처음 해석된 형태입니다.")
print("- Analyzed Logical Plan: 컬럼과 타입 검증이 끝난 형태입니다.")
print("- Optimized Logical Plan: Catalyst가 불필요한 연산을 줄인 형태입니다.")
print("- Physical Plan: 실제 실행에 사용할 operator 계획입니다.")
print("- 즉, 사용자가 작성한 DataFrame 코드가 Spark 내부 실행 계획으로 변환되는 과정을 한 번에 봅니다.")
result_df.explain(extended=True)

print("\n5. 결과 출력")
print("- show() Action이 실행되면서 위 실행 계획이 실제 Spark Job으로 수행됩니다.")
print("- explain()은 계획 확인이고, show()가 실제 계산을 시작한다는 차이를 확인합니다.")
result_df.show()

spark.stop()
