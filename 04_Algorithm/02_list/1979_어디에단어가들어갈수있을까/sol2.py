import sys
sys.stdin = open('input.txt')


# 함수 하나로 통일
def count_word_slots(line, K):
    # 한 줄(가로/세로)에서 연속된 1의 길이를 세며 K와 정확히 일치하는 구간만 카운트
    count = 0
    length = 0

    for value in line:
        if value == 1:
            length += 1
        else:
            if length == K:
                count += 1
            length = 0

    # 줄 끝이 1로 끝나는 경우 처리
    if length == K:
        count += 1

    return count


T = int(input())

for tc in range(1, T + 1):
    # 가로, 세로 길이 N, 단어의 길이 K
    N, K = map(int, input().split())
    # 단어가 들어갈 수 있는 공간: 1, 없는 공간: 0
    data = [list(map(int, input().split())) for _ in range(N)]

    # 최종 결괏값: K길이 단어가 들어갈 수 있는 공간의 수
    result = 0

    # 각 조사를 별도의 반복문으로 분리하고, 필요한 부분에 대해서만 조사 시작

    # 가로 방향 조사
    for row in data:
        result += count_word_slots(row, K)

    # 세로 방향 조사
    for col in range(N):
        column = [data[row][col] for row in range(N)]
        result += count_word_slots(column, K)

    print(f'#{tc} {result}')