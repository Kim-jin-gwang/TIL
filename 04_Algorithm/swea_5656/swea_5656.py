import sys
sys.stdin = open("input.txt", "r")

'''
- 0은 빈 공간, 그 외의 숫자는 벽돌임
- 게임 규칙
    - 구슬은 좌 우 로만 움직일 수 있어, 항상 맨 위에 있는 벽돌만 깨트릴 수 있음
    - 벽돌은 숫자 1~9로 표현되며, 구슬이 명중한 벽은 상하좌우로 (벽돌에 적힌숫자 - 1) 칸 만큼 같이 제거됨
- N개의 벽돌을 떨어뜨려 최대한 많은 벽돌을 제거하려 할 때, 남은 벽돌의 개수를 구하라


[제약 사항]
1. 1 ≤ N ≤ 4
2. 2 ≤ W ≤ 12
3. 2 ≤ H ≤ 15


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
from collections import deque

dx = [1,-1,0,0]
dy = [0,0,1,-1]

# 중복순열
# 모든 순열에 대해 구슬을 떨어뜨리고 복사한 맵에서 시뮬레이션하기
def go_permu(idx):
    global ans

    if ans == 0:
        return

    if idx == N:
        copy_field = [row[:] for row in field]
        drop_ball(copy_field, selected)

        remain = cnt_block(copy_field)
        ans = min(ans, remain)
        return
    
    for col in range(W):
        selected[idx] = col
        go_permu(idx+1)

# 구슬 떨어뜨리기
def drop_ball(board, selected_cols):
    for col in selected_cols:
        for row in range(H):
            if board[row][col] != 0:
                explode(board, row, col)
                break
        gravity(board)


# 연쇄 반응 해결
def explode(board, row, col):
    queue = deque()
    queue.append((row,col, board[row][col]))

    while queue:
        r,c,power = queue.popleft()

        if board[r][c] == 0:
            continue

        board[r][c] = 0

        for i in range(4):
            for dist in range(1,power):
                nr = r + dx[i] * dist
                nc = c + dy[i] * dist

                if not (0 <= nr < H and 0 <= nc < W):
                    break
                
                if board[nr][nc] != 0:
                    queue.append((nr, nc, board[nr][nc]))
                    


# 중력 처리
def gravity(board):

    for c in range(W):
        tmp = []
        for r in range(H-1,-1,-1):
            if board[r][c] != 0:
                tmp.append(board[r][c])

        for r in range(H-1,-1,-1):
            if tmp:
                board[r][c] = tmp.pop(0)
            else:
                board[r][c] = 0


# 남은 벽돌 세기
def cnt_block(board):
    cnt = 0
    for i in range(H):
        for j in range(W):
            if board[i][j] != 0:
                cnt += 1
    
    return cnt


T = int(input())
for t in range(1,T+1):
    N, W, H = map(int,input().split())      # 구슬을 쏘는 횟수, W * H 배열로 주어짐
    field = [list(map(int,input().split())) for _ in range(H)]
    ans = float('inf')
    selected = [0] * N

    go_permu(0)
    print(f'#{t} {ans}')