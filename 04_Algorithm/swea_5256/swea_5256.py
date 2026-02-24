import sys
sys.stdin = open("input.txt", "r")

def MakePascal():
    dp = [[0]*(n+1) for _ in range(n+1)]
    for i in range(n+1):
        for j in range(i+1):
            if j == 0 or j == i:
                dp[i][j] = 1
            else:
                dp[i][j] = dp[i-1][j-1] + dp[i-1][j]
    
    return dp


T = int(input())
for t in range(1,T+1):
    n, a, b = map(int,input().split())
    dp = MakePascal()
    print(f'#{t} {dp[-1][b]}')
