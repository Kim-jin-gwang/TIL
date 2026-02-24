import heapq, math


def dijkstra(graph, start):
    pass

graph = {
    'a': {'b': 3, 'c': 5},
    'b': {'c': 2, 'd': 6},
    'c': {'b': 1, 'd': 4, 'e': 6},
    # 'c': {'b': -4, 'd': 4, 'e': 6},
    'd': {'e': 2, 'f': 3},
    'e': {'f': 6},
    'f': {}
}
start_v = 'a'
res = dijkstra(graph, start_v)
print(res)  # {'a': 0, 'b': 3, 'c': 5, 'd': 9, 'e': 11, 'f': 12}

