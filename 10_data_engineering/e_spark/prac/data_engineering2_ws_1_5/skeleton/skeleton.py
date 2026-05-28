# 실습 힌트
# - 목표: RDD 기본 파티션 개수를 확인하고 repartition으로 파티션 수를 바꿔 봅니다.
# - numbers는 sc.parallelize(range(1, 11)) 형태로 만들면 됩니다.
# - 파티션 수 확인은 getNumPartitions(), 데이터 확인은 collect()를 사용합니다.
# - 실행 위치는 이 파일이 있는 skeleton 디렉터리를 권장합니다.

# TODO 안내
# - SparkSession과 SparkContext 생성 코드를 완성합니다.
# - 숫자 RDD는 sc.parallelize(range(1, 11)) 형태로 생성합니다.
# - 파티션 수 확인은 getNumPartitions, 파티션 변경은 repartition을 사용합니다.

from pyspark.sql import SparkSession

# SparkSession 생성
spark = SparkSession.builder.appName("PartitionApp").getOrCreate()
sc = spark.sparkContext

# 1. 1~10까지의 숫자 데이터 생성
numbers = sc.parallelize(range(1,11))

# 기본 파티션 개수 확인
default_partitions = numbers.getNumPartitions()
print(f"기본 파티션 개수: {default_partitions}")

# 파티션 개수를 1개로 변경
repartitioned_data = numbers.repartition(1)
print(f"1개로 변경된 파티션 개수: {repartitioned_data.getNumPartitions()}")

# 2. 기존  결과 스트림 출력 메서드 호출
numbers.foreach(lambda x: print(x))

# 파티션 1개로 변경된 결과 스트림 출력 메서드 호출
repartitioned_data.foreach(lambda x: print(x))