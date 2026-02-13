import sys
sys.stdin = open('input.txt')

T = int(input())

# ragne(n) -> 0 ~ n-1
# range(1, 5) -> (1, 2, 3, 4)
for tc in range(1, T+1):
    N = int(input())  # input -> 항상 문자열
    ai = list(map(int, input().split()))
    # print(ai)
    '''
    # 공백 기준으로 나눠서 새로운 리스트 (요소는 아직 문자열)
    # 모든 요소를 정수 형태로 바꿀려면? 반복문으로 순회해서 변환
    # ai = input().split()
    # for idx in range(len(ai)):
    #     ai[idx] = int(ai[idx])
    # print(ai)
    '''

    # 최종 결괏값
    max_value = ai[0]
    min_value = ai[0]
    # 전체 순회
    # for num in ai:
    #     # print(num)
    #     if max_value < num:
    #         max_value = num
    #     if min_value > num:
    #         min_value = num
    # print(max_value)

    # 코드 개선
    # for idx in range(1, N):
    #     if max_value < ai[idx]:
    #         max_value = ai[idx]
    #     if min_value > ai[idx]:
    #         min_value = ai[idx]
    #
    # result = max_value - min_value
    # print(f'#{tc} {result}')
    # pythonic
    print(f'#{tc} {max(ai) - min(ai)}')


'''
N개의 양의 정수에서 가장 큰 수와 가장 작은 수의 차이를 출력하시오.
[입력]
첫 줄에 테스트 케이스의 수 T가 주어진다. ( 1 ≤ T ≤ 50 )
각 케이스의 첫 줄에 양수의 개수 N이 주어진다. ( 5 ≤ N ≤ 1000 )
다음 줄에 N개의 양수 ai가 주어진다. ( 1 ≤ ai≤ 1000000 )
[출력]
각 줄마다 "#T" (T는 테스트 케이스 번호)를 출력한 뒤, 답을 출력한다.
#1 124
#2 567
'''