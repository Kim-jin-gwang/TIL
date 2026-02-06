import sys
sys.stdin = open("input.txt", "r")


'''
 - 카드를 이용해 수식 계산했을 때의 결과 중 최대-최소 출력

 - oper = [+,-,*,/] 순으로 개수가 있음
 - 연산자의 우선순위는 고려하지 않고 왼쪽에서 오른쪽으로 차례대로 계산
 - 숫자는 고정이고 연산자만 숫자 사이사이에 끼워서 계산함


 - 중복방지는 used를 사용
    - [+ + *] 일 때, 0번 +와 1번 +는 시작점이 같으므로 중복임, 
    - 이 상황을 방지하기 위해 각각의 depth에서 한번 사용했던 연산은 무시하고 넘어감
'''

def cal_oper(a, b, op):
    if op == '+':
        return a+b
    elif op == '-':
        return a-b
    elif op == '*':
        return a*b
    elif op == '/':
        return int(a/b)


def dfs(idx, val, oper, expr, visited):
    global max_ans, min_ans
    used = set()    # used를 사용해서 방문한 곳을 또 방문하는 중복 상황 방지

    if idx == N:
        max_ans = max(max_ans, val)
        min_ans = min(min_ans, val)
        return

    for i in range(len(oper)):
        if visited[i]:
            continue
        if oper[i] in used:
            continue
        used.add(oper[i])

        visited[i] = True
        nval = cal_oper(val, expr[idx], oper[i])
        dfs(idx+1, nval, oper, expr,visited)
        visited[i] = False


T = int(input())
for t in range(1,T+1):
    symbols = ['+', '-', '*', '/']

    N = int(input())
    oper_num = list(map(int,input().split()))  # 수식으로 바꾸기 전 숫자인 단계
    oper = []  # 바꾼 수식은 여기에 담김 ex) ['+', '+', '+', '+', '-']
    for cnt, symbol in zip(oper_num, symbols):
        oper.extend([symbol] * cnt)
    expr = list(map(int,input().split())) #  숫자 배열 담김

    max_ans = -100000000
    min_ans = 100000000
    visited = [False] * (len(oper))
    dfs(1,expr[0],oper,expr,visited)

    ans = max_ans - min_ans
    print(f'#{t} {ans}')

