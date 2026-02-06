#import sys
from collections import deque

#sys.stdin = open("input.txt", "r")

for _ in range(10):
    T = int(input())
    pw = deque(map(int,input().split()))
    cnt = 1

    while True:
        if pw[-1] <= 0:
            pw[-1] = 0
            break

        pw.append(pw.popleft()-cnt)
        cnt+=1
        if cnt >5:
            cnt = 1

    ans = pw
    print(f'#{T}',*ans)