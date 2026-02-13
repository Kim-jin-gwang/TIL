import sys
sys.stdin = open("input.txt", "r")
INF = 1000000001

T = int(input())
for t in range(1,T+1):
    N,K = map(int,input().split())
    candy = sorted(list(map(int,input().split())))

    ans = INF
    for i in range(N-K+1):
        ans = min(ans,candy[i+K-1]-candy[i])  # 슬라이딩 윈도우를 사용하여 최소값 찾기
    
    print(f'#{t} {ans}')