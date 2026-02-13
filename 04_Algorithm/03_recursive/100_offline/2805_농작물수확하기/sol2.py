import sys
sys.stdin = open('input.txt')


def get_sum(row, N, arr):
    # 기본 조건: 마지막 행을 넘어갔을 때 0을 반환하며 종료
    if row == N:
        return 0

    # 가운데를 기준으로
    mid = N // 2

    # 유도 부분: 현재 행(row)의 마름모 범위 합 계산

    '''
        가운데 행을 기준으로 상단과 하단의 식이 다르므로
        mid 값을 기준으로 서로 다른 식을 수행
    '''
    if row <= mid:
        # 상단부 및 중앙
        # 범위: 중앙에서 좌우로 row만큼 확장
        start = mid - row
        end = mid + row + 1
    else:
        # 하단부
        # 범위: 아래로 내려갈수록(row가 커질수록) 범위가 줄어듦
        # 역으로 생각하면 (N-1) - row 만큼의 간격임
        gap = (N - 1) - row
        start = mid - gap
        end = mid + gap + 1

    # 이번 행의 총 합은
    current_row_sum = sum(arr[row][start:end])

    # 재귀 호출: 현재 행의 합 + 다음 행(row+1)의 결과
    return current_row_sum + get_sum(row + 1, N, arr)


T = int(input())

for tc in range(1, T + 1):
    N = int(input())
    arr = [list(map(int, input())) for _ in range(N)]

    # 0번 행부터 재귀 시작
    result = get_sum(0, N, arr)

    print(f'#{tc} {result}')