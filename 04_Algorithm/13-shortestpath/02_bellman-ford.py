
'''
- 시작 정점에서 모든 정점까지 도달하는 최소비용
- 각 정점에 도달하는 비용을 초기화 해둔 리스트 필요
- 각 정점별 인접 정점들에게 내 위치까지 도달한 누적비용을 기준으로 다음 인접 정점에 도달하는 최소 비용으로 갱신
- 단, 도달한 적 없는 정점에 대해서는 조사안해도 됨

'''




def bellman_ford(graph, start):
    distance = {v:float('inf') for v in graph}
    distance[start] = 0

    #  V-1번 만큼 반복
    for _ in range(len(graph) - 1):
        # 각 정점 별 순회
        for now in graph:
            # 이번에 조사 대상이 된 u의 인접 정점들
            for nxt,w in graph[now].items():
                # 해당 정점에 도달한 적 있어야 하고,
                # 내 현재 위치까지 도달하는데 드는 누적비용 distance[now] + w
                # 그 누적비용이 다음 위치 distance[nxt]에 든 비용보다 싸다면
                # 더 싸게 갈 수 있는 방법이 있다는 것이니 갱신
                cost = distance[now] + w
                if distance[now] != float('inf') and cost < distance[now]:
                    distance[now] = cost

# 예시 그래프
graph = {
    'a': {'b': 4, 'c': 2},
    'b': {'c': 3, 'd': 2, 'e': 3},
    'c': {'b': 1, 'd': 4, 'e': 5},
    'd': {'e': -3},
    'e': {'f': 2},
    'f': {}
}

# 음수 사이클 예시 그래프
# graph = {
#     'a': {'b': 4, 'c': 2},
#     'b': {'c': -3, 'd': 2, 'e': 3},
#     'c': {'b': 1, 'd': 4, 'e': 5},
#     'd': {'e': -3},
#     'e': {'f': 2},
#     'f': {}
# }

# 시작 정점 설정
start_vertex = 'a'

# 벨만-포드 알고리즘 실행
result = bellman_ford(graph, start_vertex)

print(f"'{start_vertex}': {result}")
