import sys
sys.stdin = open("input.txt", "r")

T = int(input())
for t in range(1,T+1):
    N = int(input())
    arr = list(map(int,input().split()))
    dp = [1] * (N)

    for i in range(1,N):
        for j in range(i):
            if arr[i] > arr[j]:
                dp[i] = max(dp[i], dp[j]+1)
    
    print(f'#{t} {max(dp)}')