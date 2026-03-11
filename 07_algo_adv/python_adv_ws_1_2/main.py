def even_generator(limit):
    cur = 0
    while cur <= limit:
        if cur % 2 == 0:
            yield cur
            cur += 1
        cur+=1

# 사용 예시:
N = 10
for even_number in even_generator(N):
    print(even_number)
    