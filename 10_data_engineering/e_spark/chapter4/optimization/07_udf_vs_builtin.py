from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf
from pyspark.sql.types import IntegerType


print("\n=== 07. Python UDF와 Built-in Expression 비교 ===")
print("- 목표: 같은 계산을 Python UDF와 Spark 내장 표현식으로 작성했을 때 실행 계획이 어떻게 다른지 확인합니다.")

spark = (
    SparkSession.builder
    .appName("UdfVsBuiltin")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

data = [
    ("EMP-1001", "data_engineer", 1999),
    ("EMP-1002", "ml_engineer", 1994),
    ("EMP-1003", "platform_engineer", 1989),
]
df = spark.createDataFrame(data, ["employee_id", "role", "birth_year"])

print("\n1. 직원 DataFrame 생성")
print("- birth_year로 age를 계산하는 단순 예제를 사용합니다.")
print("- 단순 산술/문자열/날짜 처리는 가능하면 Spark built-in 함수나 DataFrame 표현식을 사용합니다.")
print("- 아직 Action을 실행하지 않았으므로 age 컬럼 계산은 수행되지 않았습니다.")


def get_age(birth_year):
    return 2026 - birth_year


get_age_udf = udf(get_age, IntegerType())

# Python UDF는 JVM과 Python worker 사이의 변환 비용이 생길 수 있다.
udf_df = df.withColumn("age", get_age_udf(col("birth_year")))

print("\n2. Python UDF 방식 정의")
print("- Python 함수 get_age를 udf()로 감싸서 Spark 컬럼 계산에 사용합니다.")
print("- Spark가 함수 내부 로직을 자세히 이해하기 어렵고, Python worker와의 직렬화 비용이 생길 수 있습니다.")
print("- udf_df는 결과가 아니라 '각 row의 birth_year를 Python 함수로 넘겨 age를 만든다'는 계획입니다.")

print("\n3. Python UDF 실행 계획 확인")
print("- BatchEvalPython 또는 PythonUDF 관련 operator가 보이면 Python UDF 경로를 탄 것입니다.")
print("- 이 operator는 JVM 기반 Spark 실행 흐름에서 Python 실행 환경으로 데이터를 넘기는 구간을 의미합니다.")
udf_df.explain()

print("\n4. Python UDF 결과 출력")
print("- show() Action이 실행되면서 Python UDF 계산이 실제로 수행됩니다.")
udf_df.show()

# 단순 계산은 DataFrame API나 SQL 표현식으로 대체하는 편이 좋다.
# Spark가 표현식을 이해할 수 있어 Catalyst 최적화 대상이 된다.
builtin_df = df.withColumn("age", 2026 - col("birth_year"))

print("\n5. Built-in Expression 방식 정의")
print("- 2026 - col('birth_year')는 Spark가 이해할 수 있는 컬럼 표현식입니다.")
print("- Catalyst 최적화 대상이 되며 Python UDF보다 실행 경로가 단순합니다.")
print("- builtin_df도 아직 실행 전이며, Python 함수 호출 없이 Spark 표현식으로만 계획이 만들어진 상태입니다.")

print("\n6. Built-in Expression 실행 계획 확인")
print("- Project 안에 산술 표현식이 직접 들어가고 BatchEvalPython이 없어야 합니다.")
print("- Spark가 계산식을 직접 이해하므로 코드 생성과 최적화가 적용되기 쉽습니다.")
builtin_df.explain()

print("\n7. Built-in Expression 결과 출력")
print("- show() Action으로 built-in 표현식 계산을 실행합니다.")
print("- 두 결과는 같지만 실행 계획이 더 단순한 쪽이 일반적으로 최적화에 유리합니다.")
builtin_df.show()

spark.stop()
