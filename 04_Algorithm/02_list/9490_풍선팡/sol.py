import sys
sys.stdin = open('input.txt')


dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]

T = int(input())

for tc in range(1, T + 1):
    # 가로 N, 세로 M
    N, M = map(int, input().split())
    # 각 정수 데이터
    data = [list(map(int, input().split())) for _ in range(N)]

    # 최종 결괏값
    result = 0  # 충분히 작은 값
    # 모든 지점에 대해 조회
    for x in range(N):
        for y in range(M):
            # 현재 위치 점수로 우선 초기화
            temp = data[x][y]
            '''
                내 현재 위치의 점수가 1이라면 1칸만큼 추가 이동 가능
                즉, 상하좌우로 1만큼 점수 추가 range(1, 2)
                
                내 현재 위치의 점수가 2라면 2칸만큼 추가 이동 가능
                즉, 상하좌우 각각 2번 이동하여 점수 추가 range(1, 3)
            '''
            for mul in range(1, data[x][y]+1):
                for k in range(4):  # 상하좌우 내 방향에 대한 K
                    '''
                        dx[k], dx[y] 는 0 or 1 or -1
                        좌로 1칸 이동 -> [x + 0 * 1] [y - 1 * 1]
                        좌로 2칸 이동 -> [x + 0 * 2] [y - 1 * 2]
                        좌로 3칸 이동 -> [x + 0 * 3] [y - 1 * 3]
                        
                        이동 하려는 칸 수만큼 곱하여 처리 
                    '''
                    nx = x + dx[k] * mul # 새로운 x
                    ny = y + dy[k] * mul  # 새로운 Y

                    # 새로운 좌표가 범위 (0보다 크거나 갖고 N/M보다 작은) 네거티브 인덱싱 주의 (-1 이 되어도 오류가 나지않음)
                    if 0 <= nx < N and 0 <= ny <M:
                        temp += data[nx][ny]    # 이번 위치를 임시 값에 추가
            # 4방향에 대한 조사를 마치면, 최댓값 갱신
            if result < temp:
                result = temp

    print(f'#{tc} {result}')