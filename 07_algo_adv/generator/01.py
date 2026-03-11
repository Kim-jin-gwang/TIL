import tracemalloc
import time

def report(label):
    # 현재와 최대 메모리 사용량을 바이트 단위로 반환
    current, peak = tracemalloc.get_traced_memory()
    print(f"{label} | 현재={current/1024/1024:8.2f} MiB | 최대={peak/1024/1024:8.2f} MiB")

N = 5_000_000
tracemalloc.start()
report("시작")

# 1) materialize: 리스트로 한 번에 만들기
t0 = time.perf_counter()
lst = [i for i in range(N)]
report("리스트 컴프리헨션 생성 후")
print(f"리스트 생성 시간: {time.perf_counter() - t0:.3f}초")

# 리스트를 지우고 GC 타이밍 영향을 줄이기 위해 참조 제거
lst = None
report("리스트 제거 후")

# 2) lazy: 제너레이터는 만들기만 하면 거의 할당이 없다
t0 = time.perf_counter()
gen = (i for i in range(N))
report("제너레이터 생성 후")
print(f"제너레이터 생성 시간: {time.perf_counter() - t0:.3f}초")

# 다만 "소비"하면 그때 계산이 진행됨 (여기서는 누적합으로 소비)
t0 = time.perf_counter()
s = sum(gen)
report("제너레이터 소비 후")
print(f"제너레이터 소비 시간: {time.perf_counter() - t0:.3f}초")
print("합계:", s)

tracemalloc.stop()