import sys

sys.stdin = open("input.txt", "r")

'''
- 접수 창구에서 고장 접수 후 정비 창구에서 차량 정비
- 차량 정비가 끝나면 고객만족도 조사
- 각각의 창구로 가는 시간은 무시
- ★지갑을 분실한 고객과 같은 접수 창구와 정비창구를 이용한 고객번호를 찾아
    그 합을 출력
- 고객이 없는 경우 -1 출력
 

- 접수 창구
    - 빈 접수 창구에 가서 고장 접수
    - 빈 접수 창구가 없으면 생길 때까지 기다림
    - 여러 고객이 기다리고 있는 경우 고객번호가 낮은 순서대로 우선 접수
    - 빈 창구가 여러 곳인 경우 창구번호가 작은 곳으로 감
    

- 정비 창구
    - 빈 정비 창구가 있는 경우 가서 정비
    - 빈 정비 창구가 없으면 생길 때까지 기다림
    - 먼저 기다리는 고객 우선
    - 두 명 이상의 고객들이 접수 창구에서 동시에 접수를 완료하고 정비 창구로
      이동한 경우, 이용했던 접수 창구번호가 작은 고객이 우선
    - 빈 창구가 여러 곳인 경우 창구번호가 작은 곳으로 감
    

- 생각
    - 창구 번호는 인덱스
    - queue를 사용?
    - 반복문을 돌며 A와 B 창구를 이용한 고객 찾기
    - 정비창구 이용하는 함수
    - 접수창구 이용하는 함수
    - 먼저 해야할 것 : 고객 정보가 있는 tk에서 하나씩 꺼내 접수 창구로 보내기
    - 몇번째 사람인지도 확인해야하는데? -> 어떻게 하지
    
    - GPT와 함께라면 어떤 문제든 풀 수 있지
'''

from collections import deque
import heapq  # 안에 있는 데이터를 하나하나 비교


T = int(input())
for t in range(1,T+1):
    # 접수 창구 개수, 정비 창구 개수, 방문 고객 수,
    # 지갑을 두고 간 고객이 이용한 접수 창구번호와 정비 창구번호(A,B)
    N, M, K, A, B = map(int,input().split())
    ai = list(map(int,input().split()))     # i번째 접수 창구가 고장을 접수하는 데 걸리는 시간
    bi = list(map(int, input().split()))    # j번째 정비 창구가 차량을 정비하는 데 걸리는 시간
    tk = list(map(int, input().split()))    # k번째 고객이 차량 정비소를 방문하는 시간
    time = 0

    recept_wait = deque()       # 접수 대기 큐(고객 번호만 넣음)
    repair_wait = []            # 정비 대기 큐(접수 완료 시간, 창구 번호, 고객 번호)
    recept_desk = [None] * N    # 창구별 (현재 고객 번호, 남은 시간)
    repair_desk = [None] * M    # 창구별 [현재 고객, 남은 시간]
    done_repair = []            # 정비가 끝난 사람들 모음

    used_recept = [0] * (K + 1)
    used_repair = [0] * (K + 1)


    while len(done_repair) < K:
        # 도착 고객 접수 대기열에 넣음
        for i in range(K):
            if tk[i] == time:
                recept_wait.append(i+1) # 1 2 3 4 ...

        # 창구가 꽉 차있으면 남은 시간 줄이고, 시간 0이면 repair_wait으로 이동
        for i in range(N):
            if recept_desk[i] is not None:
                customer, remain = recept_desk[i]
                remain -= 1

                if remain == 0:
                    heapq.heappush(repair_wait, (time + 1, i + 1, customer))
                    recept_desk[i] = None
                else:
                    recept_desk[i] = (customer, remain)

        #창구가 비어있으면 데스크에 값 채우기
        for i in range(N):
            if recept_desk[i] is None and recept_wait:
                customer = recept_wait.popleft()
                remain = ai[i]
                recept_desk[i] = (customer, remain)
                used_recept[customer] = i+1

        # 창구가 꽉 차있으면 남은 시간 줄이고, 시간 0이면 done_repair로 이동
        for i in range(M):
            if repair_desk[i] is not None:
                customer_id, remain_time = repair_desk[i]
                remain_time -=1

                if remain_time == 0:
                    done_repair.append(customer_id)
                    repair_desk[i] = None
                else:
                    repair_desk[i] = (customer_id, remain_time)

        # 창구가 비어있으면 데스크에 값 채우기
        for i in range(M):
            if repair_wait and repair_desk[i] is None:
                finish_time, recept_idx, customer_id = heapq.heappop(repair_wait)
                remain_time = bi[i]
                repair_desk[i] = (customer_id,remain_time)
                used_repair[customer_id] = i+1

        time += 1

    ans = 0
    #used_recept[i]가 A, used_repair[i]가 B인 거
    for i in range(1, K+1):
        if used_recept[i] == A and used_repair[i] == B:
            ans += i

    if ans == 0:
        ans = -1

    print(f'#{t} {ans}')





