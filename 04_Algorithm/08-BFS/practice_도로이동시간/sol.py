import sys
sys.stdin = open('input.txt')


dx = [0,1,0,-1]
dy = [1,0,-1,0]


def search(x,y):
    queue = [(x,y,0)]
    data[x][y] = 0

    while queue:
        x,y,dist = queue.pop(0)

        for k in range(4):
            nx = x+dx[k]
            ny = y+dy[k]

            if 0 <= nx < N and 0 <= ny < M and data[nx][ny]:
                queue.append((nx,ny,dist+1))
                data[nx][ny] = 0
                if nx == N-1 and ny == M-1:
                    return dist + 1



N,M = map(int,input().split())
data = [list(map(int,input())) for _ in range(N)]

ans = search(0,0)
print(ans)