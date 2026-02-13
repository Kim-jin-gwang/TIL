# 간선 리스트
edges = [
    (0, 1),
    (0, 2),
    (0, 5),
    (0, 6),
    (1, 3),
    (2, 3),
    (3, 4),
    (3, 5),
    (3, 6),
    (4, 6)
]

V = 7
# 인접 행렬 -> V * V 형태의 정방 2차원 리스트
# 0과 1로 채워서, 갈수 있는곳은 1로 작성
adj_mat = [[0] * V for _ in range(V)]
for edge in edges:
    u, v = edge
    # print(u, v)
    # 무방향 그래프인 경우, 양방향으로 이동 가능하도록 체크
    adj_mat[u][v] = 1
    adj_mat[v][u] = 1


for row in adj_mat:
    print(row)

# 인접 리스트
adj_list = {i: [] for i in range(V)}

for edge in edges:
    u, v = edge
    adj_list[u].append(v)
    adj_list[v].append(u)

print(adj_list)














