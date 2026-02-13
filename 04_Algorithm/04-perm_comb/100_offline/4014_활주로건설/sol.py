import sys

sys.stdin = open('input.txt')

"""
한 줄(행/열)에 활주로를 설치할 수 있는지 확인하는 함수로 풀이한다.
1) 현재 칸과 다음 칸의 높이 차이를 본다.
2) 차이가 0이면 계속 진행
3) 차이가 2 이상이면 바로 실패
4) 차이가 1이면 경사로 길이 X만큼 평평한 구간이 있는지 체크
   - 높아지는 경우: 현재 칸 기준으로 뒤쪽 체크
   - 낮아지는 경우: 다음 칸 기준으로 앞쪽 체크
   - 경사로가 겹치지 않도록 방문 배열 사용
"""
def can_build(line, n, x):
    used = [0] * n  # 경사로가 이미 설치된 위치 표시

    for i in range(n - 1):
        diff = line[i] - line[i + 1]

        if diff == 0:
            continue

        if abs(diff) >= 2:
            return False

        # 낮아지는 경우: i+1 기준으로 앞으로 x칸
        if diff == 1:
            for j in range(i + 1, i + 1 + x):
                if j >= n or line[j] != line[i + 1] or used[j]:
                    return False
                used[j] = 1

        # 높아지는 경우: i 기준으로 뒤로 x칸
        elif diff == -1:
            for j in range(i, i - x, -1):
                if j < 0 or line[j] != line[i] or used[j]:
                    return False
                used[j] = 1

    return True


T = int(input())
for tc in range(1, T + 1):
    n, x = map(int, input().split())
    board = [list(map(int, input().split())) for _ in range(n)]

    cnt = 0
    for row in board:
        if can_build(row, n, x):
            cnt += 1

    # 열 검사: 전치해서 행처럼 처리
    for col in zip(*board):
        if can_build(list(col), n, x):
            cnt += 1

    print(f'#{tc} {cnt}')
