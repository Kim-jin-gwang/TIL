import sys
sys.stdin = open("input.txt", "r")


def search(idx,cnt):
    global ans

    if cnt == K:
        ans += 1
        return
    
    if idx == N:
        return
    
    search(idx+1,cnt+arr[idx])
    search(idx+1,cnt)


T = int(input())
for t in range(1,T+1):
    N,K = map(int,input().split())
    arr = list(map(int,input().split()))
    ans = 0
    search(0,0)
    
    print(f'#{t} {ans}')