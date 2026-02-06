#import sys

#sys.stdin = open("input.txt", "r")

'''
 - 1. 첫번째 값이 다음 값보다 클 때,
    - 3 다음 2가 나올 때, 2의 idx + X가 범위를 벗어나거나 2보나 낮은 경사가 나오먄
      break
    
 - 2. 첫번째 값이 다음 값보다 작을 때,
    
- 경사로 겹침 체크
- 높이 차이가 1보다 큰 경우
- 내리막 경사로를 설치한 구간 건너뛰어야 함
'''
def check(arr,X,N):
    used = [False] * N

    for i in range(N-1):
        if arr[i] == arr[i+1]:    # 값이 같을 때
            continue

        if abs(arr[i] - arr[i+1]) > 1: # 경사로 차이가 1보다 클 때
            return False

        if arr[i] > arr[i+1]:   # 지금 값이 다음 값보다 클 때(내리막)
            for j in range(i+1,i+1+X):
                if j>=N or used[j] or arr[i+1] != arr[j]:
                    return False
                used[j] = True

        elif arr[i] < arr[i+1]:  # 지금 값이 다음 값보다 작을 때(오르막)
            for j in range(i,i-X,-1):
                if j<0 or used[j] or arr[i] != arr[j]:
                    return False
                used[j] = True

    return True

T = int(input())
for t in range(1,T+1):
    N,X = map(int,input().split())
    field = [list(map(int,input().split())) for _ in range(N)]
    ans = 0

    # 행 판별
    for arr in field:
        if check(arr,X,N):
            ans += 1

    # 열 판별
    for a in range(N):
        arr = [field[r][a] for r in range(N)]
        if check(arr,X,N):
            ans += 1

    print(f'#{t} {ans}')

