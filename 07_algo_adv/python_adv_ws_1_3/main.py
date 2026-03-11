import asyncio


def iter_log_lines(path):
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            yield line.strip()

def parse_logs(lines):
    # CSV 라인을 dict 로그로 파싱
    for line in lines:
        parts = line.split(',')

        if len(parts) != 5:
            continue

        ts, endpoint, status, response, user = parts

        if not (status.isdigit() and response.isdigit() and user.isdigit()):
            continue

        yield {
            "timestamp": ts,
            "endpoint": endpoint,
            "status_code": int(status),
            "response_time": int(response),
            "user_id": int(user)
        }

def filter_error_logs(logs):
    for log in logs:
        if log['status_code'] in (404,500):
            yield log

async def consume_logs(logs, max_items):
    res = {
        "total":0,
        "endpoint_counts" : {}
    }

    cnt = 0

    for log in logs:
        if cnt >= max_items:
            break

        await asyncio.sleep(0.02)

        endpoint = log['endpoint']

        res['total'] += 1
        res['endpoint_counts'][endpoint] = (
            res['endpoint_counts'].get(endpoint,0) + 1
        )

        cnt += 1
    
    return res


async def main():
    path = "logs_stream.txt"

    lines = iter_log_lines(path)
    parsed = parse_logs(lines)
    errors = filter_error_logs(parsed)

    result = await consume_logs(errors, max_items=40)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
