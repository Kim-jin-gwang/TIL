# 완전 이진 트리 기준 순회

# 전위 순회
def preorder_traversal(idx):
    if idx <= N:
        print(tree[idx])
        preorder_traversal(idx*2)
        preorder_traversal(idx*2+1)

# 중위 순회
def inorder_traversal(idx):
    if idx <= N:
        inorder_traversal(idx * 2)
        print(tree[idx])
        inorder_traversal(idx * 2 + 1)

# 후위 순회
def postorder_traversal(idx):
    if idx <= N:
        postorder_traversal(idx*2)
        postorder_traversal(idx*2+1)
        print(tree[idx])


N = 5
tree = [0, 'A', 'B', 'C', 'D', 'E']


'''
    트리 구조
        'A'
      /   \
   'B'    'C'
  /   \
'D'    'E'
'''

print('전위 순회')
preorder_traversal(1)  # 'A' 'B' 'D' 'E' 'C'
print('중위 순회')
inorder_traversal(1)  # 'D' 'B' 'E' 'A' 'C'
print('후위 순회')
postorder_traversal(1)  # 'D' 'E' 'B' 'C''A'