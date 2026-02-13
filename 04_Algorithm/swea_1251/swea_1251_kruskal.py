import sys
sys.stdin = open("input.txt", "r")


'''
- 모든 섬을 해저터널로 연결하는 것을 목표로 함
- 환경 부담금 정책 = 환경 부담 세율(E)과 각 해저터널 길이(L)의 제곱의 곱 (E*L**2)
- 환경 부담금을 최소로 지불하며, N개의 모든 섬을 연결할 수 있는 교통 시스템 설계

'''

# 섬 끼리 거리 계산
def euclidean_dist(a,b):
    dist = ((b[0] - a[0])**2 + (b[1] - a[1])**2)**0.5
    return dist

# 환경부담금 계산
def cal_cost(E,a,b):
    return E * (euclidean_dist(a,b)**2)

# x의 루트노드 find
def find(x):
    if parent[x] != x:
        parent[x] = find(parent[x])
    return parent[x]

# 두 집합을 합치기
def union(a,b):
    a = find(a)
    b = find(b)

    if a < b:
        parent[b] = a
    else:
        parent[a] = b

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
    
    # 엣지에 섬끼리의 간선과 가중치 저장
    edges = []
    for i in range(N-1):
        for j in range(i+1,N):
            cost,a,b = cal_cost(E,islands_locate[i],islands_locate[j]), i, j
            edges.append((cost,a,b))
    edges.sort()
    
    # 부모 노드 초기화
    parent = [0] * N
    for i in range(N):
        parent[i] = i
    
    # 사이클 판별 후 없으면 두 집합을 합치고 노드 간의 가중치 더하기
    ans = 0.0
    for cost,a,b in edges:
        if find(a) != find(b):
            union(a,b)
            ans += cost
    
    ans = round(ans)
    print(f'#{t} {ans}')