



T = int(input())
for t in range(1,T+1):
    str1 = input()
    str2 = input()

    ans = 0
    for s in str1:
        ans = max(ans, str2.count(s))
    
    print(f'#{t} {ans}')