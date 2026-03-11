import time

def io_task(i, delay=0.2):
    # 네트워크/디스크 대기를 흉내
    time.sleep(delay)  
    return f"태스크-{i}"

def run_sequential(n=20):
    # perf_counter()는 코드 실행 시간을 측정하는 데 사용
    # 시작 시간 기록
    t0 = time.perf_counter()

    results = []
    for i in range(n):
        results.append(io_task(i))
    
    # 종료 시간과 시작 시간의 차이를 계산하여 실행 시간을 구함
    dt = time.perf_counter() - t0
    print(f'실행 소요시간: {dt:.3f}초')


run_sequential()