"""
기본적인 서로소 집합 자료구조
- 각 집합은 트리 형태로 표현
- parent[i] = j는 'i의 부모는 j'를 의미
- 자기 자신이 부모인 경우 그 원소가 집합의 대표자
"""
# 6개의 원소로 테스트
parent = make_set(6)
print(f"초기 상태: {parent}")

# 긴 트리를 만들어 비효율성 확인
union(5, 6)
union(4, 5)
union(3, 4)
union(2, 3)
union(1, 2)

print(f"연산 후 상태: {parent}")