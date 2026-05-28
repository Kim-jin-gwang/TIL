from pyspark.sql import SparkSession


# SparkSession 생성
spark = (
    SparkSession.builder
    .appName("TextFileExample")
    .getOrCreate()
)

# SparkContext 가져오기
sc = spark.sparkContext

# 로그 출력 줄이기
sc.setLogLevel("WARN")

# 파일 읽기
# test.txt 파일은 이 파이썬 파일을 실행하는 위치에 있어야 합니다.
rdd = sc.textFile("test.txt")

# 파티션 개수 확인
print("파티션 개수:", rdd.getNumPartitions())

# 파티션 개수를 1개로 변경
rdd_single = rdd.repartition(1)
print("변경된 파티션 개수:", rdd_single.getNumPartitions())

# collect() — 전체 데이터 조회
print("전체 데이터:")
print(rdd.collect())

# count() — 줄 개수 확인
print("줄 개수:", rdd.count())

# filter() — 특정 조건을 만족하는 데이터만 추출
filtered = rdd.filter(lambda line: "Spark" in line)
print("'Spark'가 포함된 줄:")
print(filtered.collect())

# map() — 각 줄을 소문자로 변환
lower = rdd.map(lambda line: line.lower())
print("소문자로 변환된 데이터:")
print(lower.collect())

# SparkSession 종료
spark.stop()