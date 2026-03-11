import time
from multiprocessing import Pool, cpu_count

def cpu_task(n: int):
    total = 0
    for i in range(n):
        total += i * i
    return total

def main():
    t0 = time.perf_counter()

    with Pool(processes=cpu_count()) as pool:
        results = pool.map(cpu_task, [10_000_000] * cpu_count())

    dt = time.perf_counter() - t0
    print('작업 완료', len(results))
    print(f'소요 시간: {dt:.3f}s')

'''
    multiprocessing을 사용할때는 반드시 
    if __name__ == "__main__": 블록 안에서 main() 함수를 호출해야 함
    Windows에서 multiprocessing이 프로세스를 생성할 때, 현재 모듈을 다시 실행하기 때문

    이 블록이 없으면, 프로세스가 생성될 때마다 main() 함수가 실행되어, 
    다시 프로세스를 생성하는 악순환이 발생
'''
if __name__ == "__main__":
    main()