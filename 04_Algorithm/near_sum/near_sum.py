

T = int(input())

for t in range(1,T+1):
    N = int(input()) #5
    arr = [list(map(int,input().split())) for _ in range(N)]
    ans = 0

    dx = [0,1,-1,0]
    dy = [1,0,0,-1]

    for x in range(N):
        for y in range(N):
            sum = 0
            for i in range(4):
                nx = x+dx[i]
                ny = y+dy[i]

                if 0<=nx<N and 0<=ny<N:
                   sum += abs(arr[nx][ny] - arr[x][y])
            ans += sum

    print(f'#{t} {ans}')

