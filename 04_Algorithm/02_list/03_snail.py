N = 5 
matrix = [
    [9, 20, 2, 18, 11],
    [19, 1, 25, 3, 21],
    [8, 24, 10, 17, 7],
    [15, 4, 16, 5, 6],
    [12, 13, 22, 23, 14]
]

# 2차원 배열을 1차원 리스트로 변환 후 정렬
sorted_matrix = sorted([num for row in matrix for num in row])

# 빈 5x5 결과 행렬 초기화
result = [[0] * N for _ in range(N)]

# 달팽이 방향 설정 (우 → 하 → 좌 → 상)
dxy = [[0, 1], [1, 0], [0, -1], [-1, 0]]

x, y, direction = 0, 0, 0  # 시작 위치 (0,0), 오른쪽 방향

for value in sorted_matrix:
    result[x][y] = value  # 현재 위치에 값 채우기
    nx, ny = x + dxy[direction][0], y + dxy[direction][1]  # 다음 위치

    # 범위를 벗어나거나 이미 값이 채워진 경우 방향 변경
    if not (0 <= nx < N and 0 <= ny < N and result[nx][ny] == 0):
        direction = (direction + 1) % 4  # 다음 방향으로 변경
        nx, ny = x + dxy[direction][0], y + dxy[direction][1]  # 새 위치 갱신

    x, y = nx, ny  # 위치 업데이트

# 결과 출력
for row in result:
    print(row)
