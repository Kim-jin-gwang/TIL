import sys
sys.stdin = open('input.txt')

def dfs(honey_idx, honey_benefit, honey_sum, x, y):
    """
    DFS를 이용해 M개의 연속된 벌통에서 C 이하의 꿀로 최대 수익을 구하는 함수
    
    Args:
        honey_idx (int): 현재 확인 중인 벌통의 인덱스 (0~M-1)
        honey_benefit (int): 현재까지 얻은 수익 (꿀^2의 합)
        honey_sum (int): 현재까지 선택한 꿀의 총량
        x (int): 시작 행 위치
        y (int): 시작 열 위치
    """
    global part_sum

    # 가지치기: C를 넘으면 더 이상 진행하지 않음
    if honey_sum > C:
        return

    # 꿀의 인덱스가 M에 도달하면 최대값 갱신 후 종료
    if honey_idx == M:
        part_sum = max(part_sum, honey_benefit)
        return

    cnt_benefit = data[x][y + honey_idx] ** 2
    cnt_sum = data[x][y + honey_idx]
    # 부분집합을 구하는 방식으로 진행
    # 현재 꿀을 선택하는 경우
    dfs(honey_idx + 1, honey_benefit + cnt_benefit, honey_sum + cnt_sum, x, y)
    # 현재 꿀을 선택하지 않는 경우
    dfs(honey_idx + 1, honey_benefit, honey_sum, x, y)

T = int(input())
for tc in range(1, T + 1):
    # N: 벌통 크기, M: 벌통의 개수, C: 꿀을 채취할 수 있는 최대 양
    N, M, C = map(int, input().split())
    data = [list(map(int, input().split())) for _ in range(N)]
    result = 0  # 총 수익을 저장할 변수

    # 부분집합을 구해서 최대 이익을 구하는 부분을 DFS로 구현
    # DFS의 장점: C를 넘는 경우 가지치기로 경우의 수를 줄일 수 있음
    for i in range(N):
        for j in range(N - M + 1):
            part_sum = 0  # DFS를 통해 얻은 최대 이익을 저장할 변수
            dfs(0, 0, 0, i, j)
            fst_max = part_sum

            # 두 번째 벌통 구간을 찾기 위한 순회
            # k, l은 첫 번째 구간과 겹치지 않는 위치를 찾음
            for k in range(i, N):  # 첫 번째 구간의 행(i) 이후부터 탐색
                for l in range(0, N - M + 1):
                    # 같은 행에서는 첫 번째 구간과 겹치지 않도록 체크
                    if i == k and l < j + M:
                        continue
                    part_sum = 0
                    dfs(0, 0, 0, k, l)
                    snd_max = part_sum
                    result = max(result, fst_max + snd_max)

    print(f"#{tc} {result}")
