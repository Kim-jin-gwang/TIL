import sys
sys.stdin = open('algo2_sample_in.txt')


def search(r, path):
    # 도착 지점이면
    if r == G:
        if M in path:   # 경유 여부 확인 후
            paths.append(path)  # 추가
        return

    # 이동 가능한 모든 노드에 대해
    for n in range(1, V+1):
        # 아직 반문 한 적 없는 경우에만
        if adj_mat[r][n] and n not in path:
            search(n, path + [n])   # 조사


T = int(input())

for tc in range(1, T+1):
    # 노드의 개수, 간선의 개수
    V, E = map(int, input().split())
    # 시작, 도착, 경유
    S, G, M = map(int, input().split())
    # 0번 노드 없음
    adj_mat = [[0] * (V+1) for _ in range(V+1)]
    # 간선의 개수 만큼 인접 행렬 그리기
    for _ in range(E):
        # 무방향 그래프
        u, v = map(int, input().split())
        adj_mat[u][v] = 1
        adj_mat[v][u] = 1

    # 경로를 담을 리스트
    paths = []
    # print(S)
    # 시작 노드에서부터 출발
    search(S, [S])
    # print(paths)

    print(f'#{tc} {len(paths)}')
