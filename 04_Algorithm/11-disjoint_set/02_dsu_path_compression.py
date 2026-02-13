"""
경로 압축(Path Compression) 최적화
find_set을 실행하며 만나는 모든 노드가 대표자를 직접 가리키도록 부모 정보를 갱신
트리의 높이를 효과적으로 압축
"""

def make_set(n):
    pass

def find_set_pc(x):
    """경로 압축이 적용된 find_set"""
    pass

def union(x, y):
    """두 집합을 합치기"""
    pass


parent = make_set(6)

# 긴 트리 생성
union(5, 6)
union(4, 5)
union(3, 4)
union(2, 3)
union(1, 2)
print(f"긴 트리 상태: {parent}")

# 경로 압축 테스트
find_set_pc(6)
print(f"경로 압축 후: {parent}")