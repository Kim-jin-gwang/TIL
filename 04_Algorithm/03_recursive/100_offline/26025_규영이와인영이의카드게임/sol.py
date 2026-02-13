import sys
from itertools import permutations


sys.stdin = open('input.txt')

T = int(input())

for tc in range(1, T + 1):
    # 규영이의 카드 입력 (순서 고정)
    kyuyoung_cards = list(map(int, input().split()))

    # 전체 카드(1~18) 중 규영이 카드를 제외한 나머지가 인영이의 카드
    total_cards = set(range(1, 19))
    inyoung_cards = list(total_cards - set(kyuyoung_cards))

    # 정렬을 해두면 순열 생성 시 디버깅이 편함 (필수는 아님)
    inyoung_cards.sort()

    win_count = 0
    lose_count = 0

    # 인영이 카드의 모든 순열(9!가지) 생성
    for inyoung_perm in permutations(inyoung_cards):
        kyu_score = 0
        in_score = 0

        # 9라운드 게임 진행
        for i in range(9):
            card_k = kyuyoung_cards[i]
            card_i = inyoung_perm[i]

            if card_k > card_i:
                kyu_score += (card_k + card_i)
            else:
                in_score += (card_k + card_i)

        # 총점 비교 후 승패 카운트
        if kyu_score > in_score:
            win_count += 1
        elif kyu_score < in_score:
            lose_count += 1

    print(f'#{tc} {win_count} {lose_count}')
