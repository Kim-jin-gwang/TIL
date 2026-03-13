import numpy as np


## 1. 기본 불리언 인덱싱
arr = np.array([1, 2, 3, 4, 5])

# (1) 직접 조건식 넣기
result_a = arr[arr > 3] # [4, 5]

# (2) 마스크 변수 활용 (단계별 이해)
mask = (arr > 3)        # [False, False, False, True, True]
result_b = arr[mask]    # [4, 5]


# (3) 2차원 불리언 인덱싱
arr2d = np.array([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
])

# 방법 A: 조건 적용
# → 1차원 배열로 반환 (True 위치 요소만 추출)
result_2d_a = arr2d[arr2d > 5] # [6, 7, 8, 9]
# 방법 B: 마스크 변수 활용
mask_2d = (arr2d % 2 == 0)     # 짝수 위치만 True
result_2d_b = arr2d[mask_2d]   # [2, 4, 6, 8]


# 방법 C: 행 단위 필터링 (행 조건으로 2차원 유지)
# 첫 번째 열 값이 4 이상인 행만 선택
row_mask = arr2d[:, 0] >= 4    # [False, True, True]
result_2d_c = arr2d[row_mask]  # [[4,5,6], [7,8,9]]

# 방법 D: np.where 로 조건에 따라 값 대체
result_2d_d = np.where(arr2d > 5, arr2d, 0)
# [[0,0,0],
#  [0,0,6],
#  [7,8,9]]


## 2. 불리언 인덱싱 다중 조건 
data = np.array([15, 20, 25, 30, 35, 40])

# 조건: 20보다 크고 35보다 작은 값들만 추출
# 주의: NumPy에서는 'and' 대신 '&'를 써야 하며 각 조건은 소괄호로 감싸야 합니다.
mask = (data > 20) & (data < 35)

filtered_data = data[mask]
# 결과: [25, 30]

# 응용: 조건에 맞는 값 한꺼번에 수정하기
data[data >= 30] = -1
# 결과: [15, 20, 25, -1, -1, -1]