import sys
sys.stdin = open("input.txt", "r")

'''
- CC(i) = ∑ j dist(i,j)  // (단, dist(i,j)는 노드i로부터 노드 j까지의 최단 거리이다.)
    - 즉, 한 노드에서 모든 노드까지의 거리의 합 중 가장 최소값 출력
- 시작 정점 하나하나 다 돌면서 최솟값 찾기

- 입력은 한줄로 주어짐
    - N, 사람 네트워크의 인접 행렬이 행 우선 순으로 주어짐

    - 가중치는 1이거나 1이 아니거나
    - 플로이드 워셜? 다익스트라? 음수 가중치가 없으므로 벨만 포드는 아닐 것 같음
    - 다익스트라로 하는데 start노드를 1~N으로 바꿔가면서 해보기


'''
import heapq
INF = int(1e9)


def FindCC(start,distance):
    queue = []
    heapq.heappush(queue,(0,start)) # 현재 최단 거리, 시작 노드

    while queue:
        dist,now = heapq.heappop(queue)

        if distance[now] < dist:
            continue

        for nxt_node, nxt_dist in graph[now]:
            cost = nxt_dist + dist
            if cost < distance[nxt_node]:
                distance[nxt_node] = cost
                heapq.heappush(queue, (cost, nxt_node))
    
    return sum(distance)



T = int(input())
for t in range(1,T+1):
    # input을 전처리
    data = list(map(int,input().split()))
    N = data[0]
    arr = data[1:]
    matrix = [arr[i*N:(i+1)*N] for i in range(N)]


    # 인접리스트화
    graph = [[] for _ in range(N)]
    for i in range(N):
        for j in range(N):
            if matrix[i][j] == 1:
                graph[i].append((j,matrix[i][j]))


    # start 노드 기준으로 다익스트라 하기
    ans = INF
    for i in range(N):
        distance = [INF] * (N)
        distance[i] = 0
        tmp = FindCC(i,distance)
        ans = min(ans,tmp)
    
    print(f'#{t} {ans}')
        


    

