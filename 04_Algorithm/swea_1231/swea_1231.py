import sys

sys.stdin = open("input.txt", "r")



def in_order(n):
    if n <= N:
        in_order(n*2)
        print(tree[n], end='')
        in_order(n*2+1)


for t in range(1,11):
    N = int(input())
    tree = [0] * (N+1)

    # 왜 leaf도 저장하는거지???????
    for _ in range(N):
        parts = input().split()
        idx = int(parts[0])
        tree[idx] = parts[1]

    print(f'#{t}', end=' ')
    in_order(1)
    print()
