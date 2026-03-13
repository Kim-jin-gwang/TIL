import numpy as np


## 1. keepdims 파라미터의 이해
arr = np.array([[1, 2, 3], [4, 5, 6]])

# keepdims=False 설정시 행의 평균 값 [2, 5] shape (2,)가 되어
# arr(2,3)과 연산 불가 (행별로 평균을 뺄 수 없음) - 브로드캐스팅 불가
mean_val = np.mean(arr, axis=1)
print("행별 평균 (차원 축소):\n", mean_val)

# keepdims=True 설정시 행의 평균 값이 [[2], [5]] shape (2, 1)이 됨
# 차원을 축소하지 않고 길이를 1로 유지하는 속성이 keepdims
mean_val = np.mean(arr, axis=1, keepdims=True)

# 2. 결과 확인
# mean_val의 shape은 (2, 1). 이제 (2, 3)인 arr에서 뺄 수 있음
normalized = arr - mean_val

print("행별 평균 (차원 유지):\n", mean_val)
print("정규화 결과:\n", normalized)


# ============================================================
# 수열 및 그리드 생성
# ============================================================

print("\n--- arange ---")
# np.arange(start, stop, step)
a = np.arange(0, 10, 2)
print(a)        # [0 2 4 6 8]

print("\n--- linspace ---")
# np.linspace(start, stop, num) : stop 포함, num개 균등 분할
b = np.linspace(0, 1, 5)
print(b)        # [0.   0.25 0.5  0.75 1.  ]

print("\n--- eye ---")
# np.eye(n) : n×n 단위행렬
c = np.eye(3)
print(c)
# [[1. 0. 0.]
#  [0. 1. 0.]
#  [0. 0. 1.]]


# ============================================================
# 차원 조작 및 구조 설계
# ============================================================

print("\n--- reshape ---")
a = np.arange(6)           # [0 1 2 3 4 5]  shape (6,)
b = a.reshape(2, 3)
print(b)
# [[0 1 2]
#  [3 4 5]]

print("\n--- expand_dims ---")
a = np.array([1, 2, 3])    # shape (3,)
b = np.expand_dims(a, axis=0)   # shape (1, 3)
c = np.expand_dims(a, axis=1)   # shape (3, 1)
print(f"원본: {a.shape}  axis=0: {b.shape}  axis=1: {c.shape}")

print("\n--- squeeze ---")
a = np.array([[[1], [2], [3]]])  # shape (1, 3, 1)
b = np.squeeze(a)                # shape (3,)
print(f"원본: {a.shape}  squeeze 후: {b.shape}")
print(b)                         # [1 2 3]

print("\n--- transpose / .T ---")
a = np.array([[1, 2, 3],
              [4, 5, 6]])   # shape (2, 3)
print(a.T)                  # shape (3, 2)
# [[1 4]
#  [2 5]
#  [3 6]]

print("\n--- stack ---")
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
print(np.stack([a, b], axis=0))   # shape (2, 3) : 행으로 쌓기
# [[1 2 3]
#  [4 5 6]]
print(np.stack([a, b], axis=1))   # shape (3, 2) : 열로 쌓기
# [[1 4]
#  [2 5]
#  [3 6]]


# ============================================================
# 조건부 선택 및 논리 연산
# ============================================================

print("\n--- where ---")
a = np.array([1, -2, 3, -4, 5])
# 조건이 True면 a, False면 0
b = np.where(a > 0, a, 0)
print(b)    # [1 0 3 0 5]

print("\n--- isin ---")
a = np.array([1, 2, 3, 4, 5])
mask = np.isin(a, [2, 4])
print(mask)     # [False  True False  True False]
print(a[mask])  # [2 4]

print("\n--- any / all ---")
a = np.array([0, 1, 2, 0])
print(np.any(a > 0))   # True  (하나라도 양수?)
print(np.all(a > 0))   # False (모두 양수?)


# ============================================================
# 기본 통계 연산
# ============================================================

a = np.array([[1, 2, 3],
              [4, 5, 6]])

print("\n--- sum ---")
print(np.sum(a))            # 21
print(np.sum(a, axis=0))    # [5 7 9]  (열 합계)
print(np.sum(a, axis=1))    # [6 15]   (행 합계)

print("\n--- mean ---")
print(np.mean(a))           # 3.5
print(np.mean(a, axis=0))   # [2.5 3.5 4.5]

print("\n--- median ---")
b = np.array([3, 1, 4, 1, 5])
print(np.median(b))         # 3.0

print("\n--- std ---")
print(np.std(a))            # 전체 표준편차
print(np.std(a, axis=0))    # 열별 표준편차

print("\n--- percentile ---")
a = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
print(np.percentile(a, 25))   # 3.25  (1사분위)
print(np.percentile(a, 50))   # 5.5   (중앙값)
print(np.percentile(a, 75))   # 7.75  (3사분위)


# ============================================================
# 특수 연산
# ============================================================

print("\n--- unique ---")
a = np.array([3, 1, 2, 1, 3, 2, 3])
print(np.unique(a))                          # [1 2 3]
vals, counts = np.unique(a, return_counts=True)
print(f"값: {vals}  빈도: {counts}")         # 값: [1 2 3]  빈도: [2 2 3]

print("\n--- argmax / argmin ---")
a = np.array([3, 1, 4, 1, 5, 9, 2, 6])
print(np.argmax(a))   # 5  (최대값 9의 인덱스)
print(np.argmin(a))   # 1  (최소값 1의 첫 인덱스)

print("\n--- argsort ---")
a = np.array([3, 1, 4, 1, 5])
idx = np.argsort(a)
print(idx)          # [1 3 0 2 4]  (오름차순 정렬 시 원본 인덱스)
print(a[idx])       # [1 1 3 4 5]  (정렬된 결과)

print("\n--- clip ---")
a = np.array([1, 5, 10, 15, 20])
b = np.clip(a, 5, 15)   # 5 미만 → 5, 15 초과 → 15
print(b)    # [ 5  5 10 15 15]
