#import sys

#sys.stdin = open("input.txt", "r")


T = int(input())
for t in range(1,T+1):
    N,M = map(int,input().split())
    arr = [list(map(int,input().split())) for _ in range(N)]
    dx = [1,0,-1,0]
    dy = [0,1,0,-1]

    ans = 0
    for x in range(N):
        for y in range(M):
           tmp = arr[x][y]
           for cnt in range(arr[x][y]):
               for i in range(4):
                   if dx[i] == 1:
                       nx = x + dx[i] + cnt
                   elif dx[i] == -1:
                       nx = x + dx[i] - cnt
                   else:
                       nx = x + dx[i]

                   if dy[i] == 1:
                       ny = y + dy[i] + cnt
                   elif dy[i] == -1:
                       ny = y + dy[i] - cnt
                   else:
                       ny = y + dy[i]

                   if 0<=nx<N and 0<=ny<M:
                       tmp += arr[nx][ny]

           ans = max(ans,tmp)

    print(f'#{t} {ans}')
