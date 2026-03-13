import re
import numpy as np

# 1. 원본 비정형 데이터
raw_data = """
    sensor_1: 23.5 unit, 
    sensor_2: 12.1 unit, 
    sensor_3: 45.8 unit,
    sensor_4: error,
    sensor_5: 33.2 unit
"""

# 2. Regex 패턴 정의
# 숫자인 것(\d+), 소수점이 있을 수도 있는 것(\.?), 다시 숫자인 것(\d*)
pattern = re.compile(r"(\d+\.?\d*) unit")

# 3. 데이터 추출
# findall을 통해 'unit' 앞의 숫자만 리스트로 반환
extracted_values = pattern.findall(raw_data)

result = re.search(pattern, raw_data)
print(result.group())  # '23.5 unit'
print(result.group(1))  # '23.5'

print(f"추출된 텍스트 리스트: {extracted_values}")  # ['23.5', '12.1', '45.8', '33.2']

# 4. NumPy로의 전환
# 리스트 형태의 문자열을 NumPy의 float64 타입 배열로 변환
np_array = np.array(extracted_values, dtype=np.float64)

print(f"NumPy 배열 결과: {np_array}")   # [23.5 12.1 45.8 33.2]
print(f"평균값 계산: {np_array.mean()}")    # 28.650000000000002