import asyncio
import time

async def bad_task(i):
    time.sleep(0.2)  # 블로킹
    print(f"{i} 번째 태스크 완료")

async def main():
    tasks = [bad_task(i) for i in range(5)]
    # gather()는 여러 코루틴을 동시에 실행하고, 
    # 모든 코루틴이 완료될 때까지 기다림
    await asyncio.gather(*tasks)

asyncio.run(main())