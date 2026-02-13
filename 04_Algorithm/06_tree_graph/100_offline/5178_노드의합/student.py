import sys
sys.stdin = open('input.txt')

T = int(input())
# 여러개의 테스트 케이스가 주어지므로, 각각을 처리합니다.
for test_case in range(1, T + 1):
    # 현재 받은 노드가 목표로 하는 노드의 자식인지를 판단한 후, 자식이 맞으면 더해주는 문제
    # ///////////////////////////////////////////////////////////////////////////////////
    N, M, L = map(int, input().split())
    # 결과 변수
    res = 0
    for i in range(M):
        node, val = map(int, input().split())
        # 노드의 번호를 이용하여 자식에 있는지 확인하는 과정
        while (node >= L):
            # 트리의 부모를 타고 가다가 값이 같아질 경우 부모-자식 관계로 판정
            if (node == L):
                res += val
                break
            # 자식은 계속 부모를 타고 이동
            node //= 2
    print(f"#{test_case} {res}")
    # ///////////////////////////////////////////////////////////////////////////////////