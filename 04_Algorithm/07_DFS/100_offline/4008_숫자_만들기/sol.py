import sys
sys.stdin = open('input.txt')

'''
1. 시간 제한 : 최대 50 개 테스트 케이스를 모두 통과하는 데 C / C++ / Java 모두 3 초

2. 게임 판에 적힌 숫자의 개수 N 은 3 이상 12 이하의 정수이다. ( 3 ≤ N ≤ 12 )

3. 연산자 카드 개수의 총 합은 항상 N - 1 이다.

4. 게임 판에 적힌 숫자는 1 이상 9 이하의 정수이다.

5. 수식을 완성할 때 각 연산자 카드를 모두 사용해야 한다..

6. 숫자와 숫자 사이에는 연산자가 1 개만 들어가야 한다.

7. 완성된 수식을 계산할 때 연산자의 우선 순위는 고려하지 않고, 왼쪽에서 오른쪽으로 차례대로 계산한다.

8. 나눗셈을 계산 할 때 소수점 이하는 버린다.

9. 입력으로 주어지는 숫자의 순서는 변경할 수 없다.

10. 연산 중의 값은 -100,000,000 이상 100,000,000 이하임이 보장된다.
'''
def cal(k, acc, num):
    if k == 0: return acc + num
    elif k == 1: return acc - num
    elif k == 2: return acc * num
    else:
        return int(acc / num)

def search(r, acc):
    global max_value, min_value
    if r == N:  # 모든 수에 대해 연산을 끝냈다면
        max_value = max(max_value, acc)
        min_value = min(min_value, acc)
        return
    for k in range(4):
        if oper[k] >= 1:
            oper[k] -= 1    # 썻으면
            search(r+1, cal(k, acc, numbers[r]))
            oper[k] += 1    # 돌려놓기


T = int(input())

for tc in range(1, T+1):
    N = int(input())
    # + - * / 각 연산자의 개수 (N-1)
    oper = list(map(int, input().split()))
    numbers = list(map(int, input().split()))
    # 어떠한 작업을 진행하면서 비교할 대상
    max_value = -100000000
    min_value = 100000000
    # max_value = float('-inf')
    # min_value = float('inf')
    search(1, numbers[0])
    # 최종 결괏값
    print(f'#{tc} {max_value - min_value}')
    
    
    
    
    
    
    
    
    