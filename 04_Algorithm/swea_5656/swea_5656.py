import sys
sys.stdin = open("input.txt", "r")

'''
- 0은 빈 공간, 그 외의 숫자는 벽돌임
- 게임 규칙
    - 구슬은 좌 우 로만 움직일 수 있어, 항상 맨 위에 있는 벽돌만 깨트릴 수 있음
    - 벽돌은 숫자 1~9로 표현되며, 구슬이 명중한 벽은 상하좌우로 (벽돌에 적힌숫자 - 1) 칸 만큼 같이 제거됨
- N개의 벽돌을 떨어뜨려 최대한 많은 벽돌을 제거하려 할 때, 남은 벽돌의 개수를 구하라


- 완전탐색으로 각 열마다 실행
- 공이 떨어진 후
    - 공에 새겨진 숫자만큼 터트리기
    - 터진 벽돌의 연쇄반응 해결하기
    - 다 터진 후 벽돌 내리기
    - 리턴은 남은 벽돌의 개수

1. 재귀를 이용한 중복순열 구현
2. 블록이 연쇄적으로 파괴되는 함수 구현
3. 폭파로 생긴 공백을 채우는 함수 구현
4. 잔여 블록을 계산하는 함수 구현

'''

dx = [1,-1,0,0]
dy = [0,0,1,-1]

def Search(col, H, field):

    for i in range(H):
        # 0일때는 넘어가기
        if field[i][col] == 0:
            continue

        # 1일때는 안넘어가기
        if field[i][col] == 1:
            field[i][col] = 0
            continue

        block = field[i][col]





T = int(input())
for t in range(1,T+1):
    N, W, H = map(int,input().split())      # 구슬을 쏘는 횟수, W * H 배열로 주어짐
    field = [list(map(int,input().split())) for _ in range(H)]

    ans = 0
    for i in range(W):
        ans = Search(i,H)