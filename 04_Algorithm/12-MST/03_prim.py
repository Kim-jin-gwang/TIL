import heapq

def prim(vertices, edges):
    pass


'''
    가중치 그래프 형상
         1
      ¹ / \ ²
       2---3
         ³
'''
vertices = [1, 2, 3]
edges = [[1, 2, 1], [2, 3, 3], [1, 3, 2]]

# 인접 리스트


'''
    MST 구성 결과
         1
      ¹ / \ ²
       2   3
'''
mst = prim(vertices, edges)  # [(1, 2, 1), (1, 3, 2)]
print(mst)


# # 교재 간선 정보
# edges = [
#     (0, 1, 32),
#     (0, 2, 31),
#     (0, 5, 60),
#     (0, 6, 51),
#     (1, 2, 21),
#     (2, 4, 46),
#     (2, 6, 25),
#     (3, 4, 34),
#     (3, 5, 18),
#     (4, 5, 40),
#     (4, 6, 51),
# ]
# vertices = list(range(7))  # 정점 집합

# result = prim(vertices, edges)
# print(result) # [(0, 2, 31), (2, 1, 21), (2, 6, 25), (2, 4, 46), (4, 3, 34), (3, 5, 18)]