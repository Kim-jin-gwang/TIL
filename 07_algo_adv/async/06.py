import asyncio
import time

def blocking_task(i):
    time.sleep(0.5)  # 블로킹 작업
    return f"{i}번째 태스크 완료"

async def main():
    # 현재 실행 중인 이벤트 루프를 가져옴
    loop = asyncio.get_running_loop()

    tasks = [
        # run_in_executor는 첫 번째 인자로 실행할 executor를 받음 (None은 기본 ThreadPoolExecutor 사용)
            # ThreadPoolExecutor: 블로킹 작업을 별도의 스레드에서 실행, 메인 이벤트 루프가 블로킹되지 않도록 함
            # ProcessPoolExecutor: 별도의 프로세스에서 실행, CPU 바운드 작업에 적합함
        loop.run_in_executor(None, blocking_task, i)
        for i in range(5)
    ]

    results = await asyncio.gather(*tasks)
    print(results)

asyncio.run(main())