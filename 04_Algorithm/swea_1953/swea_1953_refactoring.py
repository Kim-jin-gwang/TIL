import sys
sys.stdin = open("input.txt", "r")


from collections import deque

# 방향(인덱스 기준) : 0-상 1-하 2-좌 3-우
dx = [-1,1,0,0]
dy = [0,0,-1,1]

# 위의 상, 하, 좌, 우 와 반대방향을 나타냄
opposite = [1,0,3,2]

# 파이프 별 뚫린 방향
pipe = {
    0:[],
    1:[0,1,2,3], # 상하좌우
    2:[0,1],     # 상하
    3:[2,3],     # 좌우
    4:[0,3],     # 상우
    5:[1,3],     # 하우
    6:[1,2],     # 하좌
    7:[0,2],     # 상좌
}

T = int(input())
for t in range(1,T+1):
    N, M, R, C, L = map(int, input().split())
    maps = [list(map(int, input().split())) for _ in range(N)]
    visited = [[False] * M for _ in range(N)]
    visited[R][C] = True
    queue = deque([(R, C, 1)])  # (x, y, time)
    cnt = 1

    while queue:
        x, y, time = queue.popleft()
        if time == L:
            continue
        
        cur_type = maps[x][y]  # 현재 파이프가 어떤 타입인지 확인
        for d in pipe[cur_type]:
            nx = x+dx[d]
            ny = y+dy[d]
            if 0 <= nx < N and 0 <= ny < M and not visited[nx][ny]:
                next_type = maps[nx][ny]  # 다음 파이프의 생김새를 확인하기 위함
                # 지금 파이프가 다음 파이프로 갔다면, 다음 파이프도 지금 파이프로 갈 수 있어야 함.
                if next_type != 0 and opposite[d] in pipe[next_type]:  # 서로 파이프가 연결되어 있는지 확인
                    visited[nx][ny] = True
                    queue.append((nx,ny,time+1))
                    cnt+=1
    
    print(f'#{t} {cnt}')