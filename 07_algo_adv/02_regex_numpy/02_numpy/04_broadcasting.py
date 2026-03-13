import numpy as np

prices = np.array([1000, 2000, 3000])
tax_rate = 1.1

# 1. 기본 for 루프 방식
taxed_prices_list = []
for p in prices:
    taxed_prices_list.append(p * tax_rate)

# 2. 벡터화 연산
taxed_prices_arr = prices * tax_rate

# 3. 스칼라 브로드캐스팅
A = np.array([1, 2, 3])
print(A + 10)           # [11 12 13]


# 4. 3차원 + 2차원 브로드캐스팅
A = np.ones((2, 3, 4))   # shape (2, 3, 4)
B = np.ones((3, 4))  # shape (3, 4)

print(f"A.shape: {A.shape}")  # (2, 3, 4)
print(f"B.shape: {B.shape}")  # (3, 4)
# 브로드캐스팅 연산 진행
C = A + B
print(C)


# 5. 열벡터 + 행벡터 → 2차원 결과
col = np.array([[1], [2], [3]])  # shape (3, 1)
row = np.array([10, 20, 30])     # shape (3,)

print(col + row)
# [[11 21 31]
#  [12 22 32]
#  [13 23 33]]
