import sys
sys.stdin = open("input.txt", "r")

'''
- 1 ~ n까지 번호가 매겨진 n개의 주차 공간 보유
- 차가 주차장에 도착하면 비어있는 주차 공간 있는지 검사
- 빈 공간 있으면 바로 주차 -> 번호가 가장 작은 주차 공간에 주차
- 주차를 기다리는 사람이 여러 대라면 대기장소에서 차례를 기다림

- 주차요금 = 차량의 무게와 주차 공간마다 따로 책정된 단위 무게당 금액을 곱한 가격
-오늘 하루 벌어들일 총 수입 계산

'''

import heapq # (우선순위, 값)
from collections import deque

T = int(input())
for t in range(1,T+1):
    N,M = map(int,input().split())
    
    # 주차 구역 별 단위 무게 당 요금
    Ri = [0]
    for _ in range(N):
        Ri.append(int(input()))
    
    # 차량의 무게
    Wi = [0]
    for _ in range(M):
        Wi.append(int(input()))


    wait = deque()  # 주차장 자리 꽉 차있을 때 차 대기 장소
    ans = 0
    free = list(range(1,N+1))  # 비어있는 주차장 자리 표시(번호표 개념으로 주차하는 차에 하나씩 배부)
    heapq.heapify(free)
    parked = [0] * (M+1)  # 차가 어디에 주차했는지 매핑

    # main code
    for _ in range(M*2):
        car = int(input())
        if car > 0:  # 입차 시
            if free:  # 주차장에 자리가 남으면
                spot = heapq.heappop(free)  # 차가 어디에 주차했는지 매핑
                parked[car] = spot  # ex) 3번 자동차는 1번 스팟에 주차함
                ans += Ri[spot] * Wi[car]  # 가중치 계산
            else:
                wait.append(car)  # 자리 없으면 wait 대기열에 넣음
        
        else:  # 출차 시
            out_car = abs(car)
            spot = parked[out_car]   # ex) 3번 자동차에 배부했던 1번 번호표를 다시 가져옴
            parked[out_car] = 0      # 주차장 자리가 비었다는 것을 표시
            heapq.heappush(free,spot)

            if wait: # 출차한 후 대기열에 차가 있다면
                nxt = wait.popleft()   # 다음 차의 정보를 nxt에 저장
                spot2 = heapq.heappop(free)  # 기다리던 차에 번호표 배부
                parked[nxt] = spot2
                ans += Ri[spot2] * Wi[nxt]
    
    print(f'#{t} {ans}')