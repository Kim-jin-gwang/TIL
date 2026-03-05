

'''
- 구역 나누기

- 최솟값 차이 찾기

'''
from itertools import combinations
from collections import deque

def is_connected(group):
    # 텅 빈 그룹이 들어왔을 때
    if not group:
        return False
    
    group_list = list(group) # 그룹을 리스트로 만들기
    start = group_list[0]
    queue = deque([start])

    # 방문한 지점은 탐색 안하기
    visited = set()
    visited.add(start)

    while queue:
        cur = queue.popleft()

        # 현재 위치와 이웃한 노드들 탐색
        for neighbor in edges[cur]:
            # 인접 노드가 우리 그룹이고 방문을 안해야 함
            if neighbor in group and neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    
    return len(visited) == len(group)


# 1부터 시작
N = int(input())
population = [0]
population.extend(list(map(int,input().split())))

# 간선 저장 : 현재 노드에서 갈 수 있는 주변 노드 탐색
edges = [[] for _ in range(N+1)]
for i in range(1,N+1):
    data = list(map(int,input().split()))
    cnt = data[0]
    if cnt > 0:
        edges[i] = data[1:]
    

ans = int(1e9)
sections = list(range(1,N+1))

# combinations로 모든 경우의 수 탐색
for i in range(1,N//2+1):
    for c in combinations(sections, i):
        group_a = set(c)
        group_b = set(sections) - group_a
        if is_connected(group_a) and is_connected(group_b):
            sum_a = sum(population[i] for i in group_a)
            sum_b = sum(population[i] for i in group_b)
            ans = min(ans, abs(sum_a - sum_b))


if ans == int(1e9):
    print(-1)
else:
    print(ans)



