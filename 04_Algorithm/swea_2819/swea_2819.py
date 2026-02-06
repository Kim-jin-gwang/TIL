import sys
sys.stdin = open("input.txt", "r")

dx = [0,1,0,-1]
dy = [1,0,-1,0]

def dfs(x,y,num_str):
    if len(num_str) == 7:
        ans.add(num_str)
        return

    for i in range(4):
        nx = x+dx[i]
        ny = y+dy[i]
        if 0<=nx<4 and 0<=ny<4:
            dfs(nx,ny,num_str+field[nx][ny])


T = int(input())
for t in range(1,T+1):
    ans = set()
    field = [input().split() for _ in range(4)]

    for i in range(4):
        for j in range(4):
            dfs(i,j,field[i][j])

    print(f'#{t} {len(ans)}')


