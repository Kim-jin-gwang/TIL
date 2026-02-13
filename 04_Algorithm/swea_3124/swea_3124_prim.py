import sys
sys.stdin = open("input.txt", "r")

import heapq

def prim(V,graph,start=1):
    visited = [False] * (V+1)

    pq = [(0,-1,start)]
    
    mst_cost = 0    # 최소 신장 트리의 가중치
    mst_edges = []  # 지금까지 넣은 엣지들의 모음
    picked = 0      # 선택한 간선의 개수 -> V만큼 선택했으면 while문 벗어나기

    while pq and picked < V:
        weight, prev, end = heapq.heappop(pq)   #end가 이번에 방문할 정점

        if visited[end]:
            continue

        visited[end] = True
        mst_cost += weight
        picked += 1

        #시작 정점 제외
        if prev != -1:
            mst_edges.append((prev,end,weight))
        
        # 현재 정점에서 갈 수 있는 간선 추가
        for next_node, next_weight in graph[end]:
            if not visited[next_node]:
                heapq.heappush(pq,(next_weight, end, next_node))
        
    if picked != V:
        return None, []
    
    return mst_cost, mst_edges
        



T = int(input())
for t in range(1,T+1):
    V,E = map(int,input().split())

    graph = [[] for _ in range(V+1)]

    edges = [] # a,b,cost 순서
    for _ in range(E):
        a,b,cost = map(int,input().split())
        edges.append((a,b,cost))
    
    for a,b,cost in edges:
        graph[a].append((b,cost))
        graph[b].append((a,cost))
    
    ans_cost, mst = prim(V,graph,start=1)
    
    print(f'#{t} {ans_cost}')
    