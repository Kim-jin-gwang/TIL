import sys
sys.stdin = open("input.txt", "r")


import heapq
INF = int(1e9)

def LowerCost(graph):
    dist = [INF] * (N+1)
    dist[0] = 0

    queue = []
    heapq.heappush(queue,(0,0))

    while queue:
        cur_dist, now = heapq.heappop(queue)

        if dist[now] < cur_dist:
            continue

        for nxt_node, nxt_dist in graph[now]:
            cost = cur_dist + nxt_dist

            if cost < dist[nxt_node]:
                dist[nxt_node] = cost
                heapq.heappush(queue,(cost, nxt_node))
    
    return dist[-1]


T = int(input())
for t in range(1,T+1):
    N,E = map(int,input().split())
    graph = [[] for _ in range(N+1)]
    for _ in range(E):
        start, end, weight = map(int,input().split())
        graph[start].append((end,weight))
    
    ans = LowerCost(graph)
    print(f'#{t} {ans}')