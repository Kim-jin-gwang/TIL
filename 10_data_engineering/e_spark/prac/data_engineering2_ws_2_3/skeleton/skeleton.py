# 실습 힌트
# - 목표: RDD를 텍스트 파일로 저장하고 다시 불러오는 흐름을 확인합니다.
# - 저장은 saveAsTextFile, 로드는 sc.textFile을 사용합니다.
# - Spark는 output 디렉터리가 이미 있으면 저장에 실패하므로 재실행 전 output을 삭제해야 합니다.
# - 실행 위치는 이 파일이 있는 skeleton 디렉터리를 권장합니다.

# TODO 안내
# - 숫자 RDD는 sc.parallelize로 생성합니다.
# - RDD 내용 확인은 collect를 사용합니다.
# - 저장은 saveAsTextFile, 다시 읽기는 sc.textFile을 사용합니다.
# - 재실행 시 기존 output 디렉터리를 먼저 삭제해야 합니다.

# Apache Spark RDD 저장 및 불러오기 실습 Skeleton 파일
# TODO 표시된 부분을 채운 후 PySpark 환경에서 실행하세요.

from pyspark.sql import SparkSession

# 1. SparkSession 생성
spark = SparkSession.builder.appName("SaveLoadRDD").getOrCreate()
sc = spark.sparkContext

# 2. 숫자 데이터(1~10)를 RDD로 변환
numbers_rdd = sc.parallelize(range(1, 11))

# 데이터 확인
print(numbers_rdd.collect())

# 3. 저장 전 하나의 파티션으로 압축 (순서 보장)
# 재실행할 때 output 디렉터리가 이미 있으면 Spark가 실패하므로 먼저 삭제하세요.
numbers_rdd.coalesce(1).saveAsTextFile("output")

# 저장된 텍스트 파일을 불러와서 확인
loaded_text_rdd = sc.textFile("output")
print(loaded_text_rdd.collect())
