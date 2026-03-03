import sys
sys.stdin = open("input.txt", "r")



from collections import deque


dx = [1,-1,0,0]
dy = [0,0,-1,1]

def Search(a,b):
    queue = deque([])
    queue.append((a,b))

    cnt = 1

    while queue:
        x,y = queue.popleft()
        
        for i in range(4):
            nx = dx[i] + x
            ny = dy[i] + y
            if 0<=nx<N and 0<=ny<N and field[nx][ny] == field[x][y] + 1:
                queue.append((nx,ny))
                cnt += 1
    
    return cnt


T = int(input())
for t in range(1,T+1):
    N = int(input())
    field = [list(map(int,input().split())) for _ in range(N)]
    
    room, move_cnt = 10001, 0
    for i in range(N):
        for j in range(N):
            cnt = Search(i,j)
            if move_cnt < cnt:
                move_cnt = cnt
                room = field[i][j]
            elif move_cnt == cnt:
                move_cnt = cnt
                room = min(room, field[i][j])
    
    print(f'#{t} {room} {move_cnt}')