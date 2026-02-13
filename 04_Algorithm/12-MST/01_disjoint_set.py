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


p, rank = make_set([1, 2, 3, 4, 5, 6])
print(p)  # 초기 부모 노드 배열 출력
print(rank)  # 초기 랭크 배열 출력
print()

# 간선 추가
edges = [(1, 2), (2, 3), (4, 5), (5, 6), (3, 4)]
# 간선을 통해 유니온 연산 수행
for i, (u, v) in enumerate(edges):
    union(p, rank, u, v)
print(p)       # 최종 부모 노드 배열 출력
print(rank)    # 최종 랭크 배열 출력
