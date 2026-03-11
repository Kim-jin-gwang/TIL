def fibonacci_generator():
    n1, n2 = 0, 1
    while True:
        yield n1
        n1, n2 = n2, n1 + n2
gen = fibonacci_generator()
# 첫 10개의 피보나치 수를 출력
for _ in range(10):
    print(next(gen))    # gen.__next__()와 동일

print(next(gen))    # 11번째 피보나치 수
print(next(gen))    # 12번째 피보나치 수
