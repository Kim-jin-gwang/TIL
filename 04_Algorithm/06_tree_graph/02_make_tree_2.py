# 부모의 정보만 주어질 때, 이진 트리 생성하기
# 자신의 값, 부모 인덱스 (부모가 0인 경우, 루트)
input_data = [
    ['A', 0],
    ['C', 1],
    ['B', 1],
    ['F', 3],
    ['G', 6],
    ['E', 2],
    ['D', 2]
]
N = 16
tree = [0] * (N + 1)
for data in input_data:
    value = data[0]
    parent = data[1]

    left_child = parent * 2
    right_child = parent * 2 + 1

    if parent == 0: # 루트
        tree[1] = value
        continue
    if tree[left_child] == 0:
        tree[left_child] = value
    else:
        tree[right_child] = value
print(tree)


