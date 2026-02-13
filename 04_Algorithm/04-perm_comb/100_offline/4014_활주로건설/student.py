'''
하나의 블럭에 대해 경사로 건설 가능 여부를 판단하는 함수(check)를 만들
면 arr와 arr[::-1]를 check 함수를 통해 검사함으로써 하나의 arr 블럭
이 경사로 건설에 문제가 없는지 판단할 수 있다.

가로, 세로 두 방향에 대한 검증이 필요하다는 부분도 NxN 크기의 활주로를
Transpose해서 각 행에 대해 활주로 건설 가능 여부를 check 함수를 통해
검증하면 세로 방향에 대한 검증을 진행할 수 있다.
'''
import sys
sys.stdin = open('input.txt')

T = int(input())

def check_downstair(arr, visited):
    for idx in range(0, N - 1):
        # 1칸 내려가는 경우
        if arr[idx] - arr[idx + 1] == 1:
            # 남은 칸이 경사로 길이에 비해 모자라는 경우 경사로 설치 불가능
            if N - idx - 1 < X:
                return False
            # 현재 칸 이후로 X칸만큼의 공간에 경사로가 존재하지 않고 평탄한 경우 경사로 놓기
            elif not any(visited[idx + 1: idx + X + 1]) and arr[idx + 1: idx + X + 1] == [arr[idx + 1]] * X:
                visited[idx + 1: idx + X + 1] = [True] * X
            # 그 외에 경우에는 모두 경사로 설치 불가능
            else:
                return False
        # 2칸 이상 내려가는 경우에는 경사로 설치 불가능
        elif arr[idx] - arr[idx + 1] > 1:
            return False
    return True



for tc in range(1, T + 1):
    # 지도 한 변의 크기, 경사로의 길이
    N, X = map(int, input().split())

    # 원본 지도 입력
    matrix = [list(map(int, input().split())) for _ in range(N)]

    # 세로 방향에 대한 검증을 위해 원본 지도 transpose
    transposed_matrix = list(map(list, zip(*matrix)))
    '''
      원본         변환 후
    [1, 2, 3]    [1, 4, 7]
    [4, 5, 6] -> [2, 5, 8]
    [7, 8, 9]    [3, 6, 9]
    '''

    ans = 0
    # 원본 지도의 행을 순회하며 경사로 건설 가능성 검증
    for mat in (matrix, transposed_matrix):
        for row in mat:
            # 경사로 설치 여부 판단을 위한 visited 배열
            visited = [False] * len(row)

            # 해당 행에 문제가 없으면 True return 및 ans += 1
            # 정방향 체크
            if not check_downstair(row, visited):
                continue
            # 역방향 체크
            if not check_downstair(row[::-1], visited[::-1]):
                continue
            # 해당 행 문제 없으므로 ans += 1
            ans += 1

    print(f"#{tc} {ans}")