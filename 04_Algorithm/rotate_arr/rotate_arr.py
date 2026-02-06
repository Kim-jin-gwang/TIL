#import sys

#sys.stdin = open("input.txt", "r")


T = int(input())
for t in range(1,T+1):
    N = int(input())
    arr = [list(input().split()) for _ in range(N)]
    ans = [[''for _ in range(N)] for _ in range(N)]
    ans_idx = 0

    #90
    for i in range(N):
        tmp = ''
        for j in range(N-1,-1,-1):
            tmp += arr[j][i]
        ans[i][ans_idx] = tmp
    ans_idx += 1


    #180
    for i in range(N-1,-1,-1):
        tmp = ''
        for j in range(N-1,-1,-1):
            tmp += arr[i][j]
        ans[N-1-i][ans_idx] = tmp
    ans_idx += 1


    #270
    for i in range(N-1,-1,-1):
        tmp=''
        for j in range(N):
            tmp += arr[j][i]
        ans[N-1-i][ans_idx] = tmp

    print(f'#{t}')
    for a in ans:
        print(' '.join(a))


