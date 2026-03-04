


from collections import deque

# 상하좌우
dx = [-1,1,0,0]
dy = [0,0,1,-1]

# 나이트의 이동 범위 : 1시방향부터 시계방향으로 이동
hdx = [-2,-1,1,2,2,1,-1,-2]
hdy = [1,2,2,1,-1,-2,-2,-1]

def Search():
    queue = deque([])

    # (y,x,말 사용 횟수,이동 거리)
    queue.append((0,0,0,0))
    visited[0][0][0] = True

    while queue:
        y,x,k,dist = queue.popleft()
        


    
    


K = int(input())
W,H = map(int,input().split())  # 가로 ,세로
field = [list(map(int,input().split())) for _ in range(H)]
visited = [[[False] * (K+1) for _ in range(W)] for _ in range(H)]

Search(0,0,K)
