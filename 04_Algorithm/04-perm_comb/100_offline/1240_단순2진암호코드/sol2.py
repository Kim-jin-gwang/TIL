import sys
sys.stdin = open('input.txt')


password = {
    (2, 1, 1): 0,
    (2, 2, 1): 1,
    (1, 2, 2): 2,
    (4, 1, 1): 3,
    (1, 3, 2): 4,
    (2, 3, 1): 5,
    (1, 1, 4): 6,
    (3, 1, 2): 7,
    (2, 1, 3): 8,
    (1, 1, 2): 9
}

def is_valid(numbers):
    odd_num = 0
    even_num = 0
    for i in range(8):
        if i % 2:   # 홀수
            odd_num += numbers[i]
        else:       # 짝수
            even_num += numbers[i]
    # (홀수 자리의 합 x 3) + (짝수 자리의 합)이 10의 배수
    answer = (odd_num * 3) + even_num
    if answer % 10:
        return 0    # 잘못된 경우 0
    else:
        return sum(numbers) # 맞는경우 모든 수의 합


def decryption(arr):
    numbers = []
    # 배열을 뒤집고
    arr.reverse()
    for i in range(0, 56, 7): # 7개씩 건너뛰면서
        # 뒤에서부터 세어나갈 패턴 0으로 초기화
        #  0  1  2  3
        pattern = [0, 0, 0, 0]
        k = 3 # 뒤에서부터
        for idx in range(i, i+7):
            if k % 2 == arr[idx]:   # 현재 패턴 홀짝 여부와 값이 같다면
                pattern[k] += 1     # 해당 위치 패턴 1증가
            else:
                k -= 1              # 다르면 1감소 후
                pattern[k] += 1
        # 하나의 패턴 종료되면 대상 숫자 찾기
        target = password[tuple(pattern[1:])]
        numbers.append(target)

    return is_valid(numbers)

T = int(input())

for tc in range(1, T+1):
    # 세로, 가로: N, M
    N, M = map(int, input().split())
    data = [list(map(int, input())) for _ in range(N)]

    for nums in data:
        # 패턴이 있는경우
        if len(set(nums)) == 2:
            # 마지막 인덱스부터 앞으로 옮겨가면서
            for idx in range(len(nums) - 1, -1, -1):
                if nums[idx]:  # 1을 만나면 패턴 부분만으로 조사시작
                    result = decryption(nums[idx-55:idx+1])
                    break   # 패턴 조사는 한번이면 충분함
            print(f'#{tc} {result}')
            break
