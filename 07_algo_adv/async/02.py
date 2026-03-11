import time
import threading    # 멀티스레딩을 사용할 수 있도록 함

def io_task(i, delay=0.2):
    time.sleep(delay)  # I/O 대기 흉내
    print(f"{i} 번째 태스크 완료")

def run_threaded(n=20):
    t0 = time.perf_counter()
    threads = []

    for i in range(n):
        # 각 태스크를 별도의 스레드에서 실행
        # target은 실행할 함수, args는 함수에 전달할 인자
        t = threading.Thread(target=io_task, args=(i,))
        t.start()
        threads.append(t)

    # 모든 스레드가 완료될 때까지 대기
    for t in threads:
        t.join()

    dt = time.perf_counter() - t0
    print(f"스레드 실행 소요시간: {dt:.3f}초")


run_threaded()