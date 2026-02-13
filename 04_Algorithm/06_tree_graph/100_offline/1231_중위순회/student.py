import sys
sys.stdin = open("input.txt")


def inorder_tree(tree, N, idx):
    if idx > N:
        return ''

    return inorder_tree(tree, N, idx * 2) + tree[idx] + inorder_tree(tree, N, idx * 2 + 1)


def solve():
    N = int(input())
    tree = [''] * (N + 1)

    for idx in range(1, N + 1):
        node = list(input().split())
        tree[int(node[0])] = node[1]

    return inorder_tree(tree, N, 1)


if __name__ == '__main__':
    T = 10
    for tc in range(1, T + 1):
        print(f'#{tc} {solve()}')
