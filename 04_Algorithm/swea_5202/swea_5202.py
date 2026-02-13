import sys
sys.stdin = open("input.txt", "r")


T = int(input())
for t in range(1,T+1):
    N = int(input())
    truck = []
    for _ in range(N):
        s,e = map(int,input().split())
        truck.append([s,e])
    truck.sort(key=lambda x : (x[1]))

    ans = 0
    cur = 0
    for i in range(N):
        if truck[i][0] >= cur:
            ans+=1
            cur = truck[i][1]
    
    print(f'#{t} {ans}')
