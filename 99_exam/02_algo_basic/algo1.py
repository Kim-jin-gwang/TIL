import sys
sys.stdin = open('algo1_sample_in.txt')


dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]

def saerch(x, y):
    # 후보군에 값 삽입
    stack = [(x, y)]
    data[x][y] = 1  # 해당 위치 방문 표시
    count = 1       # 구조 가능 구역 1로 초기화
    while stack:
        x, y = stack.pop()  # 조사
        for k in range(4):  # 4방향에 대해
            nx = x + dx[k]
            ny = y + dy[k]

            # 범위 체크, 이동 가능 구역 체크
            if 0 <= nx < M and 0 <= ny < N and data[nx][ny] == 0:
                # 해당 위치 조사처리
                data[nx][ny] = 1
                stack.append((nx, ny))
                count += 1  # 총 구조 가능 구역 횟수 1 증가
    return count


T = int(input())

for tc in range(1, T+1):
    # 가로, 세로
    N, M = map(int, input().split())
    # 길 0, 벽 1
    data = [list(map(int, input().split())) for _ in range(M)]

    # 보호 가능 구역
    area = []
    # 모든 구역에 대해
    for x in range(M):
        for y in range(N):
            # 건설 가능 구역이면
            if data[x][y] == 0:
                # 조사 시작 후, 결과를 추가
                area.append(saerch(x, y))
    # 내림차순 정렬 후
    area.sort(reverse=True)
    # 가장 큰 2개의 값 더하기
    print(f'#{tc} {area[0] + area[1]}')