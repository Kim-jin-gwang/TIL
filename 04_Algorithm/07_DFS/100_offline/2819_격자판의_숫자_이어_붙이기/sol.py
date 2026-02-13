import sys
sys.stdin = open('input.txt')

# 동서남북 네 방향으로 인접한 격자
# 상 하 좌 우
dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]

# 총 여섯 번 이동하면서
# 이번 경우에 x, y 좌표에서부터 총 6번 이동!
# 각 칸에 적혀있는 숫자를 차례대로 이어 붙이면 7자리의 수가 된다.
def search(x, y, r, acc):
    global count
    count += 1
    # 종료를 언제 하나?
    if len(acc) == 7:
        # 할 일?
        result.add(acc)
        return
    for k in range(4):
        nx = x + dx[k]
        ny = y + dy[k]
        if 0 <= nx < 4 and 0 <= ny < 4:
            search(nx, ny, r+1, acc + data[nx][ny])





T = int(input())
for tc in range(1, T+1):
    # 연산이 필요한게 아닌데 정수로 만들 이유가 없다!
    data = [input().split() for _ in range(4)]
    # 최종 결괏값 -> 그렇게 만들어진 중복 없는 수열의 개수
    result = set()
    count = 0
    # 격자판의 임의의 위치에서 시작해서,
    # 아, 모든 좌표에 대해서 다 조사
    for x in range(4):
        for y in range(4):
            # 조사
            search(x, y, 0, data[x][y])
    print(count)
    print(f'#{tc} {len(result)}')
