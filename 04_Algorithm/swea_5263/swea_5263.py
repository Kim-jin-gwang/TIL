import sys
sys.stdin = open("input.txt", "r")
INF = int(1e9)

import heapq

def LowerCost(dist):
    res = -INF
    for k in range(N):
        for i in range(N):
            for j in range(N):
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    
    for i in range(N):
        for j in range(N):
            if i!=j and dist[i][j] != INF:
                res = max(res, dist[i][j])
    
    return res



T = int(input())
for t in range(1,T+1):
    N = int(input())
    graph = [list(map(int,input().split())) for _ in range(N)]

    dist = [[INF]*N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            if i==j:
                dist[i][j] = 0
            elif graph[i][j] != 0:
                dist[i][j] = graph[i][j]

    ans = LowerCost(dist)
    print(f'#{t} {ans}')





