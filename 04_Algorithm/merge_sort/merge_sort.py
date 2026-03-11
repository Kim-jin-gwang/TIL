


def merge_sort(arr):
    global ans
    n = len(arr)
    
    if n <= 1:
        return arr
    
    mid = n//2
    left = arr[:mid]
    right = arr[mid:]

    left = merge_sort(left)
    right = merge_sort(right)

    if left[-1] > right[-1]:
        ans += 1


    return merge(left, right)


def merge(left, right):
    res = []
    i,j = 0,0
    

    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            res.append(left[i])
            i+=1
        else:
            res.append(right[j])
            j+=1
    
    res.extend(left[i:])
    res.extend(right[j:])

    return res


T = int(input())
for t in range(1,T+1):
    N = int(input())
    arr = list(map(int,input().split()))

    ans = 0
    res = merge_sort(arr)

    print(f'#{t} {res[N//2]} {ans}')
