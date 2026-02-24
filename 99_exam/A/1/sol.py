import sys
sys.stdin = open('input.txt')

'''
[학교 졸업]

N개 필수 과목
1번부터 N개
한 학기 모든 과목 이수

각 과목에는 선수 과목이 있음
이전 학기에 해당 선수 과목을 들은적 없으면 안됨

첫 학기에는 선수과목 수행 없음
선수과목을 이전학기에 완료하면 이번학기에 해당 과목 완료

선수과목이 없으면 첫 학기에 완료
모든 학기를 완료하는데 필요한 총 학기는?
유방향 그래프
4 3
3 2
3 1

과목수 N 1 이상 100이하
과목들의 선수과목의 총 합은 1이상 120이하
선수과목의 수가 0인 과목이 하나도 없을 수도 있다 (사이클?)

입력
T
N
N 줄에 걸쳐 각 과목의 선수 과목번호
선수과목 개수, 과목 번호 번호 번호
'''

T = int(input())

for tc in range(1, T+1):
    N = int(input())
    # 인접 행렬
    adj_matrix = [[0] * (N+1) for _ in range(N+1)]
    # 각 과목의 선수과목 수
    degree = {idx: 0 for idx in range(1, N+1)}

    for idx in range(1, N+1):
        nums = list(map(int, input().split()))
        # nums[0]은 선수과목의 수, nums[1:]는 선수과목 번호
        for num in nums[1:]:
            if num:
                adj_matrix[idx][num] = 1
        degree[idx] = nums[0]

    result = 0  # 총 학기 수

    # 선수과목이 남아있는 과목이 있는 동안 반복
    while degree:
        # 이번 학기에 수강할 수 있는 과목들
        can_take = [idx for idx, deg in degree.items() if deg == 0]
        # 이번 학기에 수강할 과목이 없다면 사이클이 존재하는 것
        if not can_take:
            result = -1
            break

        # 이번 학기에 수강할 과목들을 제거하고, 
        # 다음 학기에 영향을 주는 과목들의 선수과목 수를 감소
        for course in can_take:
            del degree[course]  # 이번 학기에 수강한 과목 제거

            # course가 선수과목인 과목들의 선수과목 수 감소
            for next_course in range(1, N+1):

                # course가 next_course의 선수과목인 경우
                if adj_matrix[next_course][course] == 1:  

                    # degree에 next_course가 존재하는지 확인
                    if next_course in degree:
                        degree[next_course] -= 1    # next_course의 선수과목 수 감소
        
        result += 1  # 한 학기 추가
    print(f'#{tc} {result}')

