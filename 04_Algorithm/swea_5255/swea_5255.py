import sys
sys.stdin = open("input.txt", "r")

'''
1. 마지막에 2*1 타일을 놓는 경우
2. 마지막에 2*2 타일을 놓는 경우 (가로, 세로 하나씩)
3. 마지막에 2*3 타일을 놓는 경우

'''

T = int(input())
for t in range(1,T+1):
    N = int(input())
    arr = [0] * (N+1)
    arr[0] = 1
    arr[1] = 1
    arr[2] = 3

    for i in range(3,N+1):
        arr[i] = arr[i-1] + 2*arr[i-2] + arr[i-3]
    
    print(f'#{t} {arr[-1]}')
    