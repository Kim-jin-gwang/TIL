def fibonacci_for_loop(n):
    # N이 0 이라면 0이 되어야 한다.
    if n == 0:
        return 0
    # N이 1이라면 1이 되어야 한다.
    elif n == 1:
        return 1
    # 그 외의 상황들
    else:
        # f(n) = f(n-1) + f(n-2)
        a, b = 0, 1 # a => f(0), b => f(1)
        # 2부터 n까지의 반복을 통해서 피보나치 수를 구한다.
        # 이 피보나치는 사실 순회하면서 얻게될 각각의 Ni 값은 사용하지 않음
        for _ in range(2, n+1):
            # 다음 피보나치 수
            a, b = b, a+b
            # next_fibo = a + b
            # a = b
            # b = next_fibo
            # print(next_fibo, end=' ')
        # return next_fibo
        return b
# 사용 예시
print(fibonacci_for_loop(10)) # 55