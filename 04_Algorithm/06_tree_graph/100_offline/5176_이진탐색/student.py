import sys
sys.stdin = open("input.txt", "r")

# 중위 순회하며 값 삽입
def inorder_traversl(idx, N):
    global cnt
    if idx <= N:
        # 왼쪽 조사
        inorder_traversl(idx*2, N)
        # 루트 cnt값 넣기
        binary_tree[idx] = cnt
        cnt += 1
        # 오른쪽 조사
        inorder_traversl(idx * 2+1, N)


T = int(input())

# 여러개의 테스트 케이스가 주어지므로, 각각을 처리합니다.
for test_case in range(1, T + 1):
    N = int(input())
    binary_tree = [0] * (N+1)
    cnt = 1
    inorder_traversl(1, N)
    # print(binary_tree)
    print(f'#{test_case} {binary_tree[1]} {binary_tree[N//2]}')
