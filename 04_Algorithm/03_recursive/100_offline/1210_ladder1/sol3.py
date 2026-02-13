import sys
sys.stdin = open('input.txt')

# 좌, 우, 상: 아래에서 올라가도 좌우가 먼저다.
dx = [0, 0, -1]
dy = [-1, 1, 0]
def search(x, y):
    # 최상위에 도달했다면
    if x == 0:
        return y    # y 좌표반환
    else:   # 아니면 조사
        for k in range(3):
            nx = x + dx[k]
            ny = y + dy[k]
            # 3 방향이 이동 가능한 지점이라면
            if 0 <= nx < 100 and 0 <= ny < 100 and data[nx][ny] == 1:
                # 해당 지점을 방문 처리하고
                data[nx][ny] = 0
                # 다음 조사 시작
                return search(nx, ny)   # 최종 지점에 도달해 얻은 y 반환


for _ in range(10):
    tc = int(input())
    data = [list(map(int, input().split())) for _ in range(100)]

    '''
        코드가 복잡하고, 종료조건을 구하기가 어렵다.
        함수로 변경하도록 한다면?
        
        문제의 최종 목표는 사실, 도착지점인 2에 도달할 수 있는 시작좌표 1개를 구하는 것
        그렇다면, 도착지점인 2는 한 곳만 도달 할 수 있는데
        굳이 모든 상황을 다 조사해야 할까? 도착지점에서 거슬러 올라가면?
        그럼...? 중복되는 길을 또 가는 경우를 볼 이유도 없고
        방문 여부를 표시할 이유도 없고,
        시작 지점이 어딘지 계산할 필요도...? 없다
        그럼...
    '''
    # 초기값을 -1로 잡는 이유: 0이 정답일 수 있으므로
    result = -1
    # 도착 지점을 찾아서 조사 시작
    for y in range(100):
        if data[99][y] == 2:
            # 시작 지점 방문 처리하고
            data[99][y] = 0
            # 조사하여 찾아낸 좌표를 result에 할당하고
            result = search(99, y)
        # 정해졌으면 조사 종료
        if result >= 0:
            print(f'#{tc} {result}')
            break
