import sys
sys.stdin = open("input.txt", "r")


'''
- 모든 섬을 해저터널로 연결하는 것을 목표로 함
- 환경 부담금 정책 = 환경 부담 세율(E)과 각 해저터널 길이(L)의 제곱의 곱 (E*L**2)
- 환경 부담금을 최소로 지불하며, N개의 모든 섬을 연결할 수 있는 교통 시스템 설계

'''
import heapq


# 섬 끼리 거리 계산
def euclidean_dist(a,b):
    dist = ((b[0] - a[0])**2 + (b[1] - a[1])**2)**0.5
    return dist

# 환경부담금 계산
def cal_cost(E,a,b):
    return E * (euclidean_dist(a,b)**2)

# 프림 알고리즘으로 문제 풀이
def prim(n,graph,start=0):
    visited = [False] * n
    pq = [(0,start)] # cost, prev, end
    
    mst_cost = 0
    picked = 0

    while pq and picked < n:
        weight, end = heapq.heappop(pq)
        
        if visited[end]:
            continue

        visited[end] = True
        picked +=1
        mst_cost += weight

        for next_node, next_weight in graph[end]:
            if not visited[next_node]:
                heapq.heappush(pq, (next_weight,next_node))
        
    if picked != n:
        return None
    
    return mst_cost


T = int(input())
for t in range(1,T+1):
    N = int(input())
    coordinate_x = list(map(int,input().split()))
    coordinate_y = list(map(int,input().split()))
    E = float(input())

    # 섬의 좌표를 저장
    islands_locate = []
    for _ in range(N):
        x = coordinate_x.pop()
        y = coordinate_y.pop()
        islands_locate.append((x,y))
    
    # 그래프에 섬끼리의 경로와 가중치를 append
    graph = [[] for _ in range(N)]
    for i in range(N-1):
        for j in range(i+1,N):
            a, b, cost = i, j, cal_cost(E, islands_locate[i],islands_locate[j])
            graph[a].append((b,cost))
            graph[b].append((a,cost))
    
    ans = round(prim(N,graph,start=0))
    print(f'#{t} {ans}')
