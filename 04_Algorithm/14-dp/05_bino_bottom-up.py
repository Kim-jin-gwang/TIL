def bino(n, k):
    # 배열초기화 -> (n+1) * (k+1)
    B = [[0 for _ in range(k+1)] for _ in range(n+1)]

    # 상향식으로 작은 문제부터 채워나가자
    for i in range(n + 1):
        for j in range(min(i, k) + 1):
            # 기본값
            if j == 0 or j == i:
                B[i][j] = 1
            else:
                B[i][j] = B[i-1][j-1] + B[i-1][j]
    for idx in range(n+1):
        print(B[idx])
    return B[n][k]


n = 5 
k = 2
print(bino(n, k))  # 출력: 10
