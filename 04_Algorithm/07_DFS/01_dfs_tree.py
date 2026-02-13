'''
일반 트리 예시
            'A'
        /    |    \
    'B'     'C'     'D'
  /     \         /  |  \
'E'     'F'     'G' 'H' 'I'
'''

def DFS(node):
    '''
        :param node: 탐색 대상 노드
    '''
    # 현재 방문한 노드의 정보를 출력
    print(node)
    for next in tree.get(node, []):
        DFS(next)



tree = {
    'A': ['B', 'C', 'D'],
    'B': ['E', 'F'],
    # 'C': [],
    'D': ['G', 'H', 'I'],
    # 'E': [],
    # 'F': [],
    # 'G': [],
    # 'H': [],
    # 'I': []
}

DFS('A')