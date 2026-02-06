

T = int(input())
for t in range(1,T+1):
    N = int(input())  #5
    arr = [list(map(int,input().split())) for _ in range(N)]
    ans = 0

    for i in range(N):
        for j in range(N):
            if i==j:
                ans += arr[i][j]

            elif (N-1-i) == j:
                ans += arr[i][j]

    print(f'#{t} {ans}')
