# 실습 힌트
# - 목표: sample, takeSample, randomSplit으로 RDD 샘플링과 데이터 분할을 연습합니다.
# - RDD 생성은 sc.parallelize, sample은 withReplacement 여부와 fraction을 인자로 받습니다.
# - randomSplit은 가중치 리스트를 넘기며, 결과는 여러 RDD로 나뉩니다.
# - 샘플링 결과는 실행마다 달라질 수 있으므로 개수와 개념을 중심으로 확인하세요.

# TODO 안내
# - 숫자 RDD는 sc.parallelize로 생성합니다.
# - 확률 샘플링은 sample을 사용하고 복원 여부와 fraction을 인자로 넘깁니다.
# - 분할된 RDD와 샘플 RDD의 크기는 count 액션으로 확인합니다.

#  RDD 샘플링 및 분할 실습 Skeleton 파일
# TODO 표시된 부분을 채운 후 PySpark 환경에서 실행하세요.
from pyspark import SparkContext
sc = SparkContext("local", "SamplingSplitApp")

# 1. 1~100까지 숫자 데이터를 RDD로 생성
numbers_rdd = sc.parallelize(range(1, 101))
print(f"원본 데이터 개수: {numbers_rdd.count()}")

# 2. sample() 비복원 방식으로 20% 샘플링
sample_without = numbers_rdd.sample(False, 0.2)
print("비복원 샘플링 결과:", sample_without.collect())

# sample() 복원 방식으로 20% 샘플링
sample_with = numbers_rdd.sample(True, 0.2)
print("복원 샘플링 결과:", sample_with.collect())

# takeSample() 비복원
take_sample_without = numbers_rdd.takeSample(False, 5)
print("takeSample 비복원:", take_sample_without)

# takeSample() 복원
take_sample_with = numbers_rdd.takeSample(True, 5)
print("takeSample 복원:", take_sample_with)

# 3. randomSplit()으로 훈련/테스트 분할
train_rdd, test_rdd = numbers_rdd.randomSplit([0.8, 0.2], seed=42)
print(f"훈련 데이터 개수: {train_rdd.count()}")
print(f"테스트 데이터 개수: {test_rdd.count()}")

# 4. 비교 분석
print(f"비복원 샘플 개수: {sample_without.count()}")
print(f"복원 샘플 개수: {sample_with.count()}")
