# 실습 힌트
# - 목표: map+filter, flatMap, mapPartitions 방식의 성능 차이를 비교합니다.
# - rdd 생성 시 두 번째 인자로 num_partitions를 넘겨 파티션 수를 고정하세요.
# - count()는 실제 연산을 실행시키는 액션이므로 시간 측정 대상에 포함됩니다.
# - 실행 결과 시간은 장비 상태에 따라 달라지므로 상대적인 차이를 관찰하세요.

# TODO 안내
# - 큰 숫자 RDD는 sc.parallelize에 데이터 범위와 num_partitions를 함께 넘겨 생성합니다.
# - map+filter 방식은 짝수 필터링, 2배 변환, collect 순서로 작성합니다.
# - flatMap 방식은 조건에 맞는 값만 리스트로 반환하고 collect합니다.
# - mapPartitions 방식은 transform_partition 함수를 적용하고 collect합니다.

# RDD 연산 최적화 실습 Skeleton 파일
# TODO 표시된 부분을 채운 후 PySpark 환경에서 실행하세요.
from pyspark import SparkContext
import time
sc = SparkContext("local", "RDDOptimization")

# 1. 파티션 개수 지정
num_partitions = 8

# 2. 1~1,000,000까지의 숫자 데이터를 포함하는 RDD 생성
rdd = sc.parallelize(range(1, 1000001), num_partitions)

# 3. 수행 시간 측정 함수 정의
def measure_time(fn):
    start = time.time()
    result = fn()
    end = time.time()
    return result, end - start

# 4. map+filter 연산
map_filter_result, t1 = measure_time(lambda: rdd.filter(lambda x: x % 2 == 0).map(lambda x: x * 2).collect())
print("[map + filter] 개수:", len(map_filter_result))
print("[map + filter] 샘플:", map_filter_result[:5])
print("[map + filter] 시간:", round(t1, 4), "초")

# 5. flatMap 연산
flatmap_result, t2 = measure_time(lambda: rdd.flatMap(lambda x: [x * 2] if x % 2 == 0 else []).collect())
print("[flatMap] 개수:", len(flatmap_result))
print("[flatMap] 샘플:", flatmap_result[:5])
print("[flatMap] 시간:", round(t2, 4), "초")

# 6. mapPartitions 연산
def transform_partition(iterator):
    return (x * 2 for x in iterator if x % 2 == 0)

mappart_result, t3 = measure_time(lambda: rdd.mapPartitions(transform_partition).collect())
print("[mapPartitions] 개수:", len(mappart_result))
print("[mapPartitions] 샘플:", mappart_result[:5])
print("[mapPartitions] 시간:", round(t3, 4), "초")