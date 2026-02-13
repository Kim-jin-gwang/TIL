import sys
sys.stdin = open("input.txt", "r")


def find(x):
    if parent[x] != x:
        parent[x] = find(parent[x])
    return parent[x]

def union(a,b):
    a = find(a)
    b = find(b)

    if a < b:
        parent[b] = a
    else:
        parent[a] = b
    


T = int(input())
for t in range(1,T+1):
    V,E = map(int,input().split())

    parent = [0] * (V+1)
    for i in range(V+1):
        parent[i] = i
    
    edges = []
    for _ in range(E):
        a,b,cost = map(int,input().split())
        edges.append((cost,a,b))
    edges.sort()

    ans = 0
    for edge in edges:
        cost,a,b = edge
        if find(a) != find(b):
            union(a,b)
            ans += cost
    
    print(f'#{t} {ans}')
