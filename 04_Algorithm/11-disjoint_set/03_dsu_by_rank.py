"""
랭크(Rank)를 활용한 Union 최적화
각 집합의 높이를 랭크로 기록하고, 랭크가 낮은 트리를 높은 트리 밑에 붙여서
전체 트리의 높이 증가를 억제
"""

def make_set(n):
    """부모 리스트와 랭크 리스트 초기화"""
    pass

def find_set(x):
    """기본 find_set (랭크 최적화 확인용)"""
    pass

def union_by_rank(x, y):
    """랭크를 이용한 최적화된 union"""
    pass


parent, rank = make_set(6)
print(f"초기 상태:")
print(f"parent: {parent}")
print(f"rank:   {rank}")
print()

print("union(1, 2):")
union_by_rank(1, 2)  # rank(1)이 1로 증가
print(f"parent: {parent}")
print(f"rank:   {rank}")
print()

print("union(3, 4):")
union_by_rank(3, 4)  # rank(3)이 1로 증가
print(f"parent: {parent}")
print(f"rank:   {rank}")
print()

print("union(1, 3):")
union_by_rank(1, 3)  # 랭크가 같으므로 rank(1)이 2로 증가
print(f"parent: {parent}")
print(f"rank:   {rank}")
print()

print("union(1, 6):")
union_by_rank(1, 6)  # rank(1)변화 없음.
print(f"parent: {parent}")
print(f"rank:   {rank}")


