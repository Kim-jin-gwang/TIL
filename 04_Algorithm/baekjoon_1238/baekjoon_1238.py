import heapq
INF = int(1e9)

def Search(graph,N,start,X):
    distance = [INF] * (N+1)
    distance[start] = 0

    queue = []
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

    return distance[X]




N,M,X = map(int,input().split()) # 노드, 간선, 도착 지점
graph = [[] for _ in range(N+1)]
for _ in range(M):
    a,b,w = map(int,input().split())
    graph[a].append((b,w))

ans = 0
for i in range(1,N+1):
    ans = max(ans, Search(graph,N,i,X) + Search(graph,N,X,i))

print(ans)