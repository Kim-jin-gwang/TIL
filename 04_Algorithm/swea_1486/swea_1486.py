import sys
sys.stdin = open("input.txt", "r")

'''
- 높이가 B 이상인 탑 중에서 높이가 가장 낮은 탑을 알아내는 문제(B가 넘는 것 중 최소값)
- B가 넘는데, cur이 ans보다 높으면 가지치기


'''
INF = int(1e9)

def Search(idx, cur):
    global ans
    if idx == N:
        if cur >= B:
            ans = min(ans,cur)
            return
        return
    
    if cur >= B and cur >= ans:
        return
    
    Search(idx+1, cur+tall[idx])
    Search(idx+1, cur)




T = int(input())
for t in range(1,T+1):
    N,B = map(int,input().split())
    tall = list(map(int,input().split()))
    visited = [False] * N

    ans = INF
    Search(0,0)

    print(f'#{t} {ans-B}')
