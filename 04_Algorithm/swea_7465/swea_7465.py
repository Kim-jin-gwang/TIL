import sys
sys.stdin = open("input.txt", "r")


def find(x):
    if parent[x] != x:
        parent[x] = find(parent[x])
    return parent[x]

def union(a,b):
    a = find(a)
    b = find(b)

    if a<b:
        parent[b] = a
    else:
        parent[a] = b



T = int(input())
for t in range(1,T+1):
    N,M = map(int,input().split())
    parent = [0] * (N+1)
    for i in range(1,N+1):
        parent[i] = i
    
    for _ in range(M):
        a,b = map(int,input().split())
        if find(a) != find(b):
            union(a,b)
    
    ans = set()
    for i in range(1,N+1):
        ans.add(find(i))
    
    print(f'#{t} {len(ans)}')
