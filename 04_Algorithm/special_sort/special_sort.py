



T = int(input())
for t in range(1,T+1):
    N = int(input())
    arr = list(map(int,input().split()))
    arr.sort()

    ans = []
    l, r = 0, N-1
    
    while l < r:
        ans.append(arr[r])
        r -= 1

        if l <= r:
            ans.append(arr[l])
            l += 1
        
        if len(ans) >= 10:
            break

    print(f'#{t}', *(ans[:10]))
