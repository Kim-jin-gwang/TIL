import sys
import math

sys.stdin = open("input.txt", "r")

check_oper = ['+','-','/','*']

def cal_oper(a, b, op):
    if op == '+':
        return a+b
    elif op == '-':
        return a-b
    elif op == '*':
        return a*b
    elif op == '/':
        return a/b

def cal_tree(n):
    if n<=N:
        if tree[n][0] in check_oper:
            oper = tree[n][0]
            a = cal_tree(tree[n][1])
            b = cal_tree(tree[n][2])
            tree[n][0] = cal_oper(a,b,oper)
            return tree[n][0]
        else:
            return tree[n][0]


for t in range(1,11):
    N = int(input())
    tree = [[0,0,0] for _ in range(N+1)]  # [값, 왼쪽 자식, 오른쪽 자식]

    for _ in range(N):
        parts = input().split()
        idx = int(parts[0])
        if parts[1] in check_oper:
            tree[idx] = [parts[1],int(parts[2]),int(parts[3])]
        else:
            tree[idx] = [int(parts[1]),0,0]

    cal_tree(1)
    print(f'#{t} {math.floor(tree[1][0])}')
