import sys
sys.stdin = open('input.txt')

from collections import deque
T = 10
def cycle(que):
    minus = 1
    # 마지막 요소가 0이 될 때까지 반복
    while que[-1] > 0:
        elem = que.popleft() # 왼쪽 요소 꺼내서
        elem = max(elem - minus, 0) # minus만큼 빼주고
        que.append(elem) # 오른쪽 요소에 넣기
        minus = minus % 5 + 1 # minus값 업데이트
    return que


for tc in range(1, T + 1):
    N = int(input())

    num_que = deque(list(map(int, input().split())))

    ans = cycle(num_que)

    print(f'#{tc}', " ".join(map(str, ans)))