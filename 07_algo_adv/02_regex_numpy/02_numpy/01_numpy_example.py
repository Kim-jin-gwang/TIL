import numpy as np
import time

# 1,000,000개의 데이터 생성
size = 1_000_000    # 언더스코어 구분자 (가독성을 위한 것 python 3.6+)
python_list = list(range(size))
numpy_array = np.arange(size)

# 1. Python 리스트 연산 시간 측정
start_time = time.perf_counter()
list_result = [i * 2 for i in python_list]
list_sum = sum(list_result)
print(f"Python List 소요 시간: {time.perf_counter() - start_time:.5f}초")

# 2. NumPy 배열 연산 시간 측정
start_time = time.perf_counter()
# 벡터 연산: for문 없이 수학식처럼 작성
array_result = numpy_array * 2
array_sum = array_result.sum()
print(f"NumPy Array 소요 시간: {time.perf_counter() - start_time:.5f}초")