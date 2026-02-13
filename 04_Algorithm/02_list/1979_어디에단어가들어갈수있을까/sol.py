import sys
sys.stdin = open('input.txt')


def search_witdh(x, y, K):
    # 조사 시작전 이전 자리가 벽이 아니면 삽입지점 아님
    if 0 <= y - 1 and data[x][y-1] == 1: return False

    # 시작 지점에서 단어 하나 넣었으니 K 1 감소
    k = K-1
    # 아직 단어를 넣어야 하는 동안
    while k:
        y += 1  # 오른쪽으로 한칸 이동
        # 아직 단어 넣을 수 있는지 판별
        if y < N and data[x][y] == 1:
            # 넣을 수 있으니 넣고 다음 조사
            k -= 1
        else:   # 못넣으면
            return False    # 실패 반환
    # 단어를 다 삽입 했는데 여전히 다음 칸이 남았다면 실패
    y += 1
    if y < N and data[x][y] == 1: return False

    return True # 넣었으면 성공 반환

def search_length(x, y, K):
    # 조사 시작전 이전 자리가 벽이 아니면 삽입지점 아님
    if 0 <= x-1 and data[x-1][y] == 1: return False
    # 시작 지점에서 단어 하나 넣었으니 K 1 감소
    k = K-1
    # 아직 단어를 넣어야 하는 동안
    while k:
        x += 1  # 아래로 한칸 이동
        # 아직 단어 넣을 수 있는지 판별
        if x < N and data[x][y] == 1:
            # 넣을 수 있으니 넣고 다음 조사
            k -= 1
        else:   # 못넣으면
            return False    # 실패 반환
    # 단어를 다 삽입 했는데 여전히 다음 칸이 남았다면 실패
    x += 1
    if x < N and data[x][y] == 1: return False

    return True # 넣었으면 성공 반환


T = int(input())

for tc in range(1, T + 1):
    # 가로, 세로 길이 N, 단어의 길이 K
    N, K = map(int, input().split())
    # 단어가 들어갈 수 있는 공간: 1, 없는 공간: 0
    data = [list(map(int, input().split())) for _ in range(N)]

    # 최종 결괏값: K길이 단어가 들어갈 수 있는 공간의 수
    result = 0

    # 기준을 못잡겠다면, 일단 조사 가능한 지점을 모두 찾아서 조사
    for x in range(N):
        for y in range(N):
            if data[x][y] == 1: # (단어를 넣을 수 있는 지점이면 조사 시작)
                # 우선 가로 조사한 결과를 result에 추가
                result += search_witdh(x, y, K)
                # 세로 조사에 대한 결과도 추가
                result += search_length(x, y, K)

    print(f'#{tc} {result}')