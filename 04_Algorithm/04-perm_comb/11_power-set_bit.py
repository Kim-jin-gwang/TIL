arr = [1, 2, 3]
subsets = []

# 모든 경우의수를 모두 볼것이다.
# for i in range(2**len(arr)):
for i in range(1 << len(arr)):
    # print(i) # 모든 경우의 수 중, i번째경우
    subset = []
    # 내가 가진 N개의 원소에 대해서
    # j번째 요소가 이번 경우의 수에 포함되느냐
    for j in range(len(arr)):
        if i & (1 << j):
            subset.append(arr[j])
    subsets.append(subset)

print(subsets)
