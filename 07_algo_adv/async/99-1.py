import time
import threading

def cpu_task(n):
    total = 0
    for i in range(n):
        total += i * i
    return total

def run_sequential(n_tasks=4, n=10_000_000):
    t0 = time.perf_counter()
    for _ in range(n_tasks):
        cpu_task(n)
    print("순차 실행 소요시간:", time.perf_counter() - t0)

def run_threaded(n_tasks=4, n=10_000_000):
    t0 = time.perf_counter()
    threads = []
    for _ in range(n_tasks):
        t = threading.Thread(target=cpu_task, args=(n,))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    print("스레드 실행 소요시간:", time.perf_counter() - t0)

run_sequential()
run_threaded()