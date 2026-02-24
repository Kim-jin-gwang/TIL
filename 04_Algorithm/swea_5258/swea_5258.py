import sys
sys.stdin = open("input.txt", "r")


T = int(input())
for t in range(1,T+1):
    N, M = map(int,input().split()) # N = 박스의 크기, M = 상품의 개수
    arr = [0] * (N+1)

    for _ in range(M):
        size, price = map(int,input().split())
        for i in range(N,size-1,-1):
            arr[i] = max(arr[i], arr[i-size] + price)
    
    print(f'#{t} {arr[-1]}')
