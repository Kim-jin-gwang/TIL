N = 5
matrix = [
    [1,  2,  3,  4,  5],
    [6,  7,  8,  9, 10],
    [11, 12, 13, 14, 15],
    [16, 17, 18, 19, 20],
    [21, 22, 23, 24, 25]
]

# 주대각선 합 구하기
main_sum = 0  # 주대각선 합을 저장할 변수
for i in range(N):
    main_sum += matrix[i][i]  # 왼쪽 위 ➝ 오른쪽 아래

print("주대각선 합:", main_sum)  # 결과: 1 + 7 + 13 + 19 + 25 = 65


# 부대각선 합 구하기
sub_sum = 0  # 부대각선 합을 저장할 변수
for i in range(N):
    sub_sum += matrix[i][N - 1 - i]  # 오른쪽 위 ➝ 왼쪽 아래

print("부대각선 합:", sub_sum)  # 결과: 5 + 9 + 13 + 17 + 21 = 65


# 두 대각선의 합 구하기 (가운데 값 중복 제거)
# 주대각선과 부대각선을 더하면, 가운데 원소(matrix[2][2])가 중복 포함됨
middle = matrix[N // 2][N // 2]  # 가운데 원소 (중복 제거 필요)

result = main_sum + sub_sum - middle

print("대각선 합:", result)  # 결과: 65 + 65 - 13 = 117
