def comb(arr, n):
   result = []
   if n == 1:
      return [[elem] for elem in arr]
   # 모든 원소에 대해서
   for idx in range(len(arr)):
      elem = arr[idx]   # 이번에 선택한 요소
      # 현재 요소 이후의 나머지 요소들로
      for rest in comb(arr[idx + 1:], n-1):
         result.append([elem] + rest)
   return result


print(comb([1, 2, 3, 4], 2))  # [1, 2, 3], [1, 2, 4], [1, 3, 4], [2, 3, 4] 출력
