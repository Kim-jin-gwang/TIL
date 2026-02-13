import sys
sys.stdin = open("input.txt", "r")


# 부모를 찾는 find 함수
def find(x):
    if parent[x] != x:
        parent[x] = find(parent[x])
    return parent[x]


# 두 집합을 합치는 union함수
def union(x,y):
    x = find(x)
    y = find(y)

    if x < y:
        parent[y] = x
    else:
        parent[x] = y


T = int(input())
for t in range(1,T+1):
    n,m = map(int,input().split())
    parent = [0] * (n+1)
    for i in range(1,n+1):
        parent[i] = i

    ans = ''
    for _ in range(m):
        # 0이면 집합 합치기, 1이면 같은 집합에 포함되어 있는지 확인
        check,a,b = map(int,input().split())

        if check == 0:
            if find(a) != find(b):
                union(a,b)
        
        elif check == 1:
            if find(a) == find(b):
                ans += str(1)
            else:
                ans += str(0)
    
    print(f'#{t} {ans}')