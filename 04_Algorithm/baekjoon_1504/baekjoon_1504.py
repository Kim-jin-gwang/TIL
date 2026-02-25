
import heapq
INF = int(1e9)

# 시작은 1번 정점

def Search(graph, N, start):
    distance = [INF] * (N+1)
    queue = []
    distance[start] = 0
    heapq.heappush(queue,(0,start))
    

    while queue:
        cur_dist, cur_node = heapq.heappop(queue)

        if distance[cur_node] < cur_dist:
            continue


        for nxt_node, nxt_dist in graph[cur_node]:
            cost = cur_dist + nxt_dist
            if distance[nxt_node] > cost:
                distance[nxt_node] = cost
                heapq.heappush(queue, (cost, nxt_node))
    
    return distance


N,E = map(int,input().split())
graph = [[] for _ in range(N+1)]
distance = [INF] * (N+1)
for _ in range(E):
    a,b,w = map(int,input().split())
    graph[a].append((b,w))
    graph[b].append((a,w))

v1, v2 = map(int,input().split())

dist_start = Search(graph, N, 1)
dist_v1 = Search(graph,N,v1)
dist_v2 = Search(graph,N,v2)

v1_first = dist_start[v1] + dist_v1[v2] + dist_v2[N]
v2_first = dist_start[v2] + dist_v2[v1] + dist_v1[N]

ans = min(v1_first, v2_first)
if ans >= INF:
    ans = -1

print(ans)