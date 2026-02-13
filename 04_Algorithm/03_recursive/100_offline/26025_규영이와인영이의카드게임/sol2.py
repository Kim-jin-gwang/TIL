import sys

sys.stdin = open('input.txt')

# 전역 변수로 관리하여 재귀 함수 내에서 접근 용이하게 설정
kyuyoung_cards = []
inyoung_cards = []
visited = []  # 인영이 카드 사용 여부 체크
win_count = 0
lose_count = 0

# 남은 라운드 수에 따른 팩토리얼 계산을 위한 배열 (미리 계산)
# factorial[n] = n!
factorial = [1, 1, 2, 6, 24, 120, 720, 5040, 40320, 362880]


def play_game_recursive(round_idx, kyu_score, in_score):
    global win_count, lose_count

    # [가지치기] 승패가 이미 결정된 경우 (과반수 86점 초과)
    # 남은 라운드를 진행하지 않아도 결과가 같으므로 남은 경우의 수(n!)를 한 번에 더함
    if kyu_score > 85:
        remaining_rounds = 9 - round_idx
        win_count += factorial[remaining_rounds]
        return

    if in_score > 85:
        remaining_rounds = 9 - round_idx
        lose_count += factorial[remaining_rounds]
        return

    # [기본 조건] 9라운드를 모두 마쳤을 때
    if round_idx == 9:
        if kyu_score > in_score:
            win_count += 1
        else:
            lose_count += 1
        return

    # [유도 부분] 인영이가 낼 카드를 선택하여 다음 라운드로 진행
    '''
        인영이는 남은 카드 중 하나를 낼 수 있음.
        visited 배열을 사용하여 이미 낸 카드는 제외하고 탐색 (순열 생성)
    '''
    for i in range(9):
        if not visited[i]:
            # 선택: 카드 사용 처리
            visited[i] = True

            # 점수 계산 로직
            card_k = kyuyoung_cards[round_idx]
            card_i = inyoung_cards[i]

            next_kyu_score = kyu_score
            next_in_score = in_score

            if card_k > card_i:
                next_kyu_score += (card_k + card_i)
            else:
                next_in_score += (card_k + card_i)

            # 재귀 호출: 다음 라운드(round_idx + 1) 진행
            play_game_recursive(round_idx + 1, next_kyu_score, next_in_score)

            # 복구: 다른 경우의 수를 위해 카드 사용 처리 취소 (백트래킹)
            visited[i] = False


T = int(input())

for tc in range(1, T + 1):
    kyuyoung_cards = list(map(int, input().split()))

    # 인영이 카드 준비 (전체 1~18 중 규영이 카드 제외)
    total_cards = set(range(1, 19))
    inyoung_cards = list(total_cards - set(kyuyoung_cards))
    # 순서대로 탐색하기 위해 정렬 (선택 사항)
    inyoung_cards.sort()

    # 전역 변수 초기화
    visited = [False] * 9
    win_count = 0
    lose_count = 0

    # 0라운드부터 게임 시작 (초기 점수 0 : 0)
    play_game_recursive(0, 0, 0)

    print(f'#{tc} {win_count} {lose_count}')