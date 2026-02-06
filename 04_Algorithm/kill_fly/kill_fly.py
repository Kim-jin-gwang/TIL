#import sys

#sys.stdin = open("input.txt", "r")


T = int(input())
for t in range(1,T+1):
    N,M = map(int,input().split())
    arr = [list(map(int,input().split())) for _ in range(N)]
    ans = 0

    for x in range(N-M+1):
        for y in range(N-M+1):
            tmp = 0
            for i in range(M):
                for j in range(M):
                    tmp += arr[i+x][j+y]
            ans = max(ans,tmp)

    print(f'#{t} {ans}')

