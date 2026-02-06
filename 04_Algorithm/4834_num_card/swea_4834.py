
import sys
sys.stdin = open("sample_input.txt", "r")

from collections import Counter

T = int(input())
for t in range(1, T+1):
    N = int(input())
    card = input()

    ans = Counter(card).most_common()
    ans = sorted(ans,key=lambda x:(x[1],x[0]))[::-1]
    print(f'#{t} {ans[0][0]} {ans[0][1]}')



