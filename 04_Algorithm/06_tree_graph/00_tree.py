'''
아래와 같은 이진 트리가 있다면,
        'A'
       /   \
    'B'     'C'
    /  
  'D'
  /
'E'
'''
tree = [None, 'A', 'B', 'C', 'D', None, None, None, 'E', None, None, None, None, None, None, None]
# 1번 index를 root로 설정하였을 때,
# 'A'의 왼쪽, 오른쪽 자식은 각각 2, 3 index에 해당함
# 'B'의 왼쪽, 오른쪽 자식은 각각 4, 5 index에 해당함
# 'D'의 왼쪽, 오른쪽 자식은? 


print('존재하는 모든 요소 출력하기')
H = 4
for index in range(2**H):
    node = tree[index]
    if node:
        print(node, end=' ')
print()


print('조상 찾기')
# 'E' 노트 -> 8번 인덱스에 있음.
index = 8
while index > 1:
    parent = tree[index // 2]
    print(parent)
    index //= 2

print('왼쪽 or 오른쪽 자식 찾기')
index = 1
while index < (2**H)//2:
    left_child = tree[index * 2]
    right_child = tree[index * 2 + 1]
    print(left_child, right_child)
    index *= 2

