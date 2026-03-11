import asyncio

async def good_task(i, delay=0.2):
    await asyncio.sleep(delay)  # 비동기 대기
    print(f"{i} 번째 태스크 완료")

async def main():
    tasks = [good_task(i) for i in range(20)]
    await asyncio.gather(*tasks)

asyncio.run(main())