import sys
sys.stdin = open('input.txt')


'''헌터
    헌터가 몬스터를 처리하고, 고객이 몬스터가 처리된 것을 확인하면 작업 완료
    몬스터를 처리하는 순서 상관 없음
    고객이 확인하는 순서도 상관없음
    몬스터 처리하자마자 고객에게 확인 시켜야 하는것은 아님 (자유롭게)

    헌터는 1초마다 한칸씩 상하좌우
    몬스터 처리 방법은 몬스터 위치로 이동
    몬스터를 처리하는데 걸리는 시간은 0초
    
    고객이 몬스터 처리 여부를 확인 하는 방법은
    고객에게 헌터가 이동하면 됨
    고객이 몬스터 처리 여부를 확인하는데 드는 시간은 0초

    헌터는 (1, 1)부터 시작
    몬스터와 고객의 위치가 겹치는 경우 없음
    몬스터와 고객이 (1,1) 일수는 있음

    몬스터 위치 고객 위치는 한변의 길이 N이 3이상 10 이하인 정사각형 맵으로 주어짐
    고객및 몬스터의 수 M은 1이상 4 이하
    고객의 번호는 처리해 달라는 몬스터의 번호
    맵에서 몬스터는 양수, 고객은 음수로 주어짐
    그 수의 절대값은 몬스터의 번호 및 고객의 번호를 의미
    0인 경우는 아무것도 없음
    몬스터와 고객이 같은 위치인 경우 없음
    헌터는 상하좌우로 1초에 한 칸씩 움직임
    헌터는 맵의 맨 왼쪽 위인 1,1 부터 시작함

    입력
    T
    N
    N*N 맵정보 (양수는 몬스터 음수는 고객)

    출력
    #tc 최소시간
'''

from itertools import permutations

T = int(input())

for tc in range(1, T+1):
    N = int(input())
    arr = [list(map(int, input().split())) for _ in range(N)]
    # 몬스터와 고객의 위치 저장
    '''
        monster = {번호: (x, y)}
        customer = {번호: (x, y)}
    '''
    monster = {}
    customer = {}
    for i in range(N):
        for j in range(N):
            if arr[i][j] > 0:   # 양수면 몬스터
                monster[arr[i][j]] = (i, j)
            elif arr[i][j] < 0: # 음수면 고객
                customer[-arr[i][j]] = (i, j)

    # 몬스터 번호 리스트
    monster_ids = list(monster.keys())
    # 몬스터 및 고객의 수
    M = len(monster_ids)
    
    # 방문할 모든 위치: 몬스터(양수) + 고객(음수)
    # 양수는 몬스터 번호, 음수는 고객 번호
    # all_targets = [1, 2, 3, -1, -2, -3] 형태로 생성
    all_targets = monster_ids + [-m for m in monster_ids]
    
    # 최소 시간 초기화
    result = float('inf')
    
    # 모든 순열을 탐색
    '''
        순열을 통해 몬스터와 고객을 방문하는 모든 가능한 순서를 생성
        각 순서에 대해 유효한지 확인 (고객이 몬스터가 처리된 것을 확인하는지)
        유효한 순서면 이동 시간을 계산하여 최소 시간 갱신
    '''
    for perm in permutations(all_targets):
        # 고객 방문 전에 해당 몬스터가 처리되었는지 확인
        killed = set()
        valid = True

        for target in perm:
            if target > 0:  # 양수면 몬스터
                killed.add(target)  # 몬스터 처리 완료 표시
            else:  # 음수면 고객
                # 확인하려는 몬스터가 처리목록에 없으면
                if -target not in killed:
                    # 실패
                    valid = False
                    break
        # 유효하지 않은 순서면 다음 순열 탐색
        if not valid: continue
        
        # 유효한 순서면 시간 계산
        time = 0
        # 내 현재위치는 (0, 0)에서 시작
        current = (0, 0)
        for target in perm:
            # target이 양수면 몬스터 위치, 음수면 고객 위치로 이동
            if target > 0:
                pos = monster[target]
            else:
                pos = customer[-target]
            # 이동 시간 계산 (맨해튼 거리)
            time += abs(current[0] - pos[0]) + abs(current[1] - pos[1])
            # 현재 위치 업데이트
            current = pos
        
        # 최소 시간 갱신
        result = min(result, time)

    print(f'#{tc} {result}')

