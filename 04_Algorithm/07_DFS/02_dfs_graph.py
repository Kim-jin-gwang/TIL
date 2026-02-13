# now:탐색 정점 
# adj_matrix:인접 행렬
# visited:방문 체크 배열
def dfs(now, adj_matrix, visited):
    # 할 일이 출력 말고도 또 있다?
    print(graph[now])
    visited[now] = True # 여기 도착.

    # 현재 위치에서 진출 가능한 정점?
    for next in range(N):
        if adj_matrix[now][next] == 1 and not visited[next]:
            dfs(next, adj_matrix, visited)



        # 0    1    2    3    4    5    6
graph = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
# 정점 수: N
N = 7
# 인접 행렬
adj_matrix = [
    [0, 1, 1, 0, 0, 0, 0],
    [1, 0, 0, 1, 1, 0, 0],
    [1, 0, 0, 0, 1, 0, 0],
    [0, 1, 0, 0, 0, 1, 0],
    [0, 1, 1, 0, 0, 1, 0],
    [0, 0, 0, 1, 1, 0, 1],
    [0, 0, 0, 0, 0, 1, 0],
]

# 방문 체크 배열 초기화
visited = [False] * N  # 모든 정점을 아직 방문하지 않았다고 표시

# 시작 정점: 0
dfs(0, adj_matrix, visited)  # 깊이 우선 탐색 시작
