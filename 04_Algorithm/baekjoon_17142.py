"""
- 바이러스는 활성 상태와 비활성 상태가 있음.
- 처음 모든 바이러스는 비활성 상태이고, 활성 상태인 바이러스는 상하좌우로 인접한 모든 빈 칸으로 동시에 복제되며 1초 걸림
- M개의 바이러스를 활성 상태로 변경하려고 함
- 0은 빈칸, 1은 벽, 2는 바이러스의 위치

- 연구소의 상태가 주어졌을 때, 모든 빈 칸에 바이러스를 퍼뜨리는 최소 시간 계산
- 다 못퍼뜨리면 -1 반환



● 아이디어
    - 2인 위치를 미리 담아놓고 하나하나 돌면서 주변에 바이러스 퍼뜨리기
    - 활성 상태로 만들어야 하는 바이러스의 개수가 정해져있기 때문에 itertools로 모든 조합을 다 bfs로 돌려보고 최소 시간 찾기
    - 가지치기 : 최소 시간보다 시간이 커졌으면 return
"""

from collections import deque
from itertools import combinations

dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]
INF = int(1e9)


def Search(virus, lab):
    global ans

    visited = [[-1] * N for _ in range(N)]
    queue = deque([])

    for vx, vy in virus:
        queue.append((vx, vy))
        visited[vx][vy] = 0

    while queue:
        x, y = queue.popleft()
        if lab[x][y] == 0 and visited[x][y] >= ans:
            return

        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]

            if (
                0 <= nx < N
                and 0 <= ny < N
                and lab[nx][ny] != 1
                and visited[nx][ny] == -1
            ):

                visited[nx][ny] = visited[x][y] + 1
                queue.append((nx, ny))
    tmp = 0
    for i in range(N):
        for j in range(N):
            if lab[i][j] == 0:
                if visited[i][j] == -1:
                    return
                tmp = max(tmp, visited[i][j])
    ans = min(ans, tmp)


N, M = map(int, input().split())
lab = [list(map(int, input().split())) for _ in range(N)]
viruses = [(r, c) for r in range(N) for c in range(N) if lab[r][c] == 2]
ans = INF

for virus in combinations(viruses, M):
    Search(virus, lab)

print(-1 if ans == INF else ans)
