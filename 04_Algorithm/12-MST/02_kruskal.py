def make_set(vertices):
    N = len(vertices)
    p = list(range(N + 1))  # 부모 노드 배열 초기화
    rank = [0] * (N + 1)  # 랭크 배열 초기화
    return p, rank


def find_set(p, x):
    if x != p[x]:  # 노드 x가 자기 자신을 부모로 가지지 않는 경우
        p[x] = find_set(p, p[x])  # 부모 노드를 재귀적으로 찾고 경로 압축 수행
    return p[x]


def union(p, rank, x, y):
    px = find_set(p, x)  # 노드 x의 대표자(부모) 찾기
    py = find_set(p, y)  # 노드 y의 대표자(부모) 찾기

    if px != py:
        if rank[px] < rank[py]:
            p[px] = py  # x의 부모를 y의 부모로 설정
        elif rank[px] > rank[py]:
            p[py] = px  # y의 부모를 x의 부모로 설정
        else:
            p[py] = px  # y의 부모를 x의 부모로 설정
            rank[px] += 1  # x의 랭크를 1 증가
        
def mst_kruskal(vertices, edges):
    pass

'''
    가중치 그래프 형상
         1
      ¹ / \ ²
       2---3
         ³
'''
# [시작정점, 도착정점, 가중치]
edges = [[1, 2, 1], [2, 3, 3], [1, 3, 2]]
vertices = [1, 2, 3]  # 정점 집합


'''
    MST 구성 결과
         1
      ¹ / \ ²
       2   3
'''
result = mst_kruskal(vertices, edges)  # [[1, 2, 1], [1, 3, 2]]
print(result)


# 교재 간선 정보
# edges = [
#     (0, 1, 32),
#     (0, 2, 31),
#     (0, 5, 60),
#     (0, 6, 51),
#     (1, 2, 21),
#     (2, 4, 46),
#     (2, 6, 25),
#     (3, 4, 34),
#     (3, 5, 18),
#     (4, 5, 40),
#     (4, 6, 51),
# ]
# vertices = list(range(7))  # 정점 집합

# result = mst_kruskal(vertices, edges)
# print(result) # [(3, 5, 18), (1, 2, 21), (2, 6, 25), (0, 2, 31), (3, 4, 34), (2, 4, 46)]