# Python UDF 방식과 DataFrame API 표현식 방식의 실행 계획을 비교하는 과제입니다.
# TODO에는 UDF 등록, 컬럼 추가, 필터링, 실행 계획 확인 메서드를 채워 넣습니다.
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf
from pyspark.sql.types import IntegerType

spark = (
    SparkSession.builder
    .appName("AssignmentUdfOptimization")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

data = [
    ("EMP-1001", "data_engineer", 1999, 4800000),
    ("EMP-1002", "ml_engineer", 1994, 6200000),
    ("EMP-1003", "platform_engineer", 1989, 7100000),
    ("EMP-1004", "data_analyst", 1984, 5900000),
    ("EMP-1005", "analytics_engineer", 1998, 5300000),
]
df = spark.createDataFrame(data, ["EmployeeID", "Role", "BirthYear", "MonthlySalary"])


def get_age(birth_year):
    return 2026 - birth_year


get_age_udf = udf(get_age, IntegerType())
# TODO: Python 함수를 Spark SQL UDF로 등록하는 함수

udf_df = (
    df
    .withColumn("Age", get_age_udf(col("BirthYear")))
    .filter(col("Age") >= 30)
)
# 위 TODO 순서: Age 컬럼을 추가하는 메서드, Age 조건으로 행을 거르는 메서드

print("Python UDF 결과")
udf_df.show()

print("Python UDF 실행 계획")
udf_df.explain()
# TODO: Python UDF가 실행 계획에 어떻게 나타나는지 확인하는 메서드

optimized_df = (
    df
    .withColumn("Age", 2026 - col("BirthYear"))
    .filter(col("Age") >= 30)
)

print("DataFrame API 표현식 결과")
optimized_df.show()

print("DataFrame API 표현식 실행 계획")
optimized_df.explain()
# TODO: DataFrame API 표현식의 실행 계획을 확인하는 메서드

spark.stop()
