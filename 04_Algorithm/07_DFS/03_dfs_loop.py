def dfs(graph, now, visited):
    # 방문 예정지를 stack에 담아 두겠다
    stack = []
    # 현재 지점을 방문 후보에 등록
    stack.append(now)
    visited.add(now)    # 현재위치 방문 표시
    
    while stack:    # 방문 해야 할 목록이 남은 동안
        target = stack.pop()    # LIFO
        print(target)           # 방문

        for next in graph[target]:
            if next not in visited: # 방문 한적 없다면
                stack.append(next)  # 후보군에 등록
                # 후보군에 삽입되는 순간,
                # 언젠가는 방문할 것이라는 뜻이므로
                visited.add(next)

# 그래프 인접 리스트
graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'E'],
    'D': ['B', 'F'],
    'E': ['B', 'F'],
    'F': ['D', 'E', 'G'],
    'G': ['C']
}

start_vertex = 'A'
visited = set()  # 방문한 정점을 저장할 집합

dfs(graph, start_vertex, visited) 