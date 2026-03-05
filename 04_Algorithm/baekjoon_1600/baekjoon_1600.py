

from collections import deque

# 상하좌우
dx = [-1,1,0,0]
dy = [0,0,1,-1]

# 나이트의 이동 범위 : 1시방향부터 시계방향으로 이동
hdx = [-2,-1,1,2,2,1,-1,-2]
hdy = [1,2,2,1,-1,-2,-2,-1]

def Search():
    queue = deque([])

    # (y, x, 말 사용 횟수(K), 이동 거리 = 실제 정답)
    # 말 사용 횟수가 K와 같으면 상하좌우 탐색하기
    queue.append((0,0,0,0))
    visited[0][0][0] = True

    while queue:
        x,y,k,dist = queue.popleft()

        if x == H-1 and y == W-1:  # 도착지를 찾으면 리턴
            return dist
        
        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]
            if 0<=nx<H and 0<=ny<W:
                if not visited[nx][ny][k] and field[nx][ny] != 1:
                        visited[nx][ny][k] = True
                        queue.append((nx,ny,k,dist+1))
            
            if k<K:
                for i in range(8):
                    nx = x + hdx[i]
                    ny = y + hdy[i]
                    if 0<=nx<H and 0<=ny<W:
                         if not visited[nx][ny][k+1] and field[nx][ny] != 1:
                            visited[nx][ny][k+1] = True
                            queue.append((nx,ny,k+1,dist+1))
    
    return -1
        

K = int(input())
W,H = map(int,input().split())  # 가로 ,세로
field = [list(map(int,input().split())) for _ in range(H)]

# 말 이동을 쓴 횟수에 따라 방문 기록을 다르게 하기 위해 K배열을 하나 더 만듬
visited = [[[False] * (K+1) for _ in range(W)] for _ in range(H)] # 3차원 (가로, 세로, K사용 횟수)

ans = Search()
print(ans)