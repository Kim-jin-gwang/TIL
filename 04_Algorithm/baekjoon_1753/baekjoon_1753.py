
import heapq
import sys
input = sys.stdin.readline

INF = int(1e9)

def Search(graph, distance, K):
    queue = []
    distance[K] = 0

    heapq.heappush(queue,(0,K))

    while queue:
        cur_dist, cur_node = heapq.heappop(queue)

        if distance[cur_node] < cur_dist:
            continue

        for nxt_node, nxt_dist in graph[cur_node]:
            cost = cur_dist + nxt_dist
            if distance[nxt_node] > cost:
                distance[nxt_node] = cost
                heapq.heappush(queue,(cost,nxt_node))
    
    return distance
    

V,E = map(int,input().split()) # 노드, 간선
K = int(input())   # 시작 정점

graph = [[] for _ in range(V+1)]
for _ in range(E):
    u,v,w = map(int,input().split())  # u -> v, w(가중치)
    graph[u].append((v,w))
distance = [INF] * (V+1)

ans = Search(graph, distance, K)
for i in range(1, V+1):
    if ans[i] == INF:
        ans[i] = 'INF'
    print(ans[i])
