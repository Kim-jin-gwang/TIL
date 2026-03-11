




T = int(input())
for t in range(1,T+1):
    str1 = input()
    str2 = input()

    tmp = str2.find(str1)
    ans = 0 if tmp == -1 else 1
    print(f'#{t} {ans}')