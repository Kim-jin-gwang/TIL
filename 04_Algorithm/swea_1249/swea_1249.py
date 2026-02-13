import sys
sys.stdin = open("input.txt", "r")

from collections import deque


dx = [1,0,-1,0]
dy = [0,1,0,-1]
    
T = int(input())
for t in range(1,T+1):
    N = int(input())
    field = [list(map(int,input().strip())) for _ in range(N)]
    visited = [[-1]*N for _ in range(N)]

    queue = deque([(0,0)])
    visited[0][0] = 0

    while queue:
        x,y = queue.popleft()
        
        for i in range(4):
            nx = x+dx[i]
            ny = y+dy[i]
            if 0<=nx<N and 0<=ny<N:
                check_cost = visited[x][y] + field[nx][ny]
                if visited[nx][ny] == -1 or check_cost < visited[nx][ny]:
                    visited[nx][ny] = check_cost
                    queue.append((nx,ny))
    
    ans = visited[N-1][N-1]
    print(f'#{t} {ans}')