#import sys

#sys.stdin = open("input.txt", "r")

'''
규영이가 이기는 경우와 지는 경우가 총 몇 가지인지 계산

- gy = 규영이의 카드가 담겨있음
- iy = 인영이의 카드가 담겨있음
- gy_win = 규영이의 승리 카운트
- iy_win = 인영이의 승리 카운트
- gy_score = 규영이의 점수
- gy_score = 규영이의 점수

-def start_game(인덱스, 규영이 점수, 인영이 점수)


'''
T = int(input())
for t in range(1,T+1):
    gy = list(map(int, input().split()))  # 규영이 : 카드 내는 순서 고정
    iy = []  # 인영이
    for i in range(1, 19):
        if i not in gy:
            iy.append(i)

    gy_win, iy_win = 0, 0
    visited = [False] * 9

    # 여기부터 코드 작성
    def StartGame(idx, gy_score, iy_score):
        global gy_win, iy_win

        if idx == 9:
            if gy_score > iy_score:
                gy_win += 1
            elif gy_score < iy_score:
                iy_win += 1
            return

        gycard = gy[idx]
        for i in range(9):
            if visited[i]:
                continue
            visited[i] = True
            iycard = iy[i]
            total = gycard + iycard
            if gycard > iycard:
                StartGame(idx+1,gy_score+total,iy_score)
            else:
                StartGame(idx+1, gy_score, iy_score+total)
            visited[i] = False

    StartGame(0,0,0)
    print(f'#{t} {gy_win} {iy_win}')



