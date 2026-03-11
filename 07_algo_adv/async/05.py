import asyncio

async def task(i, delay=0.2):
    await asyncio.sleep(delay)
    print(f"{i} 번째 태스크 완료")
    return f"태스크-{i}"

async def main():
    print("create_task 실행")
    t1 = asyncio.create_task(task(1, 4))
    t2 = asyncio.create_task(task(2, 3))

    print()
    print("gather 실행")
    results = await asyncio.gather(
        task(3, 2),
        task(4, 1)
    )
    print(f"gather 결과: {results}")

    print()
    # create_task로 생성된 태스크는 백그라운드에서 실행되고 있음
    # await t1과 await t2는 각각의 태스크가 완료될 때까지 기다림
    print(f"create_task 결과: {await t1}, {await t2}")

asyncio.run(main())

