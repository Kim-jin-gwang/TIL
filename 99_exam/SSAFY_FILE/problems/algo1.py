# ==============================================
# 코드 제출시 아래 2줄은 반드시 주석처리 하여 제출
# import sys
# sys.stdin = open('algo1_sample_in.txt')
# ==============================================

# 아래에 코드를 작성하세요.

dx = [0,1,0,-1]
dy = [1,0,-1,0]

# 도로 순회를 위한 dfs
def dfs(x,y):
    global cnt
    cnt += 1

    visited[x][y] = True
    for i in range(4):
        nx = dx[i] + x
        ny = dy[i] + y
        if 0<=nx<N and 0<=ny<M:
            if not visited[nx][ny] and village[nx][ny] == 0: # 다음 경로를 방문하지 않았고 도로일 때만 방문
                visited[nx][ny] = True
                dfs(nx,ny)
    return



T = int(input())
for t in range(1,T+1):
    N,M = map(int,input().split())
    village = [list(map(int,input().split())) for _ in range(N)]

    cnt = 0
    ans = 0

    for i in range(N):
        for j in range(M):
            visited = [[False] * M for _ in range(N)]
            if village[i][j] == 1:   # 도로일 때만 순회
                continue
            dfs(i,j)            # cnt 증가
            cnt_a = cnt         # a의 cnt로 바꿈
            cnt = 0             # b를 계산하기 위한 cnt초기화

            # b 계산
            for k in range(N):
                for l in range(M):
                    cnt_b = 0
                    if visited[k][l] or village[k][l] == 1:   # a에서 방문을 했으면 cnt_b는 0 or 도로일 때만 순회
                        continue
                    else:
                        dfs(k,l)
                        cnt_b = cnt  # b의 cnt로 바꿈

                    ans = max(ans, cnt_a + cnt_b) # 최대값으로 변환
                    cnt = 0

    print(f'#{t} {ans}')