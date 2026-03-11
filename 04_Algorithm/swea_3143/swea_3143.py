



T = int(input())
for t in range(1,T+1):
    str1, str2 = input().split()

    cnt = str1.count(str2)
    ans = cnt + (len(str1) - len(str2) * cnt)
    print(f'#{t} {ans}')