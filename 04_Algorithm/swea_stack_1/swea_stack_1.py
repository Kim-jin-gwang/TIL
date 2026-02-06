import sys

sys.stdin = open("input.txt", "r")

'''
- p가 ( 일 때
    - stack.append()

- p가 )일 때
    - stack[-1]의 값이 ( 이면 레이저이므로 cnt만큼 ans에 append
    - stack[-1]의 값이 ) 이면 파이프 하나가 닫힌 경우이므로 cnt-1

- cnt는 언제 + 해주지?
    - (일 때 +해주고, 레이저일 경우, cnt를 ans에 더하기 전에 -한번 해주기

- 파이프가 닫힐 때 꼬다리 하나 ans에 더해주기
'''

T = int(input())
for t in range(1,T+1):
    pipe = list(input())
    ans, cnt = 0, 0
    stack = []
    before = ''

    for p in pipe:
        # p가 (일 때
        if p == '(':
            stack.append(p)
            cnt += 1

        # p가 )일 떄
        elif p == ')':

            if before == '(':     # 레이저일 경우
                cnt -= 1
                ans += cnt
                stack.pop()

            elif before == ')':   # 파이프가 닫히는 경우
                cnt -= 1
                ans += 1
                stack.pop()

        before = p

    print(f'#{t} {ans}')