#import sys

#sys.stdin = open("input.txt", "r")

T = int(input())
for t in range(1,T+1):
    N = int(input())

    field = [list(map(int,input().strip())) for _ in range(N)]
    ans, idx = 0,0
    mid = N//2

    for i in range(N):
        tmp = field[i][mid-idx:mid+idx+1]
        ans += sum(tmp)

        if i < mid:
            idx+=1
        else:
            idx-=1

    print(f'#{t} {ans}')




