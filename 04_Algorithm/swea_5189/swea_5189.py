import sys

sys.stdin = open("input.txt", "r")


def search(idx, cur, price):
    global ans

    if price >= ans:
        return
    
    if idx == N-1:  # 끝 번호에 도달하면 끝 -> 0 비용 더하고 갱신
        ans = min(ans, price+cart[cur][0])  # 마지막 cur에서 다시 출발지로 돌아가는 가중치 계산
        return


    for i in range(1,N):   # 0은 시작점이기 때문에 방문 안함
        if not visited[i]:
            visited[i] = True
            search(idx+1,i, price + cart[cur][i])  # 지금 가중치를 price에 계산 1->2, 2->3...
            visited[i] = False


T = int(input())
for t in range(1,T+1):
    N = int(input())
    cart = [list(map(int,input().split())) for _ in range(N)]
    visited = [False] * N
    ans = 1000001

    search(0,0,0)
    print(f'#{t} {ans}')