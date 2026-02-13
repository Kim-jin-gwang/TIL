import sys
sys.stdin = open('input.txt')


def calc_taste(team, table):
    # 팀 내부의 시너지 합 계산
    total = 0
    for i in range(len(team)):
        for j in range(i + 1, len(team)):
            a = team[i]
            b = team[j]
            total += table[a][b] + table[b][a]
    return total


def choose(idx, depth):
    global result

    '''
        재귀 흐름
        1. idx 번째 재료를 팀 A에 넣을지 말지 결정한다.
        2. 팀 A 인원이 N//2가 되면 팀 B는 나머지 재료로 자동 결정된다.
        3. 두 팀의 시너지 차이를 계산해서 최소값을 갱신한다.
    '''
    if depth == N // 2:
        team_a = selected[:]
        team_b = []
        for i in range(N):
            if not picked[i]:
                team_b.append(i)

        taste_a = calc_taste(team_a, data)
        taste_b = calc_taste(team_b, data)
        diff = abs(taste_a - taste_b)
        if diff < result:
            result = diff
        return

    # 끝까지 봤는데 인원이 덜 찼으면 종료
    if idx == N:
        return

    # 현재 재료를 팀 A에 넣는 경우
    picked[idx] = 1
    selected.append(idx)
    choose(idx + 1, depth + 1)
    selected.pop()
    picked[idx] = 0

    # 현재 재료를 팀 A에 넣지 않는 경우
    choose(idx + 1, depth)


T = int(input())

for tc in range(1, T + 1):
    N = int(input())
    data = [list(map(int, input().split())) for _ in range(N)]

    '''
        목표
        - 재료를 N//2개씩 두 팀으로 나눌 때
          두 팀의 시너지 차이를 최소화한다.

        방법
        - 재귀로 팀 A를 구성한다.
        - 팀 B는 팀 A에 포함되지 않은 재료로 만든다.
    '''
    result = sum(sum(data, []))

    # picked: 팀 A 여부, selected: 팀 A 목록
    picked = [0] * N
    selected = []

    # 0번째부터 차례대로 고르는 재귀
    choose(0, 0)

    print(f'#{tc} {result}')
