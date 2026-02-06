import sys

sys.stdin = open("input.txt", "r")


T = int(input())
for t in range(1,T+1):
    N,M,L = map(int,input().split())
    tree = [0] * (N+1)
    for _ in range(M):
        a,v = map(int,input().split())
        tree[a] = v


    for i in range(N,0,-1): #리프에서부터 더해야 하므로 뒤에서부터 시작
        if 2*i <= N:
            tree[i] += tree[2*i]  # 왼쪽 자식 값 채우기
        if 2 * i+1 <= N:
            tree[i] += tree[2 * i+1]  # 오른쪽 자식 값 채우기

    print(f'#{t} {tree[L]}')
