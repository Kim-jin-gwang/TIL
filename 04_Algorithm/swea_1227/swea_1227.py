import sys
sys.stdin = open("input.txt", "r")


from collections import deque

dx = [0,1,0,-1]
dy = [1,0,-1,0]

for _ in range(10):
    t = int(input())
    maze = [list(map(int,input().strip())) for _ in range(100)]

    start_x, start_y = 0,0
    for i in range(16):
        for j in range(16):
            if maze[i][j] == 2:
                start_x, start_y = i, j

    visited = [[False] * 100 for _ in range(100)]
    queue = deque([(start_x, start_y)])
    visited[start_x][start_y] = True
    ans = 0
    flag = False

    while queue:
        x, y = queue.popleft()

        for i in range(4):
            nx = dx[i] + x
            ny = dy[i] + y
            if 0<=nx<100 and 0<=ny<100:
                if maze[nx][ny] == 3:
                    ans = 1
                    flag = True
                    break

                if not visited[nx][ny] and maze[nx][ny] != 1:
                    queue.append((nx,ny))
                    visited[nx][ny] = True
        
        if flag:
            break
            
    print(f'#{t} {ans}')

