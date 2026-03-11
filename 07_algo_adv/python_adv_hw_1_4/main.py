import asyncio
import time

def heavy_computation():
    print("Heavy Task 연산 시작")
    time.sleep(3)
    print("Heavy Task 연산 완료")
    
async def light_task():
    print("Light Task 연산 시작")
    await asyncio.sleep(1)
    print("Light Task 연산 완료")

async def main():
    loop = asyncio.get_running_loop()

    heavy = loop.run_in_executor(None, heavy_computation)
    light = asyncio.create_task(light_task())

    await asyncio.gather(heavy,light)

# asyncio.run(main())을 사용하여 비동기 메인 함수를 실행
asyncio.run(main())