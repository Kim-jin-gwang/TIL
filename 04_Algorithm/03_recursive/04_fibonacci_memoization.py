def fibonacci_memoization(n):
    global count
    count += 1
    # 함수가 호출될 때 마다
    # n이 2 이상인데, 아직 계산된적이 없어서
    # memo[n]의 값이 0인 경우에, 연산을 수행
    if n >= 2 and memo[n] == 0:
        memo[n] = fibonacci_memoization(n-2) + fibonacci_memoization(n-1)
    return memo[n]

count = 0

# 이전에 해결한적 있는 문제를 다시 계산하지 않도록
# 순서에 맞춰 어딘가에 저장 해 두자. -> 충분히 큰 공간
N = 1000
memo = [0] * (N+1)
# print(memo)
memo[0] = 0
memo[1] = 1
# print(memo)
result = fibonacci_memoization(N)
print(result)
# print(memo)
print(count)