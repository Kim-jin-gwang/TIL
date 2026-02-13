import sys
sys.stdin = open('input.txt')


def finish_tasks(time, desks, is_repair):
    '''
    창구에서 완료된 작업을 처리
    Args:
        time: 현재 시각
        desks: 창구 상태 배열 [고객번호, 종료시간]
        is_repair: 정비 창구 여부
    return: 
        정비 창구의 경우 완료된 고객 수를 반환
    '''
    done_cnt = 0  # 이번 시간에 완료된 고객 수
    next_q = []  # 접수를 마치고 정비를 기다리는 고객 목록

    for i in range(len(desks)):
        if desks[i][0] > 0 and desks[i][1] == time:  # 현재 시간에 작업이 끝나는 고객이 있다면
            customer_id = desks[i][0]
            desks[i][0] = 0  # 창구 비우기
            if is_repair:
                done_cnt += 1  # 정비 완료 고객 수 증가
            else:
                next_q.append(customer_id)  # 정비 대기 큐로 이동할 고객 추가

    if is_repair:
        return done_cnt
    return next_q


def process_arrivals(time, idx):
    global ARR_T, K
    '''
    현재 시간에 도착한 신규 고객을 처리
    Args:
        time: 현재 시각
        idx: 현재까지 처리된 도착 인덱스
    return:
        new_q: 이번 시간에 도착한 고객 목록
        idx: 다음 도착 고객 인덱스
    '''
    # time: 현재 시각
    # idx: 현재까지 처리된 도착 인덱스
    # 현재 시간에 도착한 신규 고객을 처리
    new_q = []  # 이번 시간에 도착한 고객 목록
    while idx < K and ARR_T[idx] == time:
        new_q.append(idx + 1)  # 고객 번호는 1부터 시작
        idx += 1  # 다음 도착 고객을 가리키도록 인덱스 증가
    return new_q, idx


def assign_desks(time, queue, desks, is_repair):
    global REC_T, REP_T, INFO
    '''
    대기 큐의 고객을 빈 창구에 배정
    Args:
        time: 현재 시각
        queue: 대기 큐(고객 번호 목록)
        desks: 창구 상태 배열 [고객번호, 종료시간]
        is_repair: 정비 창구 여부
    return:
        없음
    '''
    if not queue:  # 대기열에 고객이 없으면 종료
        return

    proc_times = REP_T if is_repair else REC_T

    # 우선순위에 따라 대기 큐 정렬
    if is_repair:
        queue.sort(key=lambda cid: (INFO[cid][1], INFO[cid][0]))  # 정비 큐: 접수완료시간 -> 접수창구 순
    else:
        queue.sort()  # 접수 큐: 고객번호 순

    remain_q = []  # 창구를 배정받지 못한 고객 목록
    for customer_id in queue:
        assigned = False
        for i in range(len(desks)):  # 번호가 낮은 창구부터 확인
            if desks[i][0] == 0:
                desks[i][0] = customer_id  # 창구에 고객 배정
                desks[i][1] = time + proc_times[i]  # 종료 시간 계산
                if is_repair:
                    INFO[customer_id][2] = i + 1  # 정비 창구 이용 내역 기록
                else:
                    INFO[customer_id][0] = i + 1  # 접수 창구 이용 내역 기록
                    INFO[customer_id][1] = desks[i][1]  # 접수 완료 시간 기록
                assigned = True
                break
        if not assigned:
            remain_q.append(customer_id)  # 빈 창구가 없어 대기해야 하는 고객

    # 대기 큐를 배정받지 못한 고객들로 갱신
    queue[:] = remain_q


def calc_result():
    global K, A, B, INFO
    '''
    목표 창구를 이용한 고객들의 번호 합을 계산
    Args:
        K: 전체 고객 수
        A: 목표 접수 창구 번호
        B: 목표 정비 창구 번호
        INFO: 고객별 이용 기록
    return:
        조건에 맞는 고객 번호 합(없으면 -1)
    '''
    total_sum = 0
    for i in range(1, K + 1):
        if INFO[i][0] == A and INFO[i][2] == B:
            total_sum += i  # 조건에 맞는 고객 번호 합산

    return total_sum if total_sum > 0 else -1  # 합산 결과가 0이면 -1을 반환

T = int(input())
for tc in range(1, T+1):
    N, M, K, A, B = map(int, input().split())  # 접수창구 수, 정비창구 수, 고객 수, 목표 창구 번호
    REC_T = list(map(int, input().split()))  # REC_T: 접수 창구별 처리 시간 (Reception Time)
    REP_T = list(map(int, input().split()))  # REP_T: 정비 창구별 처리 시간 (Repair Time)
    ARR_T = list(map(int, input().split()))  # ARR_T: 고객별 도착 시간 (Arrival Time)

    reception_desks = [[0, 0] for _ in range(N)]  # 접수 창구 상태: [고객번호, 종료시간]
    repair_desks = [[0, 0] for _ in range(M)]  # 정비 창구 상태: [고객번호, 종료시간]
    INFO = [[0, 0, 0] for _ in range(K + 1)]  # 고객별 이용 기록: [접수창구, 접수완료시간, 정비창구]

    reception_q = []  # 접수 대기 큐
    repair_q = []  # 정비 대기 큐

    time = 0
    done = 0  # 정비를 모두 마친 고객 수
    idx = 0  # 도착 처리가 완료된 고객 인덱스

    while done < K:  # 모든 고객이 정비를 마칠 때까지 시뮬레이션
        # 1. 정비 창구 완료 처리
        done += finish_tasks(time, repair_desks, is_repair=True)
        # 2. 접수 창구 완료 처리 및 정비 큐로 이동
        repair_q.extend(finish_tasks(time, reception_desks, is_repair=False))
        # 3. 신규 고객 도착 처리
        new_q, idx = process_arrivals(time, idx)
        reception_q.extend(new_q)
        # 4. 정비 창구 배정
        assign_desks(time, repair_q, repair_desks, is_repair=True)
        # 5. 접수 창구 배정
        assign_desks(time, reception_q, reception_desks, is_repair=False)

        time += 1  # 시간 증가

    result = calc_result()  # 최종 결과 계산 후 반환
     
    print(f'#{tc} {result}')