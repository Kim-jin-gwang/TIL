def fibonacci(n):
    global count
    count += 1
    # 함수가 호출될 때 마다
    # 피보나치의 식 f(N) = f(N-2) + f(N-1)
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n-2) + fibonacci(n-1)

count = 0
# 사용 예시
print(fibonacci(1000)) # 55를 출력합니다. (피보나치 수열: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55)
print(count)
