#import sys

#sys.stdin = open("input.txt", "r")

T = int(input())
for t in range(1,T+1):
    N, K = map(int,input().split())
    arr = [list(map(int,input().split())) for _ in range(N)]
    ans = 0

    # 1. arr[x][y]가 0인지 확인
    # 2. 오른쪽, 아래쪽으로 순회해서 공간이 K개 인지 확인
    # 3. 그 전이나 후에 더 공간이 있으면 break

    for x in range(N):
        for y in range(N):
            if arr[x][y] == 0:
                continue

            flag_y = True

            #arr[x][i]
            for i in range(y, y+K):
                if 0<=i<N:
                    if arr[x][i] == 0:
                        flag_y = False
                else:
                    flag_y = False
                    break

            if y+K < N:
                if arr[x][y+K] == 1:
                    flag_y = False

            if y-1 >= 0:
                if arr[x][y-1] == 1:
                    flag_y = False

            if flag_y:
                ans += 1

            flag_x = True

            # arr[j][y]
            for j in range(x, x + K):
                if 0<=j<N:
                    if arr[j][y] == 0:
                        flag_x = False
                else:
                    flag_x = False
                    break

            if x+K < N:
                if arr[x+K][y] == 1:
                    flag_x = False

            if x-1 >= 0:
                if arr[x-1][y] == 1:
                    flag_x = False

            if flag_x:
                ans += 1

    print(f'#{t} {ans}')





