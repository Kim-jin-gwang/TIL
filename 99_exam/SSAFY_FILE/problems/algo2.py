# ==============================================
# 코드 제출시 아래 2줄은 반드시 주석처리 하여 제출
# import sys
# sys.stdin = open('algo2_sample_in.txt')
# ==============================================

# 아래에 코드를 작성하세요.

def dfs(cur,auth,des,path,flag):
    global ans
    if cur == des: # 도착 지점일 때
        if path in visited_path or not flag: # 이미 가본 경로거나 보안 인증을 거치지 않았다면 return
            return
        visited_path.add(path)  # 기본 경로가 아니면 가본 경로에 add
        ans += 1
        return

    visited[cur] = True
    if cur == auth:  # 지금 경로가 보안인증이면 flag = True
        flag = True

    for nxt in graph[cur]:  # 그래프 순회
        if not visited[nxt]:
            visited[nxt] = True
            dfs(nxt, auth, des, path+str(nxt), flag)
            visited[nxt] = False


T = int(input())
for t in range(1,T+1):
    V,E = map(int,input().split())
    S,G,M = map(int,input().split())
    graph = [[] for _ in range(V+1)] # 그래프 초기화

    visited = [False] * (V+1)
    visited_path = set()   # 방문했던 경로를 표현하기 위한 path값 저장소

    for _ in range(E):  # 그래프에 값 삽입
        a,b = map(int,input().split())
        graph[a].append(b)
        graph[b].append(a)

    ans = 0
    dfs(S, M, G, str(S), False)

    print(f'#{t} {ans}')